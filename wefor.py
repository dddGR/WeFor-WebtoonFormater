import os, sys, struct
from typing import List, Generator, Dict, Union, Tuple
import numpy as np
from numpy.typing import NDArray
from argparse import ArgumentParser
from natsort import natsorted
from skimage.util import img_as_ubyte
from skimage.io import imread, imsave
from skimage.transform import resize as imresize
from skimage.color import rgb2gray, gray2rgb
from skimage.exposure import rescale_intensity

from classes import(UserInput,
                    PageColumn,
                    PageColumnTemp,
                    PanelSection, 
                    U8_RANGE,
                    DEF_INPUT_TYPE,
                    DEF_OUT_DIR,
                    DEF_TOLERANCE,
                    DEF_MIN_HEIGHT_P,
                    DEF_PAGE_DIRECTION,
                    MAX_PERCENT_HEIGHT)


SUPORTED_FORMATS: tuple = ('png', 'jpg', 'jpeg')
# percentage of image width size missmatch to consider resizable, if the missmatch is too large, highly just filler image.
SOURCE_IMAGE_MAX_VARIATION: int = 10
# some webtoon have artificial on the side of the image that not noticeable when viewing normally but still affect the detection of blank panels. This is the number of pixels to cut from the side
SIDE_PIXEL_TO_CUT: int = 10


def parse_input_args() -> UserInput:
    """ Parse command line arguments and return them as a ParserArguments object """
    parser: ArgumentParser = ArgumentParser(description="Reformat Webtoon/Manhwa into 3:4 format.", \
                                            usage="input_dir [-i|--input_type] [-o|--output_dir] [-t|--tolerance] [-d|--direction]")
    parser.add_argument("input_dir", help="Directory containing chapters folder or image files.")
    parser.add_argument("-i", "--input_type", choices=["auto", "main", "chapter"], default=DEF_INPUT_TYPE, help="Type of input folder to process (default: auto)")
    parser.add_argument("-o", "--output_dir", type=str, default=DEF_OUT_DIR, help="Directory to save processed images (default: .\\_output)")
    parser.add_argument("-t", "--tolerance", type=int, default=DEF_TOLERANCE, help="Tolerance level for detect blank rows <0-255> (default: 15)")
    parser.add_argument("-m", "--min_height", type=int, default=DEF_MIN_HEIGHT_P, help="Min height for spliting panel (% of output height) (default: 1.0)")
    parser.add_argument("-d", "--direction", choices=["left", "right"], default=DEF_PAGE_DIRECTION, help="Reading direction (default: left)")
    parser.add_argument("-v", "--verbose", type=bool, default=False, help="Verbose mode")

    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print(f"Input directory does not exist: {args.input_dir}")
        sys.exit("Exiting program...")

    return UserInput(input_dir=args.input_dir,
                     input_type=args.input_type,
                     output_dir=args.output_dir,
                     tolerance=args.tolerance,
                     min_height_p=args.min_height,
                     direction=args.direction,
                     verbose=args.verbose)


def _get_image_dimensions_from_metadata(file_path) -> Tuple[int, int]:
    with open(file_path, 'rb') as f:
        data = f.read(24)
        # check if the file is a PNG file
        if data.startswith(b'\211PNG\r\n\032\n') and data[12:16] == b'IHDR':
            width, height = struct.unpack('>II', data[16:24])
            return width, height
        # check if the file is a JPEG file
        elif data[0:2] == b'\xff\xd8':
            f.seek(0)
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf:
                f.seek(size, 1)
                byte = f.read(1)
                while ord(byte) == 0xff:
                    byte = f.read(1)
                ftype = ord(byte)
                size = struct.unpack('>H', f.read(2))[0] - 2
            f.seek(1, 1)  # skip precision byte
            height, width = struct.unpack('>HH', f.read(4))
            return width, height
        else:
            raise ValueError("Unsupported image format")


def get_ImageMaxWidth(image_dir: List[str]) -> int:
    """
    Source images may have different width, this function returns the largest width that can be used to resize the smaller one to match.

    - NOTE: this is not usualy happen, but just in case the source files have one that is much larger or smaller than the rest. This will raise an error.
    - (Resize too much will cause quality misssmatch or that "special" image may not the actual comic page)
    """
    max_width: int = 0
    for dir in image_dir:
        try: # only support png and jpeg
            width, _ = _get_image_dimensions_from_metadata(dir)
        except ValueError:
            width = imread(dir).shape[1]

        if max_width != 0:
            if abs(width - max_width) > max_width * SOURCE_IMAGE_MAX_VARIATION // 100:
                raise ValueError(f"Images missmatch [{max_width}] vs [{width}]. Please check your image file: {dir.split('\\')[-1]}")
        if width > max_width:
            max_width = width

    return max_width


