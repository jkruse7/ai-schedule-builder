import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), 'PittAPI'))
print(sys.path)
from pittapi import course

cs_subject = course.get_subject_courses(subject='CS')
courses_dict = cs_subject.courses # subject code, dictionary of courses

def filtered_courses(courses:dict[str, course.Course]) -> List[str]:
    parsed_courses = []
    for key, course in courses.items():
        parsed_courses.append(f"{course.subject_code} {course.course_number} {course.course_title}")
    return parsed_courses

parsed_courses = filtered_courses(courses_dict)
print(parsed_courses)