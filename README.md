# pppActivityTracker

Python tkinter GUI app to manage activity tracking for people.

## Description

For fun, ppp stands for Paul Painter Python. pppActivityTracker is a simple GUI
App to enter activities in a log with a start and stop time, a short descriptor
of an activity and additional notes. The duration of the activity in minutes
is computed. Weekly summaries of the activities can be shown.

The data is stored in a local json file.

An approximation of the MVVM pattern is employed.

## Project Structure

```txt
pppActivityTracker (project root)
│
├── model/
│   ├── ae.py (ActivityEntry dataclass)
│   └── tbd/
│
├── tests/
│   ├── test_ae.py (unit test for ActivityEntry dataclass)
│   └── package2/
|
├── README.md
├── requirements.txt
└── main.py (The program main)
```

## Dependencies

Periodically capture the dependent python packages with:

`pip freeze > requirements.txt`

To update the dependent python modules, use the command:

`pip install --upgrade -r requirements.txt`
