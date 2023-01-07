from importlib.machinery import SourceFileLoader
from pathlib import Path


class Runner:
    def __init__(self, part: int):
        self._p = Path().absolute()
        self.module = None
        self.part = part
        python_file = self._p / "day.py"
        if python_file.exists() and python_file.is_file():
            self.module = SourceFileLoader('day', str(python_file.resolve())).load_module()
            
    def run(self) -> None:
        if self.module:
            answer = self.module.part_1() if self.part == 1 else self.module.part_2()
            print(f"Part {self.part}: {answer}")
        else:
            raise AttributeError(f"Unable to run, perhaps it was unable to find 'day.py' within {self._p}.")

        