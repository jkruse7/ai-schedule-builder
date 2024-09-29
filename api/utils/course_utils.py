import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'PittAPI'))
from pittapi import course
import os
import google.generativeai as genai
from pymongo import MongoClient

# Replace <connection_string> with your MongoDB connection string
client = MongoClient("mongodb+srv://ruh32:MUKYGIasKz8Bc4rn@aischedulebuilder.hfmwv.mongodb.net/?retryWrites=true&w=majority&appName=AIScheduleBuilder")
db = client['AIScheduleBuilder']
collection = db['Major Requirements']

genai.configure(api_key="AIzaSyCgKFCeZ3CUrb62iwvzwdmw-v5pv5ylSpg")

major_courses_cache = {}
questions_cache = {}
recommendations_cache = {}

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[]
)


def ask_gemini_to_generate_questions(all_courses: dict[str, str], courses_taken:dict[str, str]):
    taken = str(courses_taken) # convert to string courses taken
    if taken in questions_cache:
        return questions_cache[taken]
    total_courses = str(all_courses) # convert to string all classes
    response = chat_session.send_message("Here are all the courses available to me: " + total_courses + ". Here are all the courses I have taken so far: " + taken + ". Can you generate 5 yes or no questions that gauge my interests for future classes? For your response, return each question in plain text, with a new line in between each question.") # sending in classes already taken, course details, as a string
    questions_cache[taken] = response.text
    print(response.text)
    return response.text

# answers from user
def ask_gemini_for_recs(answers:List[str], response: str, class_list: dict[str, str], courses_taken: dict[str, str]):
    full = ""
    for s in answers:
        full += s + " , "
    if (response + full) in recommendations_cache:
        return recommendations_cache[response + full]
    gemini_response = chat_session.send_message("Here are the questions I was asked: " + response + ". Here are my answers to the question: " + full + ". Here are the classes available: " + str(class_list) + ". Here are the classes I have already taken: " + str(courses_taken) + ". Can you give me a list of classes that I am best suited to take? Return only the class names in the format 'CS 0007 Introduction to Computer Programming', with each class seperated by a new line. Do not return any text besides the classes and limit your recomendations to 10 classes.")
    recommendations_cache[response + full] = gemini_response.text
    print(gemini_response.text)
    return gemini_response.text

def get_average_difficulty(classes_selected: dict): # hella slow.
    full_list = []
    average_list = {}
    for classes in classes_selected:
        try:
            response = course._get_course_sections(classes["course_id"], "2234") 
            catalog_nbr = ""
            for res in response['sections']:
                #print(res['catalog_nbr'])
                catalog_nbr = res['catalog_nbr']
                for instructor in res['instructors']:
                    full_list.append(instructor['name'])
                
            average_list[res['catalog_nbr']] = rmp_code.get_prof_difficulty_average(full_list)

        except:
            continue
    
    print(average_list)
    return(average_list)

def get_following_classes(sems_left: str, classes_I_want: dict):
    average = get_average_difficulty(classes_I_want)
    response = chat_session.send_message("I have " + sems_left + " semesters left. These are the classes I want to take " + str(classes_I_want) + " and this is their difficulty " + str(average) + " What classes should I take when to ensure I do not burn out? Please only give me a list of them and tell me which semester I should do it.")
    print(response.text)
    return response.text

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

def is_in_class_selected(classes_selected: list[dict[str, str]], class_list:str):
        for classy in classes_selected:
            try:
                if classy['course_number'] == class_list:
                    print(class_list)
                    print(classy['course_number'])
                    return False
            except: 
                classy.split(" ")
                if classy[1] == class_list:
                    return False
        return True
       
        
def is_in_class_taken(classes_taken: list[dict[str, str]], class_list:str):
    for classy in classes_taken:
        if classy['course_number'] == class_list: #in
            print(class_list)
            print(classy['course_number'])
            return False
    return True

