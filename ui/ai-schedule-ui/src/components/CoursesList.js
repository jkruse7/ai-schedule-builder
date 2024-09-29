import React from "react";
import { useState } from "react";
import SelectableListItem from "./SelectedableListItem";
import '../App.css';

function CoursesList({ courses, selectedCourses, setSelectedCourses }) {

  if (courses === undefined || courses.length === 0) {
    return;
  }

  return (
    <div className="courselist-container">
      <ul>
        {courses.map(course => <SelectableListItem course={course} selectedCourses={selectedCourses} setSelectedCourses={setSelectedCourses}/>)}
      </ul>
    </div>
  );
}

export default CoursesList;