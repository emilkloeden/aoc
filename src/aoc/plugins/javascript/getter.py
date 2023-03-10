import os
from pathlib import Path

import requests
from aoc.validations import is_valid_day, is_valid_year
from .local_validations import is_valid_language


class Getter:
    def __init__(self, p: Path=None):
        self.day: int = None
        self.year: int = None
        self.language: str = None
        if p is None:
            p = Path()
        self._p = p.absolute()
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
            self.location = self._p / "input.txt"
        else:
            raise ValueError(f"Unable to ascertain required info 'year', 'language' and 'day' from path: {p.absolute()}")

    def get_input(self):
        try:
            session_cookie = os.environ['AOC_SESSION']
            
            url = f"https://adventofcode.com/{self.year}/day/{self.day}/input"
            cookies = dict(session=session_cookie)
            headers = {"User-Agent": "github.com/emilkloeden/aoc"}
            
            r = requests.get(url, cookies=cookies, headers=headers)
            self.location.write_text(r.text)
        except KeyError:
            print("[!] Unable to get input, AOC_SESSION environment variable not set")
        except AttributeError:
            print("[!] Unable to save input, perhaps location was not set/set incorrectly")