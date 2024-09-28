import React from "react";
import { useState } from "react";

function CoursesList({ courses }) {

  console.log("here");

  const createCourseListItems = (course) => {
    return (
      <li>
        <label>{course.subject}{course.course_code}</label>
        <label>{course.course_name}</label>
      </li>
    );
  };

  if (courses === undefined || courses.length === 0) {
    return;
  }

  return (
    <ul>
      {courses.map(course => createCourseListItems(course))}
    </ul>
  );
}

export default CoursesList;