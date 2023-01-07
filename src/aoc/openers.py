import webbrowser
from pathlib import Path

from aoc.validations import is_valid_day, is_valid_language, is_valid_year


class Opener:
    def __init__(self):
        self._p = Path().absolute()
        self.day: int = None
        self.year: int = None
        self.language: str = None
        # These are arguably invalid here but I like the consistency
        if is_valid_day(self._p.name):
            self.day = int(self._p.name)
        for x in self._p.parents:
            if is_valid_day(x.name):
                self.day = int(x.name)
                continue
            if is_valid_language(x.name) and is_valid_year(x.parent.name):
                self.year = int(x.parent.name)
                self.language = x.name
                break

        if (self.day and self.year and self.language):
            self.url = f"https://adventofcode.com/2022/day/{self.day}"
            webbrowser.open(self.url)
        else:
            raise ValueError(f"Unable to ascertain required info 'year', 'language' and 'day' from path: {self._p.absolute()}")
        