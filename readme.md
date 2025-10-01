# WEBTOON FORMATTER

## Overview

**Webtoon Formatter (WeFor)** is a Python tool designed to reformat images from long strip pages (such as webtoons or manhwa) into a **3:4 aspect ratio** suitable for e-ink devices (this is my main use of this script).

This project start off from [ManhwaFormatter](https://github.com/eskutcheon/ManhwaFormatter/) and some inspration are from [comic-splitter](https://github.com/zuomuo/comic-splitter). However, those projects did not fully meet my needs.

So [FINE, I'LL DO IT MYSELF](#output-example)

> **Note:** This script works best when the webtoon background is simple (e.g., black, white, orange... or whatever) and the panels are short enough to fit on one page.  
> In reality, webtoons can vary significantly in size and form, sometimes it contain some background effects (like stripes or smoke) that may not be handled well. I recommend testing with a single chapter before processing an entire webtoon to avoid unexpected results.

### Output example

---
<p align=center>
    <image src="./img/example.jpg" width=1600>
</p>

## Features

- This tool automatically detects the type of input folder, making it easy to use. Just pass in the main folder directory, and you're set.
- You can adjust parameters to experiment with different settings.
- Outputs maintain the same folder structure as the input, and the original files are copied, ensuring no damage to the source files.
- A simple GUI is included for users who are not familiar with command-line environments.

## Installation

To use this project, ensure you have Python installed on your machine.

```bash
git clone https://github.com/dddGR/WeFor-WebtoonFormater.git
cd ./WeFor-WebtoonFormater
pip install -r ./requirements.txt
```

For additional GUI requirements, run:

```bash
pip install -r ./gui/requirements_gui.txt
```

> Note: A pre-compiled executable file is available for users who do not have or are unfamiliar with Python (Windows only, why are you using Linux but not python??)

## Usage

You can run the script with the following syntax:

```bash
python wefor.py <input_dir> [-i|--input_type] [-o|--output_dir] [-t|--tolerance] [-m|--min_height] [-d|--direction] [-v|--verbose]
```

For those who prefer the GUI version:

```bash
python main.py
```

> Note: The first time you run the GUI version, a `settings.json` file will be created in the same directory. This file saves all the parameters you use and can be load next time.

### Source Files Structure

The input folder should contain all the chapter folders. You can choose to process each chapter individually for testing. Any folder starting with the `_` character will be skipped.

The output will be located inside the main folder, with a default name of `_output`, containing all the chapter folders as in the main folder. You can change the output location using the `-o` argument.

```bash
main_folder/        ### (input dir)
├── _rand_name/     ### (folder start with '_' will be skip)
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Chapter 01/     ### (input dir if chose chapter mode)
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Chapter 02/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── Chapter .../
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

> Note:
>
> - Folder names can differ from the example above, but it's advisable to keep them short and avoid unique characters.
> - When downloading comics from the internet, each chapter may contain filler images of different sizes, which can cause errors.
> Consider cleaning them up first.
> - If you want to rename folders and files, I recommend using [Bulk Rename Utility](https://www.bulkrenameutility.co.uk/).

### Arguments

| Argument             | Description                                                                                     | Default Value         |
|----------------------|-------------------------------------------------------------------------------------------------|-----------------------|
| `input_dir`          | Directory containing chapters folder or image files. | N/A                   |
| `-i`, `--input_type` | Type of input folder to process. Options: `auto`, `main`, `chapter`. | `auto`                |
| `-o`, `--output_dir` | Directory to save processed images. | `./_output`           |
| `-t`, `--tolerance`  | Tolerance level for detecting blank rows (0-255). Increasing this makes detection less sensitive, which can help with low-quality sources that have many artifacts.| `15`                  |
| `-m`, `--min_height` | Minimum height for splitting panels (as a percentage of the output height). Lower this if the output page has many elements close together, although this is rarely needed. | `1.0`                  |
| `-d`, `--direction`  | Reading direction. Options: `left` for left-to-right (normal comic), `right` for right-to-left (like manga). | `left`                |
| `-v`, `--verbose`    | Enable verbose mode for detailed output. | `False`               |

## Example

To reformat images in the `main_folder`:

```bash
python reformat.py <main_folder_directory>
```

And to reformat images in the `main_folder` and save them to the `output` directory with a tolerance of `15`, you would run:

```bash
python reformat.py <main_folder_directory> -o <output_directory> -t 15
```

## Documentation

I tried to explain every detail with comments in the code. Since this is just a small and simple script, feel free to explore all the files if you're interested in understanding the implementation.

## Contributing

I have not tested this script with a wide variety of webtoons, so it may not work in every scenario.  
Please feel free to submit a pull request or open an issue for any bugs or feature requests.
