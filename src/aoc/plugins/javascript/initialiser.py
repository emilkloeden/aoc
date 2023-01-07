from pathlib import Path
from typing import Protocol

class InitialiserProtocol(Protocol):
    def initialise(self):
        pass

    def mkdirs(self):
        pass

    def write_file_templates(self):
        pass

class Initialiser(InitialiserProtocol):
    def __init__(self, year: int, location:Path=None):
        self.language = "javascript"
        self.year = year
        if location is None:
            location = Path()
        self.location = Path(location) / f"{self.year}" / self.language

        self.file_content = '''const fs = require('fs');
const path = require('fs');

const PROD = false


function loadInput() { 
    return fs.readFileSync("./input.txt");
}
const TEST_INPUT = ``

const INPUT = PROD ? loadInput() : TEST_INPUT;


function part1() {
    throw Error("NotImplemented");
}

function part2() {
    throw Error("NotImplemented");
}


function main() {
    const part = process.argv.slice(2);
    console.log(process.argv.pop())
    const parts = {
        '1': part1,
        '2': part2,
    }
    console.log(`Day: XXDAYXX Part: ${part}`);
    console.log(parts[part]());
}
main();
'''

    def initialise(self):
        print("[+] Scaffolding project...")
        self.mkdirs()
        self.mkdotenv()
        self.write_file_templates()
        print("[+] ...Done.")

    def mkdotenv(self):
        dotenv_path = self.location / ".env"
        dot_env_contents = """# AOC Environment Variables
#AOC_SESSION= # Required to download input files
"""
        dotenv_path.write_text(dot_env_contents)

    def mkdirs(self):
        try:
            self.location.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print(f"{self.location.absolute()} exists, ignoring...")
        for i in range(1, 26):
            try:
                subdir = self.location / f"{i:02}"
                subdir.mkdir(exist_ok=False)
            except FileExistsError:
                print(f"{subdir.absolute()} exists, ignoring...")


    def write_file_templates(self):
        for i in range(1, 26):
            daily_file: Path = self.location / f"{i:02}" / "day.js"
            daily_file.write_text(self.file_content.replace("XXDAYXX", f"{i}"))
        

