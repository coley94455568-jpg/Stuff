import tkinter as tk
from tkinter import ttk, messagebox

from .config import (
    DAYS,
    CORE_SUBJECTS,
    COMMON_SUBJECTS,
    OPTION_SUBJECTS,
    SCHOOL_PERIODS,
    PERIOD_ORDER,
    TEACHING_PERIODS,
    WEEKDAY_REVISION_SLOTS,
    WEEKEND_REVISION_SLOTS,
)
from .data import (
    load_data,
    save_data,
    time_to_minutes,
    minutes_to_time,
)
from .subjects import subject_is_option, option_subject_count


def make_app():
    data = load_data()

    root = tk.Tk()
    root.title("GCSE Adaptive Revision Planner")
    root.geometry("1150x760")
    root.minsize(1000, 650)

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    main = ttk.Frame(root, padding=15)
    main.pack(fill="both", expand=True)

    title = ttk.Label(
        main,
        text="GCSE Adaptive Revision Planner",
        font=("Segoe UI", 23, "bold"),
    )
    title.pack(anchor="w")

    subtitle = ttk.Label(
        main,
        text="Enter your school timetable, then let the planner adapt revision around it.",
        font=("Segoe UI", 11),
    )
    subtitle.pack(anchor="w", pady=(0, 12))

    notebook = ttk.Notebook(main)
    notebook.pack(fill="both", expand=True)

    # Tab 1: subjects
    scores_tab = ttk.Frame(notebook, padding=12)
    notebook.add(scores_tab, text="Subjects & Scores")

    left = ttk.Frame(scores_tab)
    left.pack(side="left", fill="y", padx=(0, 15))

    ttk.Label(left, text="Add subject").pack(anchor="w")
    subject_entry = ttk.Entry(left, width=30)
    subject_entry.pack(fill="x", pady=(3, 8))

    ttk.Label(left, text="Current score (%)").pack(anchor="w")
    score_entry = ttk.Entry(left, width=30)
    score_entry.pack(fill="x", pady=(3, 10))

    buttons = ttk.Frame(left)
    buttons.pack(fill="x", pady=(0, 10))

    def add_subject():
        name = subject_entry.get().strip()
        if not name:
            messagebox.showerror("Missing subject", "Enter a subject name.")
            return

        try:
            score = float(score_entry.get())
            if not 0 <= score <= 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid score", "Enter a score between 0 and 100.")
            return

        if name in data["subjects"]:
            messagebox.showwarning(
                "Already exists",
                "That subject already exists. Select it and update its score.",
            )
            return


        data["subjects"][name] = {"score": score, "history": [score]}
        save_data(data)
        subject_entry.delete(0, tk.END)
        score_entry.delete(0, tk.END)
        refresh_subjects()

    def update_score():
        selected = subject_tree.selection()
        if not selected:
            messagebox.showwarning("Select a subject", "Select a subject before updating its score.")
            return

        name = subject_tree.item(selected[0], "values")[0]
        try:
            score = float(score_entry.get())
            if not 0 <= score <= 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid score", "Enter a score between 0 and 100.")
            return

        data["subjects"][name]["score"] = score
        data["subjects"][name].setdefault("history", []).append(score)
        save_data(data)
        refresh_subjects()
        score_entry.delete(0, tk.END)
        messagebox.showinfo(
            "Score updated",
            f"{name} is now {score:.1f}%.\n\nGenerate a new timetable for the change to take effect.",
        )

    def delete_subject():
        selected = subject_tree.selection()
        if not selected:
            messagebox.showwarning("Select a subject", "Select a subject first.")
            return

        name = subject_tree.item(selected[0], "values")[0]
        if messagebox.askyesno("Delete subject", f"Delete {name} and its score history?"):
            del data["subjects"][name]
            if name in data.get("option_subjects", []):
                data["option_subjects"] = [x for x in data["option_subjects"] if x != name]
            save_data(data)
            refresh_subjects()

    def refresh_subjects():
        for item in subject_tree.get_children():
            subject_tree.delete(item)

        for name, info in sorted(data["subjects"].items()):
            score = info["score"]
            history = info.get("history", [])

            if len(history) >= 2:
                if history[-1] > history[-2]:
                    trend = "Improving ↑"
                elif history[-1] < history[-2]:
                    trend = "Falling ↓"
                else:
                    trend = "Unchanged →"
            else:
                trend = "New"

            subject_tree.insert("", tk.END, values=(name, f"{score:.1f}%", trend))

        if "school_subject_combo" in globals():
            school_subject_combo["values"] = sorted(
                set(data["subjects"].keys())
                | set(COMMON_SUBJECTS)
                | set(OPTION_SUBJECTS)
            )

        if "option_subject_vars" in globals():
            for subject, var in option_subject_vars.items():
                var.set(subject in data.get("option_subjects", []))

    ttk.Button(buttons, text="Add Subject", command=add_subject).pack(side="left", padx=(0, 5))
    ttk.Button(buttons, text="Update Score", command=update_score).pack(side="left")

    subject_tree = ttk.Treeview(left, columns=("Subject", "Score", "Trend"), show="headings", height=18)
    subject_tree.heading("Subject", text="Subject")
    subject_tree.heading("Score", text="Score")
    subject_tree.heading("Trend", text="Trend")
    subject_tree.column("Subject", width=155)
    subject_tree.column("Score", width=70)
    subject_tree.column("Trend", width=100)
    subject_tree.pack(fill="both", expand=True)

    ttk.Button(left, text="Delete Selected", command=delete_subject).pack(fill="x", pady=(10, 0))

    # Tab 2: school timetable
    school_tab = ttk.Frame(notebook, padding=12)
    notebook.add(school_tab, text="School Timetable")

    info = ttk.LabelFrame(school_tab, text="School Day", padding=10)
    info.pack(fill="x", pady=(0, 10))

    ttk.Label(
        info,
        text=(
            "Tutor 08:40–09:00 | "
            "P1 09:00–10:00 | "
            "P2 10:00–11:00 | "
            "Break 11:00–11:20 | "
            "P3 11:20–12:20 | "
            "P4 12:20–13:20 | "
            "Lunch 13:20–14:00 | "
            "P5 14:00–15:00"
        ),
    ).pack(anchor="w")

    form = ttk.LabelFrame(school_tab, text="Add School Lesson", padding=12)
    form.pack(fill="x", pady=(0, 10))

    ttk.Label(form, text="Day").grid(row=0, column=0, padx=5, pady=3)
    school_day_combo = ttk.Combobox(form, values=DAYS[:5], state="readonly", width=12)
    school_day_combo.grid(row=1, column=0, padx=5, pady=3)
    school_day_combo.set("Monday")

    ttk.Label(form, text="Period").grid(row=0, column=1, padx=5, pady=3)
    school_period_combo = ttk.Combobox(form, values=PERIOD_ORDER, state="readonly", width=8)
    school_period_combo.grid(row=1, column=1, padx=5, pady=3)
    school_period_combo.set("P1")

    ttk.Label(form, text="Subject").grid(row=0, column=2, padx=5, pady=3)
    school_subject_combo = ttk.Combobox(form, values=[], state="readonly", width=20)
    school_subject_combo.grid(row=1, column=2, padx=5, pady=3)

    double_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(form, text="Double lesson", variable=double_var).grid(row=1, column=3, padx=10, pady=3)
    ttk.Button(form, text="Add Lesson", command=lambda: add_school_lesson(data, school_day_combo, school_period_combo, school_subject_combo, double_var, refresh_school_timetable)).grid(row=1, column=4, padx=5, pady=3)

    ttk.Label(
        school_tab,
        text=(
            "Choose a day, period and subject. "
            "Tick 'Double lesson' to automatically use the next teaching period too."
        ),
    ).pack(anchor="w", pady=(0, 8))

    school_tree_frame = ttk.Frame(school_tab)
    school_tree_frame.pack(fill="both", expand=True)

    def refresh_school_timetable():
        for item in school_tree.get_children():
            school_tree.delete(item)

        for day in DAYS[:5]:
            lessons = data["school_timetable"].get(day, [])
            lesson_by_period = {lesson["period"]: lesson for lesson in lessons}

            for period, start, end in SCHOOL_PERIODS:
                if period == "Tutor":
                    school_tree.insert("", tk.END, values=(day, period, f"{start}–{end}", "Tutor", "Fixed"))
                elif period == "Break":
                    school_tree.insert("", tk.END, values=(day, period, f"{start}–{end}", "Break", "Fixed"))
                elif period == "Lunch":
                    school_tree.insert("", tk.END, values=(day, period, f"{start}–{end}", "Lunch", "Fixed"))
                elif period in lesson_by_period:
                    lesson = lesson_by_period[period]
                    school_tree.insert(
                        "",
                        tk.END,
                        values=(
                            day,
                            period,
                            f"{start}–{end}",
                            lesson["subject"],
                            "Double" if lesson.get("double", False) else "Single",
                        ),
                    )
                else:
                    school_tree.insert("", tk.END, values=(day, period, f"{start}–{end}", "FREE / STUDY", "Free"))

    school_tree = ttk.Treeview(school_tree_frame, columns=("Day", "Period", "Time", "Subject", "Type"), show="headings")
    for column in ("Day", "Period", "Time", "Subject", "Type"):
        school_tree.heading(column, text=column)
    school_tree.column("Day", width=100)
    school_tree.column("Period", width=70)
    school_tree.column("Time", width=120)
    school_tree.column("Subject", width=200)
    school_tree.column("Type", width=90)
    school_tree.pack(side="left", fill="both", expand=True)

    school_scrollbar = ttk.Scrollbar(school_tree_frame, orient="vertical", command=school_tree.yview)
    school_scrollbar.pack(side="right", fill="y")
    school_tree.configure(yscrollcommand=school_scrollbar.set)

    ttk.Button(school_tab, text="Delete Selected Lesson", command=lambda: delete_school_lesson(data, school_tree, refresh_school_timetable)).pack(fill="x", pady=(10, 0))

    # Tab 3: option subjects
    options_tab = ttk.Frame(notebook, padding=12)
    notebook.add(options_tab, text="Option Subjects")

    

    option_subject_vars = {}
    option_subject_frame = ttk.Frame(options_tab)
    option_subject_frame.pack(fill="both", expand=True)

    for subject in OPTION_SUBJECTS:
        var = tk.BooleanVar(value=subject in data.get("option_subjects", []))
        option_subject_vars[subject] = var

        ttk.Checkbutton(
            option_subject_frame,
            text=subject,
            variable=var,
            command=lambda s=subject: toggle_option_subject(data, s, option_subject_vars[s].get(), refresh_subjects),
        ).pack(anchor="w", pady=2)

    # Tab 4: timetable
    timetable_tab = ttk.Frame(notebook, padding=12)
    notebook.add(timetable_tab, text="Revision Timetable")

    ttk.Button(timetable_tab, text="Generate Adaptive Timetable", command=lambda: generate_timetable(data, timetable_text)).pack(fill="x", pady=(0, 10))

    text_frame = ttk.Frame(timetable_tab)
    text_frame.pack(fill="both", expand=True)

    scroll = ttk.Scrollbar(text_frame)
    scroll.pack(side="right", fill="y")

    timetable_text = tk.Text(text_frame, wrap="none", font=("Consolas", 11), yscrollcommand=scroll.set)
    timetable_text.pack(fill="both", expand=True)
    scroll.config(command=timetable_text.yview)

    timetable_text.tag_configure("title", font=("Segoe UI", 17, "bold"))
    timetable_text.tag_configure("day", font=("Segoe UI", 12, "bold"))

    timetable_text.insert(
        tk.END,
        "Your timetable will appear here.\n\n"
        "1. Add your subjects and current scores.\n"
        "2. Enter your normal school lessons in the School Timetable tab.\n"
        "3. Mark doubles where appropriate.\n"
        "4. Generate the adaptive timetable.\n\n"
        "The planner keeps your after-school break, dinner/free time,\n"
        "2 hours of Photography, and 21:00 finish protected.",
    )
    timetable_text.config(state=tk.DISABLED)

    refresh_subjects()
    school_subject_combo["values"] = sorted(set(data["subjects"].keys()) | set(COMMON_SUBJECTS) | set(OPTION_SUBJECTS))
    refresh_school_timetable()

    root.mainloop()


