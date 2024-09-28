import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'PittAPI'))
from pittapi import course

# cs_subject = course.get_subject_courses(subject='CS')
# courses_dict = cs_subject.courses # subject code, dictionary of courses

# parsed_courses = filtered_courses(courses_dict)
# print(parsed_courses)

def get_courses_by_subject(subject: str):
    cs_subject = course.get_subject_courses(subject)
    return format_courses(cs_subject.courses)

def format_courses(courses:dict[str, course.Course]) -> dict:
    formatted = []
    # print(courses)
    for key in courses:
      cur_dict = courses[key]._asdict()
      cur_dict["course_key"] = key
      formatted.append(cur_dict)
    return formatted

def filtered_courses(courses:dict[str, course.Course]) -> List[str]:
    parsed_courses = {}
    for key, course in courses.items():
        parsed_courses[key] = (f"{course.subject_code} {course.course_number} {course.course_title}")
    return parsed_courses

if __name__ == "__main__":
    cool = get_courses_by_subject(subject="CS")
    print(cool[0])