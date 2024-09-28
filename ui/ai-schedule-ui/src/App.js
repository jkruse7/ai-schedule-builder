import './App.css';
import React from 'react';
import { useState } from 'react';
import StudentInputs from './components/StudentInputs';
import CoursesList from './components/CoursesList';

function App() {

  const [courses, setCourses] = useState([]);
  const selectedCourses = [];

  return (
    <div>
       <StudentInputs setCourses={setCourses} selectedCourse={selectedCourses}/>
       {courses.length > 0 && <CoursesList courses={courses} selectedCourses={selectedCourses}/>}
    </div>
  );
}

export default App;