def toggle_option_subject(data, subject_name, selected, refresh_subjects):
    current = data.get("option_subjects", [])

    if selected:

        if subject_name not in current:
            current.append(subject_name)
            data["option_subjects"] = current

        data["subjects"].setdefault(subject_name, {"score": 0, "history": [0]})
        save_data(data)
        refresh_subjects()
        return True

    data["option_subjects"] = [item for item in current if item != subject_name]
    save_data(data)
    refresh_subjects()
    return True


def add_school_lesson(data, school_day_combo, school_period_combo, school_subject_combo, double_var, refresh_school_timetable):
    day = school_day_combo.get()
    period = school_period_combo.get()
    subject = school_subject_combo.get()
    is_double = double_var.get()

    if not subject:
        messagebox.showerror("Missing subject", "Choose a subject first.")
        return
    if not period:
        messagebox.showerror("Missing period", "Choose a period.")
        return

    period_index = PERIOD_ORDER.index(period)
    for lesson in data["school_timetable"][day]:
        if lesson["period"] == period:
            messagebox.showerror("Already occupied", f"{day} {period} already contains {lesson['subject']}.")
            return

    periods_used = [period]
    if is_double:
        if period_index == len(PERIOD_ORDER) - 1:
            messagebox.showerror("Invalid double", "P5 cannot be the first period of a double.")
            return
        next_period = PERIOD_ORDER[period_index + 1]
        for lesson in data["school_timetable"][day]:
            if lesson["period"] == next_period:
                messagebox.showerror("Already occupied", f"{day} {next_period} already contains {lesson['subject']}.")
                return
        periods_used.append(next_period)

    start = TEACHING_PERIODS[period][0]
    if is_double:
        end = TEACHING_PERIODS[periods_used[-1]][1]
    else:
        end = TEACHING_PERIODS[period][1]

    new_lesson = {"period": period, "start": start, "end": end, "subject": subject, "double": is_double}
    data["school_timetable"][day].append(new_lesson)
    data["school_timetable"][day].sort(key=lambda lesson: PERIOD_ORDER.index(lesson["period"]))
    save_data(data)
    refresh_school_timetable()
    school_subject_combo.set("")
    double_var.set(False)


