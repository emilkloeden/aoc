from importlib.machinery import SourceFileLoader
from pathlib import Path


class Runner:
    def __init__(self, part: int):
        self._p = Path().absolute()
        python_file = self._p / "day.py"
        if python_file.exists() and python_file.is_file():
            day = SourceFileLoader('day', str(python_file.resolve())).load_module()
            answer = day.part_1() if part == 1 else day.part_2()
            print(f"Part {part}: {answer}")

        