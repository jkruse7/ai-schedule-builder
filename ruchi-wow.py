import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'PittAPI'))
from pittapi import course

cs_subject = course.get_subject_courses(subject='CS')
courses_dict = cs_subject.courses

print(courses_dict)

cs_course = course.get_course_details(term='2244', subject='CS', course='1501')
section_list = cs_course.sections

print(section_list)