def delete_school_lesson(data, school_tree, refresh_school_timetable):
    selected = school_tree.selection()
    if not selected:
        messagebox.showwarning("Select a lesson", "Select a lesson first.")
        return

    values = school_tree.item(selected[0], "values")
    day, period, time, subject, lesson_type = values
    if lesson_type in ("Fixed", "Free"):
        messagebox.showwarning("Cannot delete", "Tutor, break, lunch and free periods are automatic.")
        return

    lessons = data["school_timetable"][day]
    for index, lesson in enumerate(lessons):
        if lesson["period"] == period and lesson["subject"] == subject:
            del lessons[index]
            break

    save_data(data)
    refresh_school_timetable()


def calculate_priorities(data):
    priorities = {}
    for name, info in data["subjects"].items():
        score = float(info["score"])
        priority = 100 - score
        history = info.get("history", [])
        if len(history) >= 2:
            previous = float(history[-2])
            current = float(history[-1])
            if current < previous:
                priority += min((previous - current) * 1.5, 25)
        priorities[name] = max(priority, 1)
    return priorities


def build_revision_queue(data):
    priorities = calculate_priorities(data)
    if not priorities:
        return []

    ordered = sorted(priorities.keys(), key=lambda subject: priorities[subject], reverse=True)
    queue = []
    for subject in ordered:
        score = data["subjects"][subject]["score"]
        if score <= 30:
            weight = 5
        elif score <= 45:
            weight = 4
        elif score <= 60:
            weight = 3
        elif score <= 75:
            weight = 2
        else:
            weight = 1
        queue.extend([subject] * weight)
    return queue


