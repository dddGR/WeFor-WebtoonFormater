from typing import List, Tuple

U8_RANGE: int = 2**8
PAD_WHITE: int = -1         # for signal to create white padding
PAD_BLACK: int = -U8_RANGE  # for signal to create black padding

# number of percent of content in one column to be considered "full"
FINAL_CONTENT_PERCENTAGE: int = 85

# amout of percent of content in one column to be considered "low"
LOW_CONTENT_PERCENTAGE: int = 30

# 101% | maximum height of a panel, 1% is not noticeable when stretching so is considered can be fit in. This only affect when evaluating that panel can be add in or not, and when after panel image is combined.
MAX_PERCENT_HEIGHT: int = 101

# percentage of panel page height to be considered can be remove and split.
SPLITABLE_PERCENTAGE: int = 2

# default value for user input
DEF_INPUT_TYPE: str = "auto"
DEF_OUT_DIR: str = "auto"
DEF_TOLERANCE: int = 15
DEF_MIN_HEIGHT_P: float = 1.0 # == 1%
DEF_PAGE_DIRECTION: str = "left"

class UserInput:
    def __init__(self,  input_dir: str,
                        input_type: str = DEF_INPUT_TYPE,
                        output_dir: str = DEF_OUT_DIR,
                        tolerance: int = DEF_TOLERANCE,
                        min_height_p: float = DEF_MIN_HEIGHT_P,
                        direction: str = DEF_PAGE_DIRECTION,
                        verbose: bool = False) -> None:
        self.input_dir = input_dir
        self.input_type = input_type
        self.output_dir = output_dir
        self.tolerance = tolerance
        self.min_height_p = min_height_p
        self.direction = direction
        self.verbose = verbose

    @property
    def main_folder_name(self) -> str:
        return self._main_folder_name

    @property
    def input_dir(self) -> str:
        return self._input_dir

    @input_dir.setter
    def input_dir(self, value: str) -> None:
        self._input_dir = value
        self._main_folder_name = value.split('\\')[-1]

    @property
    def input_type(self) -> str:
        return self._input_type

    @input_type.setter
    def input_type(self, value: str) -> None:
        self._input_type = value

    @property
    def output_dir(self) -> str:
        return self._output_dir

    @output_dir.setter
    def output_dir(self, value: str) -> None:
        self._output_dir = value

    @property
    def tolerance(self) -> int:
        return self._tolerance

    @tolerance.setter
    def tolerance(self, value: int) -> None:
        self._tolerance = value

    @property
    def min_height_p(self) -> float:
        return self._min_height_p

    @min_height_p.setter
    def min_height_p(self, value: float) -> None:
        self._min_height_p = value

    @property
    def direction(self) -> str:
        return self._direction

    @direction.setter
    def direction(self, value: str) -> None:
        self._direction = value

    @property
    def verbose(self) -> bool:
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self._verbose = value


