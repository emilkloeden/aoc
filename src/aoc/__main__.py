import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv
from aoc.getters import Getter
from aoc.runners import Runner
from aoc.submitters import Submitter
from aoc.initialisers import (JavaInitialiser, JavaScriptInitialiser,
                          PythonInitialiser)
from aoc.openers import Opener

from aoc.utils import get_default_year

load_dotenv()
days = list(range(1, 26))

"""
aoc init . --year 2022 --language python
aoc get .
aoc run [1,2]
aoc submit [1,2]
"""



def parse_args():
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

def handle_init_javascript(args):
    raise NotImplementedError

def handle_init_java(args):
    raise NotImplementedError

def handle_init_python(args):
    base_dir = Path(args.location)

def handle_init(args):
    language_handlers = {
        "python": PythonInitialiser,
        "java": JavaInitialiser,
        "javascript": JavaScriptInitialiser
    }
    return language_handlers[args.language](args.year, args.location).initialise()

def handle_get(args):
    Getter(Path(args.location))

def handle_run(args):
    Runner(args.part)

def handle_submit(args):
    Submitter(args.part)   

def handle_open():
    Opener()

def main():
    args = parse_args()
    logging.debug(args)
    if args.command == "init":
        if is_init_valid(args):
            handle_init(args)
        else:
            raise ValueError(f"Invalid arguments supplied to init command.")
    elif args.command == "get":
        handle_get(args)
    elif args.command == "run":
        handle_run(args)

    elif args.command == "submit":
        handle_submit(args)
    elif args.command == "open":
        handle_open()

    else:
        raise ValueError(f"Invalid command {args.command} supplied.")
    

if __name__ == "__main__":
    main()