def get_available_revision_slots():
    slots = []
    for day in DAYS:
        if day in DAYS[:5]:
            day_slots = WEEKDAY_REVISION_SLOTS
        else:
            day_slots = WEEKEND_REVISION_SLOTS
        for start, end in day_slots:
            slots.append((day, start, end))
    return slots


def make_subject_assignments(data):
    queue = build_revision_queue(data)
    if not queue:
        return []

    assignments = []
    last_subject = None
    for position in range(len(get_available_revision_slots())):
        candidates = queue[position % len(queue):] + queue[:position % len(queue)]
        chosen = None
        for candidate in candidates:
            if candidate != last_subject:
                chosen = candidate
                break
        if chosen is None:
            chosen = candidates[0]
        assignments.append(chosen)
        last_subject = chosen
    return assignments


def generate_timetable(data, timetable_text):
    if not data["subjects"]:
        messagebox.showwarning("No subjects", "Add at least one subject first.")
        return

    timetable = {day: [] for day in DAYS}
    all_slots = get_available_revision_slots()
    fixed_photography = [("Wednesday", "20:00", "21:00"), ("Saturday", "20:00", "21:00")]
    occupied = set()

    for day, start, end in fixed_photography:
        timetable[day].append((start, end, "Photography"))
        occupied.add((day, start, end))

    revision_slots = [slot for slot in all_slots if slot not in occupied]
    assignments = make_subject_assignments(data)[:len(revision_slots)]

    for slot, subject in zip(revision_slots, assignments):
        day, start, end = slot
        timetable[day].append((start, end, subject))

    for day in DAYS:
        timetable[day].sort(key=lambda item: time_to_minutes(item[0]))

    display_timetable(timetable, timetable_text)


