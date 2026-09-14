import json
from pathlib import Path

from .config import DAYS

DATA_FILE = Path("revision_planner_data.json")


def default_data():
    return {
        "subjects": {},
        "option_subjects": [],
        "school_timetable": {day: [] for day in DAYS[:5]},
    }


def load_data():
    if not DATA_FILE.exists():
        return default_data()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            loaded = json.load(file)

        data = default_data()
        data.update(loaded)

        for day in DAYS[:5]:
            data["school_timetable"].setdefault(day, [])

        return data
    except (json.JSONDecodeError, OSError):
        return default_data()


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError:
        return False
    return True


def time_to_minutes(time_text):
    hours, minutes = map(int, time_text.split(":"))
    return hours * 60 + minutes


def minutes_to_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def valid_time(time_text):
    try:
        hours, minutes = map(int, time_text.split(":"))
        return 0 <= hours <= 23 and 0 <= minutes <= 59
    except ValueError:
        return False


def overlaps(start_a, end_a, start_b, end_b):
    a_start = time_to_minutes(start_a)
    a_end = time_to_minutes(end_a)
    b_start = time_to_minutes(start_b)
    b_end = time_to_minutes(end_b)
    return a_start < b_end and b_start < a_end
