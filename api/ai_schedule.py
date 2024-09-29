from flask import (
  Flask, request, jsonify, make_response, request
)
from flask_cors import CORS
from http import HTTPStatus
from utils.course_utils import get_courses_by_subject, get_cached_courses, ask_gemini_to_generate_questions, ask_gemini_for_recs
import json


app = Flask(__name__)
app.debug = True
CORS(app)


@app.route("/")
def hello_world():
  return "<p>Hello, world!</p>"

@app.route("/ai-schedule-builder/api/courses/get/<subject>", methods=["GET"])
def get_subject_courses(subject):
  if request.method == "OPTIONS":
        return make_response(jsonify({"message": "CORS preflight"}), HTTPStatus.OK)
  subject_courses = get_courses_by_subject(subject)
  # print(subject_courses)
  subject_courses = jsonify(subject_courses)
  return make_response(subject_courses, HTTPStatus.OK)

@app.route("/ai-schedule-builder/api/get/questions", methods=["GET","POST"])
def get_questions():
  if request.method == "OPTIONS":
    return make_response(jsonify({"message": "CORS preflight"}), HTTPStatus.OK)
  if not request.json["taken_courses"] or not request.json["major"]:
     return make_response(jsonify({"error": "Not enough parameter"}), HTTPStatus.BAD_REQUEST)
  print("whats up big dawg")
  taken_courses = request.json["taken_courses"]
  print(type(taken_courses))
  courses = get_cached_courses(request.json["major"])
  print(type(courses))

  questions = ask_gemini_to_generate_questions(courses, taken_courses)
  return make_response(jsonify(questions), HTTPStatus.OK)

@app.route("/ai-schedule-builder/api/get/recommendations", methods = ["GET", "POST"])
def get_recommendations():
   if request.method == "OPTIONS":
    return make_response(jsonify({"message": "CORS preflight"}), HTTPStatus.OK)
   if not request.json["taken_courses"] or not request.json["class_list"] or not request.json["q_and_a"]:
     return make_response(jsonify({"error": "Not enough parameter"}), HTTPStatus.BAD_REQUEST)
   q_and_a = request.json["q_and_a"]
   full_questions = ""
   for question in q_and_a:
      full_questions += question
   answers = q_and_a.items()
   class_list = request.json["class_list"]
   taken_courses = request.json["taken_courses"]
   recommendations = ask_gemini_for_recs(answers, full_questions, class_list, taken_courses)
   return make_response(jsonify(recommendations), HTTPStatus.OK)

if __name__ == "__main__":
  app.run(debug=True, port=5000)
  CORS(app=app)