def get_ListPanels(blank_mask: NDArray, min_height: int) -> List[PanelSection]:
    """
    Iterates through the blank_mask and determines the start and end points of each panel.
    """
    panels: List[PanelSection] = []
    i_last: int = 0
    p_type_last: bool = blank_mask[0]

    for index, p_type in enumerate(blank_mask[1:], start=1):
        type: bool = blank_mask[index - 1]
        if p_type == type:
            continue
        
        if index - i_last < (min_height // 2):
            # too close to last panel, assume it is the same type
            type = p_type_last

        panel = PanelSection(i_last, index - 1, type)
        i_last = index
        p_type_last = type
        
        if panels and panels[-1].is_blank == panel.is_blank:
            # same type with previous panel, consider to merge
            if panel.is_blank or (not panel.is_blank and panel.height < min_height):
                panels[-1].end = panel.end
                continue

        panels.append(panel)

    if i_last < len(blank_mask) - 1:
        panels.append(PanelSection(i_last, len(blank_mask), blank_mask[-1]))

    return panels


def get_SplitedColumns(panels: List[PanelSection], page_height: int) -> List[PageColumn]:
    """
    With blank mask, iterates line by line to get all the blank and content panels.
    Packs them into page columns. and returns a list of PageColumn (coordinates of panels).
    """
    out_columns: List[PageColumn] = []
    column = PageColumnTemp(max_height=page_height)

    for panel in panels:
        ret_columns = column.add_Panel(panel)

        for col in ret_columns:
            out_columns.append(col)

    if column.content:
        out_columns.append(PageColumn(column.evaluate(True)))

    return out_columns


""" FOR TESTING PURPOSES """
def save_out_panels(img: NDArray, panels: List[PanelSection], dir: str) -> None:
    for panel in panels:
        out_panel: NDArray = img[panel.start:panel.end]
        print(f"Saving image... {panel.start}-{panel.end}")
        imsave(os.path.join(dir, f"_output_pcs\\p_{panel.start}-{panel.end}_{panel.is_blank}.jpg"), out_panel)
    # sys.exit("Done!!!")


def slice_Image(img_source: NDArray, page_height: int, user: UserInput) -> Generator[NDArray, None, None]:
    """
    Slices the image into smaller panels.
    Packs them into pages with ratio of 3:4 and output them.

    - NOTE: `blank row` is the row that contain pixels that have the same color.
    """
    img_gray: NDArray = rgb2gray(img_source[:,SIDE_PIXEL_TO_CUT:-SIDE_PIXEL_TO_CUT])
    img_gray = img_as_ubyte(rescale_intensity(img_gray, in_range=(0.0, 0.8), out_range=(0, 1)))
    blank_mask = np.all(np.abs(img_gray - np.mean(img_gray, axis=1, keepdims=True)) <= user.tolerance, axis=1)
    min_panel_height: int = int(page_height * user.min_height_p / 100)

    columns: List[PageColumn] = get_SplitedColumns(get_ListPanels(blank_mask, min_panel_height),
                                                   page_height)

    out_page: List[NDArray] = []
    # The strategy here is simple. Inside each column will contain coordinates of all the panels, iterate them to get the coresponding image. Concatenate them together to form a complete column. Once we have 2 columns (complete page), join and output to save.
    for col in columns:
        if col.blank_num:
            pad_height: int = (page_height - col.content) // col.blank_num

        panel_combined: List = []
        for panel in col.panels:
            img = img_source[panel.start:panel.end]
            
            if panel.is_blank:
                if panel.start < 0:
                    img = np.ones((pad_height, img_source.shape[1], 3), dtype=np.uint8) * (U8_RANGE + panel.start)

                # TODO: maybe just fill all the blank with black or white image to avoid artifact??
                try:
                    img = img_as_ubyte(imresize(img, (pad_height, img.shape[1])))
                except Exception as e:
                    raise ValueError(f"resize padding: {e}")

            panel_combined.append(img)
        
        out_img: NDArray = np.vstack(panel_combined)
        # sometime, output image will be slightly missmatch. 1% is not noticeable
        if abs(out_img.shape[0] - page_height) <= (page_height * MAX_PERCENT_HEIGHT // 100):
            out_img = img_as_ubyte(imresize(out_img, (page_height, out_img.shape[1]), anti_aliasing=True))
        else:
            raise ValueError(f"output height missmatch: {out_img.shape[0]} != {page_height}")
        out_page.append(out_img)

        if (len(out_page) == 2):
            if user.direction == "right":
                out_page.reverse()
            yield np.hstack(out_page)
            out_page = []

    if out_page:
        yield out_page[0]


def process_Folder(imgs_dir: List[str], output_dir: str, user: UserInput) -> None:
    try:
        column_width = get_ImageMaxWidth(imgs_dir)
    except ValueError as err:
        if user.verbose:
            print(f"[failed] to get max width: \"{err}\"")
        raise ValueError(f"image size missmatch")

    # COMBINE ALL OF THEM INTO A SINGLE ARRAY, CHECK SIZE AND RESIZE IF NEEDED (WITDH ONLY)
    # TODO: maybe use Generator here to reduce memory usage
    _imgs: list[NDArray] = []
    for dir in imgs_dir:
        _img: NDArray = imread(dir)
        if _img.ndim == 2:
            _img = img_as_ubyte(gray2rgb(_img))
        elif _img.shape[2] > 3:
            _img = _img[:, :, :3]

        if _img.shape[1] != column_width:
            if user.verbose:
                print(f"[resizing] {dir.split('\\')[-1]}")
            new_dimensions: Tuple[int, int] = (_img.shape[0] / _img.shape[1] * column_width, column_width)
            try:
                _img = img_as_ubyte(imresize(_img, new_dimensions, anti_aliasing=True))
            except Exception as e:
                raise ValueError(f"resize image: \"{e}\"")
        _imgs.append(_img)

    stacked_image: NDArray = np.vstack(_imgs)

    # 3:4 ratio, 2 columns per page. Edit if need more.
    final_page_height: int = column_width * 8 // 3
    # PROCESS IMAGE
    for i, col in enumerate(slice_Image(stacked_image, final_page_height, user)):
        if user.verbose:
            print(f"Saving page {i + 1}")
        imsave(os.path.join(output_dir, f"page_{i + 1:02}.jpg"), col)


def get_FilesList(user: UserInput) -> Generator[Tuple[List[str], str, int, int], None, None]:
    """ 
    Get all the chapter folders and with each folder get all the image files and put them in a list
    
    Parameters
    ----------
    input_dir: str
        The input directory

    Other Parameters
    ----------------
    mode: str
        - auto: get all the files
        - main: get all the files in the main folder
        - chapter: get all the files in the sub folders (aka. chapter folder)
    
    Returns
    -------
    files_list: tuple[str, list[str]]
        The list of all the files in the input directory or sub directories.
        If have multiple directories, it will return in a chunk of tuples
        contain folder name and all the files in that folder.
    """
    if user.input_type not in ("auto", "main", "chapter"):
        raise ValueError("[--mode] must be 'auto', 'main' or 'chapter'")

    folders: List[str] = []
    files: List[str] = []

    with os.scandir(user.input_dir) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.name.startswith("_"):
                folders.append(entry.path)
            elif entry.is_file() and entry.name.lower().endswith(SUPORTED_FORMATS):
                files.append(entry.path)

    if user.input_type == "auto":
        user.input_type = "main" if folders else "chapter"

    if user.input_type == "chapter":
        if files:
            yield (natsorted(files), user.main_folder_name, 1, 1)
            return
        else:
            raise FileNotFoundError(f"no image in \"{user.main_folder_name}\"")

    if not folders:
        raise FileNotFoundError(f"no chapter in \"{user.input_dir}\"")

    total_chapters: int = len(folders)
    for index, folder in enumerate(natsorted(folders)):
        chapter_name: str = folder.split('\\')[-1]
        file_list: List[str] = []
        with os.scandir(folder) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.lower().endswith(SUPORTED_FORMATS):
                    file_list.append(entry.path)
        if file_list:
            yield (natsorted(file_list), chapter_name, index + 1, total_chapters)
        else:
            if user.verbose:
                print(f"[skipping] - \"{chapter_name}\" not containing any images.")


def do_FormatWebtoon(user: UserInput) -> None:
    # HANDLE INPUT DIR, IF CONTAIN MULTIPLE CHARPTER THEN PROCESS EACH CHARPTER
    for f_list, folder, current, total in get_FilesList(user):
        # HANDLE OUTPUT DIR
        out_dir: str = user.output_dir
        if user.main_folder_name != folder:
            out_dir = os.path.join(out_dir, folder)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        print(f"Processing [{current}/{total}]: {folder}")
        process_Folder(f_list, out_dir, user)


def main() -> None:
    # try:
    #     do_FormatWebtoon(parse_input_args())
    # except Exception as err:
    #     print(f"[failed]: \"{err}\"")

    do_FormatWebtoon(parse_input_args())


if __name__ == "__main__":
    main()
