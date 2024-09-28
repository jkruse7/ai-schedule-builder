import './App.css';
import React from 'react';
import { useState } from 'react';
import StudentInputs from './components/StudentInputs';
import CoursesList from './components/CoursesList';

function App() {

  const [courses, setCourses] = useState([]);

  return (
    <div>
       <StudentInputs setCourses={setCourses}/>
       {courses.legnth > 0 && <CoursesList courses={courses}/>}
    </div>
  );
}

export default App;
