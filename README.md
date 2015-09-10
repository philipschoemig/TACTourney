TACTourney
=========

A tournament management software for the board game [TAC](http://www.spieltac.de). It is based on the lightweight web application framework [Flask](http://flask.pocoo.org/) for Python.

## Prerequisites

- Install [Python](https://www.python.org/)
- Install [pip](https://pip.pypa.io/)
- Install [Virtualenv](https://virtualenv.pypa.io/) with pip:
```
pip install virtualenv
```

## Installation

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
*If you get the error message "mysql_config not found" you need to install additional mysql tools. For Debian-based Linux distributions install the package libmysqlclient-dev.*
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

## Links

- [Code Climate](https://codeclimate.com/github/philipschoemig/TACTourney)
- [Travis CI](https://travis-ci.org/philipschoemig/TACTourney)
- [Pivotal Tracker](https://www.pivotaltracker.com/projects/1339060)

## Status

[![Code Climate](https://codeclimate.com/github/philipschoemig/TACTourney/badges/gpa.svg)](https://codeclimate.com/github/philipschoemig/TACTourney)
[![Build Status](https://travis-ci.org/philipschoemig/TACTourney.svg)](https://travis-ci.org/philipschoemig/TACTourney)
