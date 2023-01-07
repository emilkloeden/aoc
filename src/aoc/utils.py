from datetime import datetime
from pathlib import Path
import aoc.validations as validations

from importlib.machinery import SourceFileLoader

# from aoc.validations import is_valid_day, is_valid_year

REQUIRED_ATTRS_IN_PLUGIN = {
    "Initialiser",
    "Getter",
    "Submitter",
    "Runner",
    "Opener",
}


def discover_languages() -> list[str]:
    p = Path(__file__).parent
    plugins_dir = p / "plugins"
    contents = plugins_dir.glob("*")
    
    dirs = [d for d in contents if d.is_dir()]
    plugins = []
    for d in dirs:
        try:
            module = SourceFileLoader('module', str(d.resolve())).load_module()
            if all([module.hasattr(attr) for attr in REQUIRED_ATTRS_IN_PLUGIN]):
                plugins.append(d.name)
            
        except PermissionError:
            try:
                init_file = d / "__init__.py"
                module = SourceFileLoader('module', str(init_file.resolve())).load_module()
                if all([hasattr(module, attr) for attr in REQUIRED_ATTRS_IN_PLUGIN]):
                    plugins.append(d.name)
            except NotImplementedError:
                raise

    return plugins

def get_default_year():
    now = datetime.today()
    return now.year if now.month == 12 else now.year-1

def derive_language(location: Path=None):
    if location is None:
        location = Path()
    p = location.absolute()
    if validations.is_valid_day(p.name):
        for x in p.parents:
            if validations.is_valid_day(x.name):
                continue
            if is_valid_language(x.name) and validations.is_valid_year(x.parent.name):
                language = x.name
                return language
    raise ValueError(f"Unable to derive language from path: {p.resolve()}")

def is_valid_language(language: str):
    plugin_languages = discover_languages()
    return language in plugin_languages 