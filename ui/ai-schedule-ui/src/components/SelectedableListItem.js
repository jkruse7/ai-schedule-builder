import React from "react";
import { useState } from "react";

function SelectableListItem({ course, selectedCourses }) {

  const [added, setAdded] = useState(false);

  const addToList = () => {
    if (added === true) {
      const idx = selectedCourses.indexOf(course);
      if (idx > -1) {
        selectedCourses.splice(idx, 1);
      }
    }
    else {
      selectedCourses.push(course);
    }
    setAdded(!added);
    console.warn(selectedCourses);
  };
  
  return (
    <li>
        {added === false 
          ? <button onClick={addToList}>Add</button>
          : <button onClick={addToList}>Remove</button>
        }
        <label>{course.subject_code}{course.course_key} {course.course_title}</label>
    </li>
  );
}

export default SelectableListItem;