import os
import requests
from importlib.machinery import SourceFileLoader
from pathlib import Path
from validations import is_valid_day, is_valid_language, is_valid_year

class Submitter:
    def __init__(self, part: int):
        self._p = Path().absolute()
        self.part = part
        self.day: int = None
        self.year: int = None
        self.language: str = None
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
            self.location = self._p / "day.py"
            self.submit_answer()
        else:
            raise ValueError(f"Unable to ascertain required info 'year', 'language' and 'day' from path: {self._p.absolute()}")
        

    def submit_answer(self):
        python_file = self.location
        if python_file.exists() and python_file.is_file():
            day = SourceFileLoader('day', str(python_file.resolve())).load_module()
            answer = day.part_1() if self.part == 1 else day.part_2()
            if answer:
                session_cookie = os.environ['AOC_SESSION']
                
                url = f"https://adventofcode.com/{self.year}/day/{self.day}/answer"
                cookies = dict(session=session_cookie)
                headers = {"User-Agent": "github.com/emilkloeden/aoc"}
                data = {
                    "submit": "[Submit]",
                    "answer": answer,
                    "level": self.part
                }
                r = requests.post(url, data=data, cookies=cookies, headers=headers)
                if r.status_code == 200:
                    if "That's the right answer!" in r.text:
                        print(f"[*] Your answer to part {self.part} ({answer}) was correct!")
                    else:
                        print(f"[-] That probably wasn't correct, see ressponse below\n")
                        print(r.text)
                else:
                    print(f"[!] {r.status_code} status code returned.")
            else:
                print("[!] No answer returned from part {part}.")

        