import argparse
import logging
from importlib.machinery import SourceFileLoader
from pathlib import Path

from dotenv import load_dotenv

from aoc.utils import derive_language, get_default_year

load_dotenv()

"""
aoc init . --year 2022 --language python
aoc get .
aoc run [1,2]
aoc submit [1,2]
"""



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    init_parser = subparsers.add_parser('init', help='Initialise an advent of code project/folder.')
    
    init_parser.add_argument('location', type=str, help="where to scaffold project.", default=".")
    init_parser.add_argument('--year', type=int, default=get_default_year())
    init_parser.add_argument('--language', choices=('python', 'java', 'javascript'), default='python')

    get_parser = subparsers.add_parser('get', help="Get input file, requires AOC_SESSION environment variable.")
    get_parser.add_argument('--location', type=str, help="Which input to download and where", default=".")
    
    run_parser = subparsers.add_parser('run', help="execute a part processor in the current directory.")
    run_parser.add_argument('part', type=int, choices=(1,2))

    submit_parser = subparsers.add_parser('submit', help="Submit an answer, requires AOC_SESSION environment variable.")
    submit_parser.add_argument('part', type=int, choices=(1,2))

    open_parser = subparsers.add_parser('open', help="Submit an answer, requires AOC_SESSION environment variable.")

    

    return parser.parse_args()


def is_init_valid(args) -> bool:
    max_year = get_default_year()
    if args.year < 2015 or args.year > max_year:
        raise ValueError(f"Year must be between 2015 and {max_year} (inclusive).")

    return True


def __load_plugin(language: str):
    dir_path = Path(__file__).parent
    plugins_dir = dir_path / "plugins"
    language_dir = plugins_dir / language
    try:
        return SourceFileLoader('module', str(language_dir.resolve())).load_module()
    except PermissionError:
        return SourceFileLoader('module', str((language_dir / "__init__.py").resolve())).load_module()


def handle_init(year: int, language: str, location: Path) -> None:
    """Given {year}, {language} and {location}, scaffolds out a project
    in accordance with the Initialiser class of the respective {language} plugin.

    Args:
        year (int): _description_
        language (str): _description_
        location (Path): _description_
    """
    module = __load_plugin(language)
    i = module.Initialiser(year, location)
    i.initialise()

    
def handle_get(location: Path=None) -> None:
    """Derives year and day from {location}, downloads input to {location}/input.txt

    Args:
        location (Path): Directory
    """
    if location is None:
        location = Path()
    derived_language = derive_language(location)
    module = __load_plugin(derived_language)
    g = module.Getter(location)
    g.get_input()


def handle_run(part: int) -> None:
    derived_language = derive_language()
    module = __load_plugin(derived_language)
    r = module.Runner(part)
    r.run()


def handle_submit(part: int) -> None:
    derived_language = derive_language()
    module = __load_plugin(derived_language)
    s = module.Submitter(part)   
    s.submit()


def handle_open() -> None:
    derived_language = derive_language()
    module = __load_plugin(derived_language)
    o = module.Opener()
    o.open()


def main() -> None:
    args = parse_args()
    logging.debug(args)
    if args.command == "init":
        if (args):
            handle_init(args)
        else:
            raise ValueError(f"Invalid arguments supplied to 'init' sub-command.")
    elif args.command == "get":
        handle_get(args.location)
    elif args.command == "run":
        handle_run(args.part)

    elif args.command == "submit":
        handle_submit(args.part)
    elif args.command == "open":
        handle_open()

    else:
        raise ValueError(f"Invalid command {args.command} supplied.")
    

if __name__ == "__main__":
    main()