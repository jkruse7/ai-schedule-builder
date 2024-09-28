import React from "react";
import { useState } from "react";

function SelectableListItem({ course, selectedCourses, setSelectedCourses }) {

  const [added, setAdded] = useState(false);

  const addToList = () => {
    let currentSelect = [...selectedCourses];
    if (added) {
      currentSelect = currentSelect.filter(item => item !== course);
    } else {
      currentSelect.push(course);
    }
    setSelectedCourses(currentSelect);
    setAdded(!added);
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