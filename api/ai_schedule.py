from flask import (
  Flask, request, jsonify, make_response, request
)
from flask_cors import CORS
from http import HTTPStatus
from utils.course_utils import get_courses_by_subject

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
  response, code = "", -1
  subject_courses = get_courses_by_subject("CS")
  subject_courses = jsonify(subject_courses)
  code = HTTPStatus.OK
  return make_response(subject_courses), code

if __name__ == "__main__":
  app.run(debug=True, port=5000)
  CORS(app=app)