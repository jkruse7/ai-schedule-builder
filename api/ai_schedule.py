from flask import (
  Flask, request, jsonify, make_response, request
)
from flask_cors import CORS
from http import HTTPStatus
from utils.course_utils import get_courses_by_subject, get_cached_courses
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
  taken_courses = request.json["taken_courses"]
  courses = get_cached_courses(request.json["major"])
  #ruchis function here
  questions = 'temp'
  return make_response(jsonify(questions), HTTPStatus.OK)

if __name__ == "__main__":
  app.run(debug=True, port=5000)
  CORS(app=app)