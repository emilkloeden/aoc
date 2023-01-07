from pathlib import Path
import subprocess

class Runner:
    def __init__(self, part: int):
        self._p = Path().absolute()
        self.module = None
        self.part = part
        javascript_file = self._p / "day.js"
        if javascript_file.exists() and javascript_file.is_file():
            self.module = javascript_file
            
    def run(self) -> None:
        if self.module:
            answer = subprocess.check_output(['node', self.module.resolve(), f"{self.part}"])
            print(f"Part {self.part}: {answer.decode().strip()}")
        else:
            raise AttributeError(f"Unable to run, perhaps it was unable to find 'day.js' within {self._p}.")

        