import React from "react";
import { useState } from "react";
import SelectableListItem from "./SelectedableListItem";

function CoursesList({ courses, selectedCourses, setSelectedCourses }) {

  if (courses === undefined || courses.length === 0) {
    return;
  }

  return (
    <ul>
      {courses.map(course => <SelectableListItem course={course} selectedCourses={selectedCourses} setSelectedCourses={setSelectedCourses}/>)}
    </ul>
  );
}

export default CoursesList;