from .config import OPTION_SUBJECTS


def subject_is_option(name):
    simplified = name.strip().lower()
    if simplified.startswith("gcse "):
        simplified = simplified[5:]
    if simplified.startswith("btec level 2 tech award in "):
        simplified = simplified[len("btec level 2 tech award in "):]
    if simplified.startswith("level 2 cambridge national "):
        simplified = simplified[len("level 2 cambridge national "):]

    normalized = {
        item.strip().lower().replace("gcse ", "").replace(
            "btec level 2 tech award in ", ""
        ).replace("level 2 cambridge national ", "")
        for item in OPTION_SUBJECTS
    }
    return simplified in normalized


def option_subject_count(data):
    return len(data.get("option_subjects", []))
