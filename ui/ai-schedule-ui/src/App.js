import './App.css';
import React from 'react';
import { useState } from 'react';
import StudentInputs from './components/StudentInputs';
import CoursesList from './components/CoursesList';

function App() {

  const [courses, setCourses] = useState([]);
  const [selectedCourses, setSelectedCourses] = useState([]);

  return (
    <div>
       <StudentInputs setCourses={setCourses} selectedCourse={selectedCourses}/>
       {selectedCourses.length != 0 && <button>Submit</button>}
       {courses.length > 0 && <CoursesList courses={courses} selectedCourses={selectedCourses} setSelectedCourses={setSelectedCourses}/>}
    </div>
  );
}

export default App;