def display_timetable(timetable, timetable_text):
    timetable_text.config(state=tk.NORMAL)
    timetable_text.delete("1.0", tk.END)

    timetable_text.insert(tk.END, "WEEKLY ADAPTIVE REVISION TIMETABLE\n", "title")
    timetable_text.insert(tk.END, "School: 07:00–15:00 | Home: 15:30 | Break: 15:30–16:00\n")
    timetable_text.insert(tk.END, "Dinner / free time: 18:00–20:00 | Finish: 21:00\n\n")

    for day in DAYS:
        timetable_text.insert(tk.END, f"{day}\n", "day")
        timetable_text.insert(tk.END, "-" * 48 + "\n")
        for start, end, subject in timetable[day]:
            label = "Photography ★" if subject == "Photography" else subject
            timetable_text.insert(tk.END, f"{start}–{end}   {label}\n")
        timetable_text.insert(tk.END, "\n")

    timetable_text.insert(tk.END, "PLANNER RULES\n", "day")
    timetable_text.insert(
        tk.END,
        "• School: Monday–Friday, 07:00–15:00\n"
        "• Travel/home time: 15:00–15:30\n"
        "• Protected break: 15:30–16:00\n"
        "• Dinner/free time: 18:00–20:00\n"
        "• No revision after 21:00\n"
        "• Photography: exactly 2 hours per week\n"
        "• Lower scores receive more revision\n"
        "• Falling scores receive an extra priority boost\n"
        "• Double school lessons are stored in your timetable\n",
    )
    timetable_text.config(state=tk.DISABLED)


def main():
    make_app()
