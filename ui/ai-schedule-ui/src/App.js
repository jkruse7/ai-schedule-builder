import './App.css';
import React from 'react';
import { useState } from 'react';
import StudentInputs from './components/StudentInputs';
import CoursesList from './components/CoursesList';

function App() {

  const [courses, setCourses] = useState([]);
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [curScreen, setCurScreen] = useState("HOME");

  const changeScreen = (type) => {
    setCurScreen(type)
  };

  if (curScreen === "QUESTIONS") {
    console.warn("switvhing");
    return (
      <div>

      </div>
    )
  }

  return (
    <div>
       <StudentInputs setCourses={setCourses} selectedCourse={selectedCourses}/>
      {selectedCourses.length != 0 && <button id='generate-questions' onClick={changeScreen("QUESTIONS")}>Generate Questions</button>}
       {courses.length > 0 && <CoursesList courses={courses} selectedCourses={selectedCourses} setSelectedCourses={setSelectedCourses}/>}
    </div>
  );
}

export default App;
