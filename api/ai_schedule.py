from flask import (
  Flask, request, jsonify, make_response, request
)
from flask_cors import CORS
from http import HTTPStatus

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
  print(subject)
  response, code = "", -1
  course1 = { 
    "subject": "CS", 
    "couse_code": "0007",
    "course_name": "Introduction to Computer Programming"
  };
  course2 = { 
    "subject": "CS", 
    "couse_code": "1550",
    "course_name": "Introduction to Operating Systems"
  };
  response = jsonify(course1, course2)
  code = HTTPStatus.OK
  return make_response(response), code

if __name__ == "__main__":
  app.run(debug=True, port=5000)
  CORS(app=app)