if __name__ == "__main__":
    cool = get_courses_by_subject("CS")
    # should change based on what they enter
    courses_taken = {"course_id": "105699", "course_key": "0449", "course_number": "0449", "course_title": "INTRODUCTION TO SYSTEMS SOFTWARE", "subject_code": "CS"}, {"subject_code": "CS", "course_number": "0004", "course_id": "105609", "course_title": "INTRODUCTION TO COMPUTER PROGRAMMING-BASIC", "course_key": "0004"}
    all_courses = {"subject_code": "CS", "course_number": "0004", "course_id": "105609", "course_title": "INTRODUCTION TO COMPUTER PROGRAMMING-BASIC", "course_key": "0004"}, {"subject_code": "CS", "course_number": "0007", "course_id": "105611", "course_title": "INTRODUCTION TO COMPUTER PROGRAMMING", "course_key": "0007"}, {"subject_code": "CS", "course_number": "0008", "course_id": "183225", "course_title": "INTRODUCTION TO COMPUTER PROGRAMMING WITH PYTHON", "course_key": "0008"}, {"subject_code": "CS", "course_number": "0010", "course_id": "190421", "course_title": "INTRODUCTION TO COMPUTING FOR SYSTEMS ENGINEERS", "course_key": "0010"}, {"subject_code": "CS", "course_number": "0011", "course_id": "190422", "course_title": "INTRODUCTION TO COMPUTING FOR SCIENTISTS", "course_key": "0011"}, {"subject_code": "CS", "course_number": "0012", "course_id": "190423", "course_title": "INTRODUCTION TO COMPUTING FOR THE HUMANITIES", "course_key": "0012"}, {"subject_code": "CS", "course_number": "0015", "course_id": "105615", "course_title": "INTRODUCTION TO COMPUTER PROGRAM", "course_key": "0015"}, {"subject_code": "CS", "course_number": "0016", "course_id": "105616", "course_title": "INTRODUCTION TO COMPUTER PROGRAMMING APPLICATIONS", "course_key": "0016"}, {"subject_code": "CS", "course_number": "0045", "course_id": "105634", "course_title": "ALGORITHMS AND INFORMATION STRUCTURES APPLICATIONS", "course_key": "0045"}, {"subject_code": "CS", "course_number": "0046", "course_id": "105635", "course_title": "COMPUTER SYSTEMS ARCHITECTURE APPLICATIONS", "course_key": "0046"}, {"subject_code": "CS", "course_number": "0047", "course_id": "105636", "course_title": "ADVANCED PROGRAMMING CONCEPTS APPLICATIONS", "course_key": "0047"}, {"subject_code": "CS", "course_number": "0048", "course_id": "105637", "course_title": "DATA STRUCTS & FILES APPLICATNS", "course_key": "0048"}, {"subject_code": "CS", "course_number": "0081", "course_id": "105642", "course_title": "COMPUTER LITERACY", "course_key": "0081"}, {"subject_code": "CS", "course_number": "0082", "course_id": "105643", "course_title": "CS ASSISTANTSHIP NONMAJORS", "course_key": "0082"}, {"subject_code": "CS", "course_number": "0085", "course_id": "105644", "course_title": "PC SOFTWARE FOR BUSINESS", "course_key": "0085"}, {"subject_code": "CS", "course_number": "0090", "course_id": "181863", "course_title": "SUSTAINABILITY AND COMPUTING", "course_key": "0090"}, {"subject_code": "CS", "course_number": "0098", "course_id": "185140", "course_title": "DECSION MAKING WITH EXCEL\t", "course_key": "0098"}, {"subject_code": "CS", "course_number": "0100", "course_id": "105645", "course_title": "PERSPECTIVES IN COMPUTER SCIENCE", "course_key": "0100"}, {"subject_code": "CS", "course_number": "0131", "course_id": "105657", "course_title": "SOFTWARE FOR PERSONAL COMPUTING", "course_key": "0131"}, {"subject_code": "CS", "course_number": "0134", "course_id": "105660", "course_title": "WEB SITE DESIGN AND DEVELOPMENT", "course_key": "0134"}, {"subject_code": "CS", "course_number": "0135", "course_id": "105661", "course_title": "ADV SOFTWARE-PERSNL COMPUTING", "course_key": "0135"}, {"subject_code": "CS", "course_number": "0145", "course_id": "181639", "course_title": "INTRODUCTION TO DIGITAL IMAGING", "course_key": "0145"}, {"subject_code": "CS", "course_number": "0155", "course_id": "184374", "course_title": "DATA WITCHCRAFT", "course_key": "0155"}, {"subject_code": "CS", "course_number": "0180", "course_id": "105662", "course_title": "DATABASE DESIGN", "course_key": "0180"}, {"subject_code": "CS", "course_number": "0207", "course_id": "105679", "course_title": "JAVA FOR INTERMEDIATE PROGRAMMERS", "course_key": "0207"}, {"subject_code": "CS", "course_number": "0241", "course_id": "195188", "course_title": "NON-JAVA INTERMEDIATE PROGRAMMING", "course_key": "0241"}, {"subject_code": "CS", "course_number": "0245", "course_id": "195127", "course_title": "NON-JAVA ALGORITHMS AND DATA STRUCTURES 1", "course_key": "0245"}, {"subject_code": "CS", "course_number": "0251", "course_id": "195128", "course_title": "NON-JAVA ALGORITHMS AND DATA STRUCTURES 2", "course_key": "0251"}, {"subject_code": "CS", "course_number": "0334", "course_id": "171560", "course_title": "INTERMEDIATE WEB SITE DESIGN AND DEVELOPMENT", "course_key": "0334"}, {"subject_code": "CS", "course_number": "0401", "course_id": "105686", "course_title": "INTERMEDIATE PROGRAMMING USING JAVA", "course_key": "0401"}, {"subject_code": "CS", "course_number": "0405", "course_id": "187142", "course_title": "PROGRAMMING USING PYTHON", "course_key": "0405"}, {"subject_code": "CS", "course_number": "0406", "course_id": "105689", "course_title": "DISCRETE MATH 2 & STATS FOR CS", "course_key": "0406"}, {"subject_code": "CS", "course_number": "0410", "course_id": "105692", "course_title": "INTRO TO COMPTR SCI PRGM APPLC", "course_key": "0410"}, {"subject_code": "CS", "course_number": "0411", "course_id": "105693", "course_title": "INTRO COMPUTER SCI PROGRMMNG", "course_key": "0411"}, {"subject_code": "CS", "course_number": "0417", "course_id": "175419", "course_title": "INTERMEDIATE PROGRAMMING USING JAVA", "course_key": "0417"}, {"subject_code": "CS", "course_number": "0421", "course_id": "170834", "course_title": "PROGRAMMING USING JAVA", "course_key": "0421"}, {"subject_code": "CS", "course_number": "0422", "course_id": "170835", "course_title": "ADVANCED PROGRAMMING USING JAVA", "course_key": "0422"}, {"subject_code": "CS", "course_number": "0441", "course_id": "105694", "course_title": "DISCRETE STRUCTURES FOR CS", "course_key": "0441"}, {"subject_code": "CS", "course_number": "0445", "course_id": "105695", "course_title": "ALGORITHMS AND DATA STRUCTURES 1", "course_key": "0445"}, {"subject_code": "CS", "course_number": "0446", "course_id": "105696", "course_title": "INTRODUCTION TO COMPUTER SCIENCE CONCEPTS", "course_key": "0446"}, {"subject_code": "CS", "course_number": "0447", "course_id": "105697", "course_title": "COMPUTER ORGANIZATION AND ASSEMBLY LANGUAGE", "course_key": "0447"}, {"subject_code": "CS", "course_number": "0449", "course_id": "105699", "course_title": "INTRODUCTION TO SYSTEMS SOFTWARE", "course_key": "0449"}, {"subject_code": "CS", "course_number": "0455", "course_id": "105700", "course_title": "ALGORITHMS AND INFORMATION STRUCTURES", "course_key": "0455"}, {"subject_code": "CS", "course_number": "0456", "course_id": "105701", "course_title": "COMPUTER SYSTEMS ARCHITECTURE", "course_key": "0456"}, {"subject_code": "CS", "course_number": "0457", "course_id": "105702", "course_title": "ADVANCED PROGRAMMING CONCEPTS", "course_key": "0457"}, {"subject_code": "CS", "course_number": "0458", "course_id": "105703", "course_title": "DATA STRUCTURES AND FILES", "course_key": "0458"}, {"subject_code": "CS", "course_number": "0590", "course_id": "184201", "course_title": "SOCIAL IMPLICATIONS OF COMPUTING TECHNOLOGY", "course_key": "0590"}, {"subject_code": "CS", "course_number": "0699", "course_id": "184373", "course_title": "SPECIAL TOPICS IN COMPUTER SCIENCE", "course_key": "0699"}, {"subject_code": "CS", "course_number": "1132", "course_id": "105723", "course_title": "CLASSICAL NUMERICAL ANALYSIS", "course_key": "1132"}, {"subject_code": "CS", "course_number": "1163", "course_id": "105725", "course_title": "ADVANCED TOPICS IN CS", "course_key": "1163"}, {"subject_code": "CS", "course_number": "1164", "course_id": "105726", "course_title": "ADVANCED CS TOPICS & APPLICATNS", "course_key": "1164"}, {"subject_code": "CS", "course_number": "1165", "course_id": "105727", "course_title": "DIRECTED PROJECT", "course_key": "1165"}, {"subject_code": "CS", "course_number": "1171", "course_id": "105728", "course_title": "COMPUTER SCIENCE ASSISTANTSHIP", "course_key": "1171"}, {"subject_code": "CS", "course_number": "1399", "course_id": "184344", "course_title": "COMPUTER SCIENCE INTERNSHIP", "course_key": "1399"}, {"subject_code": "CS", "course_number": "1498", "course_id": "105759", "course_title": "DIRECTED RES: COMPUTER SCIENCE", "course_key": "1498"}, {"subject_code": "CS", "course_number": "1501", "course_id": "105761", "course_title": "ALGORITHMS AND DATA STRUCTURES 2", "course_key": "1501"}, {"subject_code": "CS", "course_number": "1502", "course_id": "105762", "course_title": "FORMAL METHODS IN COMPUTER SCIENCE", "course_key": "1502"}, {"subject_code": "CS", "course_number": "1503", "course_id": "194819", "course_title": "MATHEMATICAL FOUNDATIONS OF MACHINE LEARNING", "course_key": "1503"}, {"subject_code": "CS", "course_number": "1510", "course_id": "105763", "course_title": "ALGORITHM DESIGN", "course_key": "1510"}, {"subject_code": "CS", "course_number": "1511", "course_id": "105764", "course_title": "THEORY OF COMPUTATION", "course_key": "1511"}, {"subject_code": "CS", "course_number": "1520", "course_id": "105767", "course_title": "PROGRAMMING LANGUAGE FOR WEB APPLICATIONS", "course_key": "1520"}, {"subject_code": "CS", "course_number": "1530", "course_id": "105768", "course_title": "SOFTWARE ENGINEERING", "course_key": "1530"}, {"subject_code": "CS", "course_number": "1538", "course_id": "105771", "course_title": "INTRODUCTION TO SIMULATION", "course_key": "1538"}, {"subject_code": "CS", "course_number": "1541", "course_id": "105772", "course_title": "INTRODUCTION TO COMPUTER ARCHITECTURE", "course_key": "1541"}, {"subject_code": "CS", "course_number": "1550", "course_id": "105774", "course_title": "INTRODUCTION TO OPERATING SYSTEMS", "course_key": "1550"}, {"subject_code": "CS", "course_number": "1555", "course_id": "105775", "course_title": "DATABASE MANAGEMENT SYSTEMS", "course_key": "1555"}, {"subject_code": "CS", "course_number": "1566", "course_id": "105778", "course_title": "INTRODUCTION COMPUTER GRAPHICS", "course_key": "1566"}, {"subject_code": "CS", "course_number": "1567", "course_id": "105779", "course_title": "PROGRAMMING SYSTEM DESIGN ON A MOBILE ROBOT PLATFORM", "course_key": "1567"}, {"subject_code": "CS", "course_number": "1571", "course_id": "105780", "course_title": "INTRODUCTION TO ARTIFICIAL INTELLIGENCE", "course_key": "1571"}, {"subject_code": "CS", "course_number": "1613", "course_id": "194137", "course_title": "QUANTUM COMPUTATION", "course_key": "1613"}, {"subject_code": "CS", "course_number": "1621", "course_id": "105785", "course_title": "STRUCTURE PROGRAMMING LANGUAGES", "course_key": "1621"}, {"subject_code": "CS", "course_number": "1622", "course_id": "105786", "course_title": "INTRODUCTION TO COMPILER DESIGN", "course_key": "1622"}, {"subject_code": "CS", "course_number": "1631", "course_id": "105787", "course_title": "SOFTWARE DESIGN METHODOLOGY", "course_key": "1631"}, {"subject_code": "CS", "course_number": "1632", "course_id": "186142", "course_title": "SOFTWARE QUALITY ASSURANCE", "course_key": "1632"}, {"subject_code": "CS", "course_number": "1635", "course_id": "178553", "course_title": "INTERFACE DESIGN METHODOLOGY", "course_key": "1635"}, {"subject_code": "CS", "course_number": "1637", "course_id": "190184", "course_title": "INTRODUCTION TO HUMAN-COMPUTER INTERACTION", "course_key": "1637"}, {"subject_code": "CS", "course_number": "1640", "course_id": "178081", "course_title": "BIOINFORMATICS SOFTWARE DESIGN", "course_key": "1640"}, {"subject_code": "CS", "course_number": "1645", "course_id": "105788", "course_title": "INTRODUCTION TO HIGH PERFORMANCE COMPUTING SYSTEMS", "course_key": "1645"}, {"subject_code": "CS", "course_number": "1651", "course_id": "105789", "course_title": "ADVANCED SYSTEMS SOFTWARE", "course_key": "1651"}, {"subject_code": "CS", "course_number": "1652", "course_id": "105790", "course_title": "DATA COMMUNICATION AND COMPUTER NETWORKS", "course_key": "1652"}, {"subject_code": "CS", "course_number": "1653", "course_id": "171440", "course_title": "APPLIED CRYPTOGRAPHY AND NETWORK SECURITY", "course_key": "1653"}, {"subject_code": "CS", "course_number": "1655", "course_id": "105791", "course_title": "SECURE DATA MANAGEMENT AND WEB APPLICATIONS", "course_key": "1655"}, {"subject_code": "CS", "course_number": "1656", "course_id": "186481", "course_title": "INTRODUCTION TO DATA SCIENCE", "course_key": "1656"}, {"subject_code": "CS", "course_number": "1657", "course_id": "105792", "course_title": "PRIVACY IN THE ELECTRONIC SOCIETY", "course_key": "1657"}, {"subject_code": "CS", "course_number": "1660", "course_id": "190185", "course_title": "INTRODUCTION TO CLOUD COMPUTING", "course_key": "1660"}, {"subject_code": "CS", "course_number": "1666", "course_id": "176426", "course_title": "PRINCIPLES OF COMPUTER GAME DESIGN AND IMPLEMENTATION", "course_key": "1666"}, {"subject_code": "CS", "course_number": "1671", "course_id": "174339", "course_title": "HUMAN LANGUAGE TECHNOLOGIES", "course_key": "1671"}, {"subject_code": "CS", "course_number": "1674", "course_id": "186929", "course_title": "INTRODUCTION TO COMPUTER VISION", "course_key": "1674"}, {"subject_code": "CS", "course_number": "1675", "course_id": "184372", "course_title": "INTRODUCTION TO MACHINE LEARNING", "course_key": "1675"}, {"subject_code": "CS", "course_number": "1678", "course_id": "192036", "course_title": "INTRODUCTION TO DEEP LEARNING", "course_key": "1678"}, {"subject_code": "CS", "course_number": "1684", "course_id": "193767", "course_title": "BIAS AND ETHICAL IMPLICATIONS IN ARTIFICIAL INTELLIGENCE", "course_key": "1684"}, {"subject_code": "CS", "course_number": "1699", "course_id": "105795", "course_title": "SPECIAL TOPICS IN COMPUTER SCIENCE", "course_key": "1699"}, {"subject_code": "CS", "course_number": "1713", "course_id": "105799", "course_title": "ALGORITHM DESIGN AND ANALYSIS", "course_key": "1713"}, {"subject_code": "CS", "course_number": "1720", "course_id": "105801", "course_title": "PROGRAMMING LANGUAGES", "course_key": "1720"}, {"subject_code": "CS", "course_number": "1735", "course_id": "105802", "course_title": "SOFTWARE DESIGN METHODOLOGY", "course_key": "1735"}, {"subject_code": "CS", "course_number": "1736", "course_id": "105803", "course_title": "SOFTWARE ENGINEERING", "course_key": "1736"}, {"subject_code": "CS", "course_number": "1760", "course_id": "175420", "course_title": "ADVANCED OBJECT-ORIENTED PROGRAMMING AND DESIGN", "course_key": "1760"}, {"subject_code": "CS", "course_number": "1761", "course_id": "194327", "course_title": "MOBILE APPLICATION DEVELOPMENT", "course_key": "1761"}, {"subject_code": "CS", "course_number": "1762", "course_id": "175421", "course_title": "WEB PROGRAMMING", "course_key": "1762"}, {"subject_code": "CS", "course_number": "1765", "course_id": "105806", "course_title": "DATA BASE MANAGEMENT SYSTEMS", "course_key": "1765"}, {"subject_code": "CS", "course_number": "1766", "course_id": "105807", "course_title": "INTRODUCTION COMPUTER GRAPHICS", "course_key": "1766"}, {"subject_code": "CS", "course_number": "1783", "course_id": "105808", "course_title": "ARTIFICIAL INTELLGNC PROGRAMMING", "course_key": "1783"}, {"subject_code": "CS", "course_number": "1792", "course_id": "105811", "course_title": "COMPUTER OPERATING SYSTEMS", "course_key": "1792"}, {"subject_code": "CS", "course_number": "1900", "course_id": "105814", "course_title": "INTERNSHIP", "course_key": "1900"}, {"subject_code": "CS", "course_number": "1901", "course_id": "193035", "course_title": "INTERNSHIP", "course_key": "1901"}, {"subject_code": "CS", "course_number": "1902", "course_id": "105815", "course_title": "DIRECTED STUDY", "course_key": "1902"}, {"subject_code": "CS", "course_number": "1903", "course_id": "105816", "course_title": "INTERNSHIP", "course_key": "1903"}, {"subject_code": "CS", "course_number": "1904", "course_id": "105817", "course_title": "DIRECTED STUDY", "course_key": "1904"}, {"subject_code": "CS", "course_number": "1906", "course_id": "188561", "course_title": "COMPUTER SCIENCE COOPERATIVE PROGRAM", "course_key": "1906"}, {"subject_code": "CS", "course_number": "1950", "course_id": "105821", "course_title": "DIRECTED RESEARCH: CAPSTONE", "course_key": "1950"}, {"subject_code": "CS", "course_number": "1951", "course_id": "193683", "course_title": "DIRECTED RESEARCH", "course_key": "1951"}, {"subject_code": "CS", "course_number": "1980", "course_id": "184203", "course_title": "TEAM PROJECT DESIGN AND IMPLEMENTATION", "course_key": "1980"}, {"subject_code": "CS", "course_number": "2000", "course_id": "105822", "course_title": "MS THESIS RESEARCH", "course_key": "2000"}, {"subject_code": "CS", "course_number": "2001", "course_id": "105823", "course_title": "RESEARCH TOPICS/COMPUTER SCIENCE", "course_key": "2001"}, {"subject_code": "CS", "course_number": "2002", "course_id": "105824", "course_title": "RESEARCH EXPERIENCE/COMPUTER SCI", "course_key": "2002"}, {"subject_code": "CS", "course_number": "2003", "course_id": "184343", "course_title": "COMPUTER SCIENCE COLLOQUIUM", "course_key": "2003"}, {"subject_code": "CS", "course_number": "2012", "course_id": "178043", "course_title": "ALGORITHM DESIGN", "course_key": "2012"}, {"subject_code": "CS", "course_number": "2021", "course_id": "194486", "course_title": "STRUCTURED PROGRAMMING LANGUAGES", "course_key": "2021"}, {"subject_code": "CS", "course_number": "2032", "course_id": "197964", "course_title": "SOFTWARE QUALITY ASSURANCE", "course_key": "2032"}, {"subject_code": "CS", "course_number": "2035", "course_id": "194954", "course_title": "INTERFACE DESIGN METHODOLOGY", "course_key": "2035"}, {"subject_code": "CS", "course_number": "2037", "course_id": "194966", "course_title": "INTRODUCTION TO HUMAN-COMPUTER INTERACTION", "course_key": "2037"}, {"subject_code": "CS", "course_number": "2041", "course_id": "194138", "course_title": "INTRODUCTION TO COMPUTER ARCHITECTURE", "course_key": "2041"}, {"subject_code": "CS", "course_number": "2045", "course_id": "170705", "course_title": "INTRODUCTION TO HIGH PERFORMANCE COMPUTING SYSTEMS", "course_key": "2045"}, {"subject_code": "CS", "course_number": "2051", "course_id": "194967", "course_title": "ADVANCED SYSTEMS SOFTWARE", "course_key": "2051"}, {"subject_code": "CS", "course_number": "2052", "course_id": "197965", "course_title": "DATA COMMUNICATION AND COMPUTER NETWORKS", "course_key": "2052"}, {"subject_code": "CS", "course_number": "2053", "course_id": "171439", "course_title": "APPLIED CRYPTOGRAPHY AND NETWORK SECURITY", "course_key": "2053"}, {"subject_code": "CS", "course_number": "2055", "course_id": "177614", "course_title": "DATABASE MANAGEMENT SYSTEMS", "course_key": "2055"}, {"subject_code": "CS", "course_number": "2056", "course_id": "186908", "course_title": "INTRODUCTION TO DATA SCIENCE", "course_key": "2056"}, {"subject_code": "CS", "course_number": "2057", "course_id": "194139", "course_title": "PRIVACY IN THE ELECTRONIC SOCIETY", "course_key": "2057"}, {"subject_code": "CS", "course_number": "2060", "course_id": "194968", "course_title": "INTRODUCTION TO CLOUD COMPUTING", "course_key": "2060"}, {"subject_code": "CS", "course_number": "2071", "course_id": "194140", "course_title": "HUMAN LANGUAGE TECHNOLOGIES", "course_key": "2071"}, {"subject_code": "CS", "course_number": "2074", "course_id": "186930", "course_title": "INTRODUCTION TO COMPUTER VISION", "course_key": "2074"}, {"subject_code": "CS", "course_number": "2075", "course_id": "194487", "course_title": "INTRODUCTION TO MACHINE LEARNING", "course_key": "2075"}, {"subject_code": "CS", "course_number": "2078", "course_id": "192037", "course_title": "INTRODUCTION TO DEEP LEARNING", "course_key": "2078"}, {"subject_code": "CS", "course_number": "2084", "course_id": "194955", "course_title": "BIAS AND ETHICAL IMPLICATIONS IN ARTIFICIAL INTELLIGENCE", "course_key": "2084"}, {"subject_code": "CS", "course_number": "2099", "course_id": "198515", "course_title": "SPECIAL TOPICS IN COMPUTER SCIENCE", "course_key": "2099"}, {"subject_code": "CS", "course_number": "2110", "course_id": "105827", "course_title": "THEORY OF COMPUTATION", "course_key": "2110"}, {"subject_code": "CS", "course_number": "2150", "course_id": "105830", "course_title": "DESIGN & ANALYSIS OF ALGORITHMS", "course_key": "2150"}, {"subject_code": "CS", "course_number": "2210", "course_id": "105834", "course_title": "COMPILER DESIGN", "course_key": "2210"}, {"subject_code": "CS", "course_number": "2310", "course_id": "105838", "course_title": "SOFTWARE ENGINEERING", "course_key": "2310"}, {"subject_code": "CS", "course_number": "2410", "course_id": "105842", "course_title": "COMPUTER ARCHITECTURE", "course_key": "2410"}, {"subject_code": "CS", "course_number": "2510", "course_id": "105844", "course_title": "COMPUTER OPERATING SYSTEMS", "course_key": "2510"}, {"subject_code": "CS", "course_number": "2520", "course_id": "105847", "course_title": "WIDE AREA NETWORKS", "course_key": "2520"}, {"subject_code": "CS", "course_number": "2530", "course_id": "150231", "course_title": "COMPUTER AND NETWORK SECURITY", "course_key": "2530"}, {"subject_code": "CS", "course_number": "2550", "course_id": "105850", "course_title": "PRINCIPLES OF DATABASE SYSTEMS", "course_key": "2550"}, {"subject_code": "CS", "course_number": "2610", "course_id": "105856", "course_title": "INTERFACE DESIGN & EVALUATION", "course_key": "2610"}, {"subject_code": "CS", "course_number": "2620", "course_id": "177251", "course_title": "INTERDISCIPLINARY MODELING AND VISUALIZATION", "course_key": "2620"}, {"subject_code": "CS", "course_number": "2637", "course_id": "193001", "course_title": "FOUNDATIONS OF HUMAN-COMPUTER INTERACTION", "course_key": "2637"}, {"subject_code": "CS", "course_number": "2710", "course_id": "105858", "course_title": "FOUNDTNS OF ARTIFICIAL INTELLGNC", "course_key": "2710"}, {"subject_code": "CS", "course_number": "2731", "course_id": "105863", "course_title": "INTRO NATURAL LANGUAGE PROCSSNG", "course_key": "2731"}, {"subject_code": "CS", "course_number": "2750", "course_id": "105866", "course_title": "MACHINE LEARNING", "course_key": "2750"}, {"subject_code": "CS", "course_number": "2756", "course_id": "193002", "course_title": "PRINCIPLES OF DATA MINING", "course_key": "2756"}, {"subject_code": "CS", "course_number": "2770", "course_id": "187449", "course_title": "COMPUTER VISION", "course_key": "2770"}, {"subject_code": "CS", "course_number": "2900", "course_id": "105869", "course_title": "GRADUATE INTERNSHIP", "course_key": "2900"}, {"subject_code": "CS", "course_number": "2905", "course_id": "188576", "course_title": "COMPUTER SCIENCE COOPERATIVE PROGRAM", "course_key": "2905"}, {"subject_code": "CS", "course_number": "2910", "course_id": "105871", "course_title": "MS PROJECT", "course_key": "2910"}, {"subject_code": "CS", "course_number": "2990", "course_id": "105872", "course_title": "INDEPENDENT STUDY", "course_key": "2990"}, {"subject_code": "CS", "course_number": "3000", "course_id": "105873", "course_title": "RESEARCH AND DISSERTATION PHD", "course_key": "3000"}, {"subject_code": "CS", "course_number": "3150", "course_id": "105878", "course_title": "ADV TOPCS DSGN & ANALYS ALGORTHM", "course_key": "3150"}, {"subject_code": "CS", "course_number": "3210", "course_id": "105880", "course_title": "ADV TOPICS PROGRAMMING LANGUAGES", "course_key": "3210"}, {"subject_code": "CS", "course_number": "3220", "course_id": "105881", "course_title": "COMPILING TECHNQS/PARALLEL SYMS", "course_key": "3220"}, {"subject_code": "CS", "course_number": "3410", "course_id": "105887", "course_title": "ADV TOPICS COMPUTER ARCHITECTURE", "course_key": "3410"}, {"subject_code": "CS", "course_number": "3510", "course_id": "105890", "course_title": "ADV TOPICS IN OPERATING SYSTEMS", "course_key": "3510"}, {"subject_code": "CS", "course_number": "3521", "course_id": "105892", "course_title": "ADV TOPCS SENSING/UBIQUITOUS TEC", "course_key": "3521"}, {"subject_code": "CS", "course_number": "3525", "course_id": "178121", "course_title": "ADVANCED TOPICS IN SECURITY AND PRIVACY", "course_key": "3525"}, {"subject_code": "CS", "course_number": "3530", "course_id": "105893", "course_title": "ADV TOPCS DISTBD & REAL-TIME SYS", "course_key": "3530"}, {"subject_code": "CS", "course_number": "3550", "course_id": "105896", "course_title": "ADV TOPICS IN MANAGEMENT OF DATA", "course_key": "3550"}, {"subject_code": "CS", "course_number": "3551", "course_id": "105897", "course_title": "ADV TOPICS IN DISTBD INFOR SYS", "course_key": "3551"}, {"subject_code": "CS", "course_number": "3570", "course_id": "181858", "course_title": "ADVANCED TOPICS IN USER INTERFACE", "course_key": "3570"}, {"subject_code": "CS", "course_number": "3580", "course_id": "105901", "course_title": "SEM: ADV TOPC PARALLEL COMPUTING", "course_key": "3580"}, {"subject_code": "CS", "course_number": "3650", "course_id": "105905", "course_title": "VISUAL LANGUAGES AND PROGRAMMING", "course_key": "3650"}, {"subject_code": "CS", "course_number": "3710", "course_id": "105906", "course_title": "ADV TOPICS ARTIFICIAL INTELLGNC", "course_key": "3710"}, {"subject_code": "CS", "course_number": "3720", "course_id": "105907", "course_title": "ADVANCED TOPICS IN INTERNET OF THINGS", "course_key": "3720"}, {"subject_code": "CS", "course_number": "3730", "course_id": "105908", "course_title": "ADV TOPCS NATURAL LANG PROCSSNG", "course_key": "3730"}, {"subject_code": "CS", "course_number": "3750", "course_id": "105912", "course_title": "ADV TOPICS IN MACHINE LEARNING", "course_key": "3750"}, {"subject_code": "CS", "course_number": "3790", "course_id": "105914", "course_title": "ADVANCED TOPICS IN EDUCATIONAL TECHNOLOGY: PERSONALIZED LEARNING ENVIRONMENTS", "course_key": "3790"}, {"subject_code": "CS", "course_number": "3800", "course_id": "191493", "course_title": "ADVANCED TOPICS IN COMPUTING", "course_key": "3800"}, {"subject_code": "CS", "course_number": "3900", "course_id": "105915", "course_title": "PHD DIRECTED STUDY", "course_key": "3900"}
    all = []
    for c in all_courses:  # Assuming courses_taken is a list of dicts
        if int(c["course_number"]) >= 1503 and int(c["course_number"]) <= 1900:
            all.append(c)

    #print(all)
    #response = ask_gemini_to_generate_questions(all, courses_taken)
    answers = ["yes", "no", "yes", "no", "no"]
    #print(answers)
    #ask_gemini_for_recs(answers, response, all, courses_taken)

    # depending on what they select, we call pitt api with those classes to find professor
    classes_selected = [{"subject_code": "CS", "course_number": "1571", "course_id": "105780", "course_title": "INTRODUCTION TO ARTIFICIAL INTELLIGENCE", "course_key": "1571"}, {"subject_code": "CS", "course_number": "1613", "course_id": "194137", "course_title": "QUANTUM COMPUTATION", "course_key": "1613"}, {"subject_code": "CS", "course_number": "1621", "course_id": "105785", "course_title": "STRUCTURE PROGRAMMING LANGUAGES", "course_key": "1621"}, {"subject_code": "CS", "course_number": "0007", "course_id": "105611", "course_title": "INTRODUCTION TO COMPUTER PROGRAMMING", "course_key": "0007"}]


    #get_following_classes("2", classes_selected)
    
    print(classes_selected)

    result = collection.find_one({"_id": "66f8a064a9a540a0e41b1abb"})
    major_docs = collection.find({"Major": "CS"})

    for doc in major_docs:
        print(doc)

    for classes in doc['Requirements']:
        class_list = classes.split(" ") # required
        for courses in courses_taken:
            if is_in_class_selected(classes_selected, class_list[1]) and is_in_class_taken(courses_taken, class_list[1]): # if it is not in selected class & not in classes taken
                classes_selected.append(classes) # if they have a class they havent taken thats required we'll automatically add that to the classes they have to take
                break
    #print(cool[0])