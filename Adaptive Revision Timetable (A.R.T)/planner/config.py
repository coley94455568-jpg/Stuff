DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

CORE_SUBJECTS = [
    "English",
    "Maths",
    "Biology",
    "Chemistry",
    "Physics",
    "R.E.",
    "Religious Education",
]

COMMON_SUBJECTS = CORE_SUBJECTS + [
    "Photography",
    "Computer Science",
    "Geography",
    "History",
    "P.E.",
    "R.E.",
    "Religious Education",
]

OPTION_SUBJECTS = [
    "Geography",
    "History",
    "GCSE Geography",
    "GCSE History",
    "French/Spanish",
    "GCSE French/Spanish",
    "Computer Science",
    "GCSE Computer Science",
    "Creative iMedia (ICT)",
    "Level 2 Cambridge National Creative iMedia (ICT)",
    "Art & Design",
    "GCSE Art & Design",
    "Photography",
    "GCSE Photography",
    "Business",
    "GCSE Business",
    "Drama",
    "GCSE Drama",
    "Food Preparation & Nutrition",
    "GCSE Food Preparation & Nutrition",
    "Design & Technology: Papers & Boards",
    "GCSE Design & Technology: Papers & Boards",
    "Design & Technology: Timbers",
    "GCSE Design & Technology: Timbers",
    "Media",
    "GCSE Media",
    "Music",
    "GCSE Music",
    "Physical Education",
    "GCSE Physical Education",
    "Sport",
    "BTEC Level 2 Tech Award in Sport",
    "Health and Social",
    "BTEC Level 2 Tech Award in Health and Social",
]

OPTION_SUBJECT_LIMIT = 2

# School timings
SCHOOL_START = "8:40"
SCHOOL_END = "15:00"
HOME_TIME = "15:30"
BREAK_START = "15:30"
BREAK_END = "16:00"
DINNER_START = "18:00"
DINNER_END = "20:00"
REVISION_END = "21:00"

WEEKDAY_REVISION_SLOTS = [
    ("16:00", "17:00"),
    ("17:00", "18:00"),
    ("20:00", "21:00"),
]

WEEKEND_REVISION_SLOTS = [
    ("10:00", "11:00"),
    ("11:00", "12:00"),
    ("12:00", "13:00"),
    ("14:00", "15:00"),
    ("15:00", "16:00"),
    ("16:00", "17:00"),
    ("17:00", "18:00"),
    ("20:00", "21:00"),
]

SCHOOL_PERIODS = [
    ("Tutor", "08:40", "09:00"),
    ("P1", "09:00", "10:00"),
    ("P2", "10:00", "11:00"),
    ("Break", "11:00", "11:20"),
    ("P3", "11:20", "12:20"),
    ("P4", "12:20", "13:20"),
    ("Lunch", "13:20", "14:00"),
    ("P5", "14:00", "15:00"),
]

PERIOD_ORDER = [period for period, _, _ in SCHOOL_PERIODS]

TEACHING_PERIODS = {
    period: (start, end)
    for period, start, end in SCHOOL_PERIODS
    if period not in {"Break", "Lunch", "Tutor"}
}
TEACHING_PERIODS["Tutor"] = ("08:40", "09:00")
TEACHING_PERIODS["Break"] = ("11:00", "11:20")
TEACHING_PERIODS["Lunch"] = ("13:20", "14:00")
