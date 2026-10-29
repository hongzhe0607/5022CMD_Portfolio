"""
course_system.py
Menu-driven University Course Prerequisite System.

Edge direction:  PREREQUISITE  ->  COURSE IT UNLOCKS
   e.g. CS101 -> CS201 means "CS101 is a prerequisite of CS201".
So:
   prerequisites of X  = incoming adjacent vertices of X
   courses unlocked by X = outgoing adjacent vertices of X

Run:  python course_system.py
"""
from graph import Graph
from course import Course


class CourseRegistry:
    """Connects Course objects (the domain) with the generic Graph."""

    def __init__(self):
        self.graph = Graph()
        self._by_code = {}                  # code -> Course, for O(1) lookup

    def add_course(self, course):
        if course.course_code in self._by_code:
            return False
        self._by_code[course.course_code] = course
        self.graph.addVertex(course)        # the Course object IS the vertex
        return True

    def get(self, code):
        return self._by_code.get(code.strip().upper())

    def all_courses(self):
        return sorted(self._by_code.values(), key=lambda c: c.course_code)

    def add_prerequisite(self, course, prereq):
        """Make `prereq` a prerequisite of `course` (edge prereq -> course).
        Refuses edges that would create a cycle (A needs B, B needs A)."""
        if course is prereq:
            return "A course cannot be its own prerequisite."
        if self.graph.hasEdge(prereq, course):
            return f"{prereq.course_code} is already a prerequisite of {course.course_code}."
        if self.graph.hasPath(course, prereq):
            return (f"Not allowed: {course.course_code} already leads to "
                    f"{prereq.course_code}, this would create a circular prerequisite.")
        self.graph.addEdge(prereq, course)
        return None

    def remove_prerequisite(self, course, prereq):
        return self.graph.removeEdge(prereq, course)

    def prerequisites_of(self, course):
        return sorted(self.graph.listIncomingAdjacentVertex(course),
                      key=lambda c: c.course_code)

    def unlocked_by(self, course):
        return sorted(self.graph.listOutgoingAdjacentVertex(course),
                      key=lambda c: c.course_code)


def build_sample_registry():
    reg = CourseRegistry()
    courses = [
        Course("CS101", "Introduction to Programming", 4, "core", 1, "Dr. Tan"),
        Course("CS102", "Discrete Mathematics", 3, "core", 1, "Dr. Lim"),
        Course("CS201", "Data Structures", 4, "core", 2, "Dr. Wong"),
        Course("CS202", "Web Development", 3, "elective", 2, "Mr. Lee"),
        Course("CS301", "Algorithms", 4, "core", 3, "Dr. Kumar"),
        Course("CS302", "Database Systems", 4, "core", 3, "Ms. Ng"),
        Course("CS303", "Mobile App Development", 3, "elective", 3, "Mr. Chong"),
        Course("CS401", "Software Engineering", 4, "core", 4, "Dr. Rahman"),
    ]
    for c in courses:
        reg.add_course(c)

    # (prerequisite, course)
    links = [("CS101", "CS201"), ("CS102", "CS201"), ("CS101", "CS202"),
             ("CS201", "CS301"), ("CS102", "CS301"), ("CS201", "CS302"),
             ("CS202", "CS303"), ("CS302", "CS303"), ("CS301", "CS401"),
             ("CS302", "CS401")]
    for pre, crs in links:
        reg.add_prerequisite(reg.get(crs), reg.get(pre))
    return reg


# ---------------------------------------------------------------------- #
# Menu helpers
# ---------------------------------------------------------------------- #
def ask_course(reg, prompt="Enter Course Code: "):
    course = reg.get(input(prompt))
    if course is None:
        print("Course not found.")
    return course


def print_list(title, courses, empty_msg):
    print(title)
    if not courses:
        print(f"  {empty_msg}")
    for c in courses:
        print(f"  - {c}")


# Mandatory features
def view_all(reg):
    print("\nAvailable Courses:")
    for i, c in enumerate(reg.all_courses(), 1):
        print(f"{i}. {c.course_code} - {c.course_name}")


def view_details(reg):
    c = ask_course(reg)
    if c:
        print("\n" + c.full_details())          # ignores visibility setting


def view_prereqs(reg):
    c = ask_course(reg)
    if c:
        print_list(f"Prerequisites for {c.course_code} - {c.course_name}:",
                   reg.prerequisites_of(c), "None (no prerequisites)")


def view_unlocked(reg):
    c = ask_course(reg)
    if c:
        print_list(f"Courses unlocked by {c.course_code} - {c.course_name}:",
                   reg.unlocked_by(c), "None (does not unlock any course)")


# Advanced features
def add_course(reg):
    code = input("New Course Code: ").strip().upper()
    if not code or reg.get(code):
        print("Invalid or duplicate course code.")
        return
    name = input("Course Name: ").strip() or "Untitled"
    try:
        credits = int(input("Credit Hours: "))
        year = int(input("Year of study: "))
    except ValueError:
        print("Credit hours and year must be numbers.")
        return
    level = input("Level (core/elective): ").strip().lower()
    if level not in (Course.CORE, Course.ELECTIVE):
        print("Level must be 'core' or 'elective'.")
        return
    lecturer = input("Lecturer: ").strip() or "TBA"
    reg.add_course(Course(code, name, credits, level, year, lecturer))
    print(f"Course {code} added.")


def view_profile(reg):
    c = ask_course(reg)
    if c:
        print("\n" + c.profile())


def add_prereq(reg):
    x = ask_course(reg, "Course X (the course that needs a prerequisite): ")
    if not x:
        return
    y = ask_course(reg, "Course Y (the prerequisite to add): ")
    if not y:
        return
    error = reg.add_prerequisite(x, y)
    print(error or f"{y.course_code} is now a prerequisite of {x.course_code}.")


def remove_prereq(reg):
    x = ask_course(reg, "Course X: ")
    if not x:
        return
    y = ask_course(reg, "Prerequisite Y to remove: ")
    if not y:
        return
    if reg.remove_prerequisite(x, y):
        print(f"{y.course_code} is no longer a prerequisite of {x.course_code}.")
    else:
        print(f"{y.course_code} was not a prerequisite of {x.course_code}.")


MENU = [
    ("View All Courses", view_all),
    ("View Course Details", view_details),
    ("View Prerequisites of a Course", view_prereqs),
    ("View Courses Unlocked by a Course", view_unlocked),
    ("Add a New Course", add_course),
    ("View Course Profile (core/elective visibility)", view_profile),
    ("Add a Prerequisite to a Course", add_prereq),
    ("Remove a Prerequisite from a Course", remove_prereq),
]


def main():
    reg = build_sample_registry()
    exit_no = len(MENU) + 1
    while True:
        print("\n==== University Course Prerequisite System ====")
        for i, (label, _) in enumerate(MENU, 1):
            print(f"{i}. {label}")
        print(f"{exit_no}. Exit")
        choice = input("Enter choice: ").strip()
        if choice == str(exit_no):
            print("Exiting program. Goodbye!")
            break
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            MENU[int(choice) - 1][1](reg)
        else:
            print(f"Invalid choice, please enter 1-{exit_no}.")


if __name__ == "__main__":
    main()
