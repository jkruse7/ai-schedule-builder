import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'PittAPI'))
from pittapi import course

major_courses_cache = {}

def get_cached_courses(major):
    if major in major_courses_cache:
      return major_courses_cache[major]
    return []

def get_courses_by_subject(major: str):
    if major in major_courses_cache:
    #   # print(major_courses_cache[major]a
      return major_courses_cache[major]
    major_courses = course.get_subject_courses(major)
    formatted = format_courses(major_courses.courses)
    major_courses_cache[major] = formatted
    return formatted

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