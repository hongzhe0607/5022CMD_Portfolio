"""
course.py
Course entity class - one course offered by the university.
"""


class Course:
    CORE = "core"
    ELECTIVE = "elective"

    def __init__(self, course_code, course_name, credit_hours, level, year, lecturer):
        self.course_code = course_code.upper()
        self.course_name = course_name
        self.credit_hours = int(credit_hours)
        self.level = level.lower()          # "core" or "elective"
        self.year = int(year)               # year of study it is offered
        self.lecturer = lecturer

    def is_core(self):
        return self.level == Course.CORE

    def full_details(self):
        return (f"Course Code : {self.course_code}\n"
                f"Course Name : {self.course_name}\n"
                f"Credit Hours: {self.credit_hours}\n"
                f"Level       : {self.level.capitalize()}\n"
                f"Year        : {self.year}\n"
                f"Lecturer    : {self.lecturer}")

    def profile(self):
        """Visibility rule (advanced feature b):
        core -> all details, elective -> name only."""
        if self.is_core():
            return self.full_details()
        return f"Course Name : {self.course_name}\n(Elective course - other details hidden)"

    def __str__(self):
        return f"{self.course_code} ({self.course_name})"