class PanelSection:
    @property
    def height(self) -> int:
        return self._end - self._start

    @property
    def start(self) -> int:
        return self._start
    
    @start.setter
    def start(self, value: int) -> None:
        self._start = value

    @property
    def end(self) -> int:
        return self._end
    
    @end.setter
    def end(self, value: int) -> None:
        self._end = value
    
    @property
    def is_blank(self) -> bool:
        return self._is_blank
    
    @is_blank.setter
    def is_blank(self, value: bool) -> None:
        self._is_blank = value

    def __init__(self, start: int, end: int, is_blank: bool) -> None:
        self.start: int = start
        self.end: int = end
        self.is_blank: bool = is_blank

    def __str__(self):
        return f"start: {self.start}, end: {self.end}, height: {self.height}, Blank: {self.is_blank}"

    def get_StartEnd(self) -> Tuple[int, int]:
        return (self._start, self._end)
    
    def _is_fit_in(self, height: int) -> bool:
        """ Return True if the panel is fit in the column.  
        [1% max height] is not noticeable when stretching """
        return self.height <= height * 101 // 100
    
    def split(self, page_height: int, requested_height: int) -> List[Tuple[int, int]]:
        """ 
        Split the panel into two smaller parts, and return the start and end of each part

        Parameters
        ----------
        page_height: int
            The height of the page (maximum height of a panel)

        requested_height: int
            The requested height of the first panel

        Returns
        -------
        List[Tuple[int, int]]
            The [start] and [end] of each part

        """
        # no need to split blank panel (maybe this is not necessary)
        if self.is_blank:
            raise ValueError(f"Split blank panel: {self}")
        
        if self.height <= requested_height:
            raise ValueError(f"Cannot split - Height: {self.height}, Requested Height: {requested_height}")
        
        out: List[Tuple[int, int]] = []
        height: int = requested_height

        while self.height > (page_height * SPLITABLE_PERCENTAGE // 100):
            # only take the last part if it is not too small (2%)
            out.append((self._start, split_p := self._start + height))
            self.start = split_p
            height = min(page_height, self.height)

        return out


class PageColumn:
    def __init__(self, panels: List[PanelSection]) -> None:
        self.content_num: int = 0
        self.content: int = 0
        self.blank_num: int = 0
        self.blank: int = 0
        self.panels: List[PanelSection] = panels
        for panel in self.panels:
            if panel.is_blank:
                self.blank_num += 1
                self.blank += panel.height
            else:
                self.content_num += 1
                self.content += panel.height

    @property
    def content(self) -> int:
        return self._content
    
    @content.setter
    def content(self, value: int) -> None:
        self._content = value

    @property
    def content_num(self) -> int:
        return self._content_num
    
    @content_num.setter
    def content_num(self, value: int) -> None:
        self._content_num = value

    @property
    def blank(self) -> int:
        return self._blank

    @blank.setter
    def blank(self, value: int) -> None:
        self._blank = value

    @property
    def blank_num(self) -> int:
        return self._blank_num
    
    @blank_num.setter
    def blank_num(self, value: int) -> None:
        self._blank_num = value

    def __str__(self) -> str:
        return f"Total Content: {self.content_num} - Height: {self.content}, Total Blank: {self.blank_num} - Height: {self.blank}"
    
    def clear(self) -> None:
        self.panels = []
        self.content_num = 0
        self.content = 0
        self.blank_num = 0
        self.blank = 0

    def is_StartwBlank(self) -> bool:
        """
        Return
        ------
        bool 
            True if first panel is blank
        """
        return self.panels[0].is_blank if self.panels else False

    def is_EndwBlank(self) -> bool:
        """
        Return
        ------
        bool 
            True if last panel is blank
        """
        return self.panels[-1].is_blank if self.panels else False
    
    def is_StartwContent(self) -> bool:
        """
        Return
        ------
        bool 
            True if first panel is not blank
        """
        return not self.panels[0].is_blank if self.panels else False
    
    def is_EndwContent(self) -> bool:
        """
        Return
        ------
        bool 
            True if last panel is not blank
        """
        return not self.panels[-1].is_blank if self.panels else False


class PageColumnTemp(PageColumn):
    def __init__(self, panels: List[PanelSection] | None = None, max_height: int = 0) -> None:
        _panels: List[PanelSection] = [] if panels is None else panels
        super().__init__(_panels)
        self._height_max: int = max_height
        self._is_full: bool = False
        self.last_blank = ()

    @property
    def height_max(self) -> int:
        return self._height_max

    @property
    def is_full(self) -> bool:
        return self._is_full

    @property
    def last_blank(self) -> Tuple:
        return self._last_blank
    
    @last_blank.setter
    def last_blank(self, value: Tuple) -> None:
        self._last_blank = value

    def _is_fit(self, p: PanelSection) -> bool:
        """ Return True if the panel is fit in the column.  
        Slightly over 100%, this is aceptable and is not noticeable when stretching """
        return (self.content + p.height) <= (self.height_max * MAX_PERCENT_HEIGHT // 100)

    def append_Panel(self, panel: PanelSection) -> None:
        if panel.is_blank:
            self.blank_num += 1
            self.blank += panel.height
        else:
            self.content_num += 1
            self.content += panel.height
        self.panels.append(panel)
    
    def _cal_cut_request(self, panel: PanelSection) -> int:
        """
        This func is call only when panel height is larger than free space, it contains all the logic to evaluate that is can be trim or not.
        - If current column not have any content, then force to split the panel
        - If current column is almost full, no need to squeeze in more panel.
        - Panel will NOT be split if is height is about 90% of a page.
        - When current column content have less than LOW_CONTENT_PERCENTAGE, force panel to split
        - When current column have more than 3 panels, no need to squeeze in more panel
        - Panel is considered to be splitable when, if panel is slightly larger that SPLITABLE_PERCENTAGE, then we can cut it a little bit.
        - BUT when panel is lightly larger that SPLITABLE_PERCENTAGE, we can cut a little bit of the top panel to make it fit.
        """
        if (self.height_max * 9 // 10) <= self.content \
        or (self.height_max * 9 // 10) <= panel.height <= self.height_max:
            return 0
        
        free_space: int = self.height_max - self.content
        if self.content < (self.height_max * LOW_CONTENT_PERCENTAGE // 100):
            # force to split panel if current column is too short
            return free_space
        
        if self.content_num >= 3:
            # 3 panels is enough in most cases
            return 0

        cut_amount: int = (panel.height - free_space)
        if cut_amount < (self.height_max * SPLITABLE_PERCENTAGE // 100):
            return free_space

        if (cut_amount := cut_amount // 2) < (self.height_max * SPLITABLE_PERCENTAGE // 100) \
        and self.content_num > 0: # need at least one content panel
            for p in self.panels: # trim the top panel of column
                if p.is_blank:
                    continue
                p.start += cut_amount
                self.content -= cut_amount
                break
            free_space += cut_amount
            return free_space

        return 0

    def add_Panel(self, panel: PanelSection) -> List[PageColumn]:
        """
        This will try add panel to column. When panel is a blank panel, or it fit in, this will be add.  
        If not, we will evaluate if we can trim a little bit to make it fit.  
        If still not, then we will just output the current column and make a new one. And in the new column, if it still not fit (that happen when we have a long long panel), we will split the panel to make it fit.

        Args:
            panel (PanelSection): Panel to add

        Returns:
            List[PageColumn]: List of columns if panel can't fit in current column.  
            NOTE: When list is empty, then add success. No need to do anything.
        """
        output: List[PageColumn] = []
        if panel.is_blank or (not panel.is_blank and self._is_fit(panel)):
            self.append_Panel(panel)
            return output

        if not (request_cut := self._cal_cut_request(panel)):
            output.append(self._on_Full())
            if self._is_fit(panel):
                self.append_Panel(panel)
                return output
            request_cut = self.height_max # TODO: maybe evaluate to get better size. (ex. don't cut text..)

        panels_splited = panel.split(self.height_max, request_cut)
        for p in panels_splited:
            self.append_Panel(PanelSection(p[0], p[1], False))
            if p != panels_splited[0] and p == panels_splited[-1]:
                continue # everything except last one
            output.append(self._on_Full())
        return output
    
    def _on_Full(self) -> PageColumn:
        self._set_LastBlank()
        ret: PageColumn = PageColumn(self.evaluate())
        self.clear()
        if self.last_blank:
            self.add_Panel(PanelSection(self.last_blank[0], self.last_blank[1], True))
        return ret

    def _fill_EndwBlank(self, color: str = "white") -> None:
        """ This is unusual case, when need to fill the rest of column with blank panel """
        height: int = self.height_max - self.content
        self.blank_num += 1
        self.blank += height
        match color:
            case "white":
                _co = PAD_WHITE
            case _:
                _co = PAD_BLACK
        self.panels.append(PanelSection(_co, height, True))

    def _set_LastBlank(self) -> None:
        """
        If the column end with blank panel, split it in half.  
        Use first half to end current column and store the second half to start next column.
        """
        if self.is_EndwBlank():
            start, end = self.panels[-1].get_StartEnd()
            mid_point = (start + end) // 2
            self.panels[-1].end = mid_point
            self.last_blank = (mid_point + 1, end)
        else:
            self.last_blank = ()

    def remove(self, index: int) -> PanelSection:
        if self.panels[index].is_blank:
            self.blank_num -= 1
            self.blank -= self.panels[index].height
        else:
            self.content_num -= 1
            self.content -= self.panels[index].height
        return self.panels.pop(index)

    def rem_AllBlank(self) -> None:
        """
        Remove all blank panels in the column
        """
        self.panels = [panel for panel in self.panels if not panel.is_blank]
        self.blank_num = 0
        self.blank = 0
    
    def rem_BlankTop(self) -> PanelSection | None:
        """
        If column start with blank panel, remove it

        Returns
        -------
        PanelSection | None
            The removed panel
        """
        return self.remove(0) if self.is_StartwBlank() else None
    
    def rem_BlankBottom(self) -> PanelSection | None:
        """
        If column end with blank panel, remove it

        Returns
        -------
        PanelSection | None
            The removed panel
        """
        return self.remove(-1) if self.is_EndwBlank() else None

    def _get_ColumnMap(self) -> List[bool]:
        """
        Get types of panels in the column in sequential order

        Returns
        -------
        List[bool]
            List of panel types with no duplicates
        """
        map: List[bool] = [True if self.panels[0].is_blank else False]
        if len(self.panels) > 1:
            for i in range(1, len(self.panels)):
                if is_blank := self.panels[i].is_blank != map[-1]:
                    map.append(is_blank)
        return map

    def evaluate(self, last_column: bool = False) -> List[PanelSection]:
        """
        Contains all the rules to evaluate output the column.  
        Clear any panels that are not needed, or add more if needed.

        Returns
        -------
        List[PanelSection]
            List of panels that can be use for creating a final column
        """
        if self.content_num < 1:
            raise ValueError(f"No content found in this column: {self.panels[0].start}->{self.panels[-1].end}")

        if self.content > (self.height_max * 995 // 1000):
            # really close to page height
            self.rem_AllBlank()
            return self.panels
        
        if not last_column:
            if self.content > (self.height_max * FINAL_CONTENT_PERCENTAGE // 100):
                # enough content panel in the column, remove blank panel on top and bottom to make panel space out.
                if len(map := self._get_ColumnMap()) > 3:
                    if map[-1]:
                        self.rem_BlankBottom()
                    if map[0]:
                        self.rem_BlankTop()

            # else: # TODO: MAYBE ADD SOMETHING ELSE HERE

        else: # for the last column, handle a bit differently
            if self.is_StartwBlank() and self.is_EndwContent():
                self.append_Panel(self.panels[0])

        if self.blank_num < 1:
            # if not enough content panel in the last column, the image will be stretch. Add white panel to make it fit. But because this is only contain coordinate for extract the source image, we cannot directly add white panel here. This just add a fake blank panel. Output func will handle the regeneration.
            self._fill_EndwBlank("white")

        return self.panels
