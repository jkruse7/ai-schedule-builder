import React from "react";
import { useState } from "react";

function SelectableListItem({ course, selectedCourses, setSelectedCourses }) {

  const [added, setAdded] = useState(false);

  const addToList = () => {
    const currentSelect = selectedCourses;
    if (added === true) {
      const idx = currentSelect.indexOf(course);
      if (idx > -1) {
        currentSelect.splice(idx, 1);
      }
    }
    else {
      currentSelect.push(course);
    }
    console.warn(setSelectedCourses);
    setSelectedCourses(currentSelect);
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