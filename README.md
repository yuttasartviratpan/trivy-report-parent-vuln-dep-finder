## Setup Instruction
```
poetry install
```

## Run Test
```
poetry run pytest
```

## What to do next

### Install Pre-commit (Recommended)
```
poetry run pre-commit install
```
If you wish to edit pre-commit behavior see ```.pre-commit-config.yaml```.
Normally it checks only the file you are committing. But if you wish to run it manually for all files do
```
poetry run pre-commit run --all
```

### Adjusting the Dependencies
edit pyproject.toml or just do
```
poetry add numpy
```
or for dev dependencies
```
poetry add --dev numpy
```
See [python-poetry.org](https://python-poetry.org/)

### Change Pytest, Flake, Coverage Setting
See ```tox.ini```

### Change how sonarqube behaves.
See ```sonar-project.properties```

### Get Pycharm to show the correct coverage
Ironically in pycharm test configuration add `--no-cov` to `Additional Arguments` this turn off pytest-cov coverage and uses Pycharm's own pytest.

### ----------------------------------------------------------------------------

### Parent Dependency Vulnerability Scanning by reading Trivy's report (JSON).
This project reads a report produced by Trivy, the security scanner.
This project currently can only read the json format report, and CycloneDX format report, which is also in json...

## Instruction
First we need to build the project into a binary executables. Run
```
poetry install
```
To install the most important builder, pyinstaller.

After installing the packages, run either:
```
# This format
# poetry run pyinstaller --onefile <path to this project src/main.py>

poetry run pyinstaller --onefile ./src/trivy_script_project/main.py
```

or

```
# This format
# pyinstaller --onefile <path to this project src/main.py>

pyinstaller --onefile ./src/trivy_script_project/main.py
```

depending on whether you have pyinstaller on your computer or not.

After successfully run the program, hopefully, an executable called ```main.exe```
should appear in ```/dist/main.exe```.

After you got the executable, all you have to do is to run it with a report
file as an argument input, like this:
```
./dist/main.exe <The path to your report in .json>
```

Ex:
```
# Windows
.\dist\main.exe "C:\Users\<username>\Desktop\report.json"

# Linux
./dist/main.exe "~/Desktop/report.json"
```
