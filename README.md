TACTourney
=========

A tournament management software for the board game [TAC](http://www.spiel-tac.de). It is based on the lightweight web application framework [Flask](http://flask.pocoo.org/) for Python.

## Installation

- Install [Python](https://www.python.org/) and [pip](https://pip.pypa.io/)
- Install [Virtualenv](https://virtualenv.pypa.io/):
```
pip install virtualenv
```
- Retrieve the source code from GitHub
- Change into the project directory (where this README.md file is located)
- Create a virtual environment for Python:
```
virtualenv .venv
```
- Activate the virtual environment:
```
source .venv/bin/activate
```
- Install the project requirements with pip:
```
pip install -r requirements.txt
```
- Deactivate the virtual environment:
```
deactivate
```

## Configuration

- Change into the project directory (where this README.md file is located)
- Activate the virtual environment:
```
source .venv/bin/activate
```
- Change into the subdirectory src/tourney
- Execute the manage.py script with argument setup and follow the instructions:
```
python manage.py setup
```
- Deactivate the virtual environment:
```
deactivate
```
