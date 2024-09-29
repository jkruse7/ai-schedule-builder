import './App.css';
import React from 'react';
import { useState } from 'react';
import StudentInputs from './components/StudentInputs';
import CoursesList from './components/CoursesList';
import QuestionsDisplay from './components/QuestionsDisplay';
import CourseRecommendations from './components/CourseRecommendations';

function App() {

  const [courses, setCourses] = useState([]);
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [curScreen, setCurScreen] = useState("HOME");
  const [answers, setAnswers] = useState([]);

  const changeScreen = (type) => {
    setCurScreen(type)
  };

  if (curScreen === "QUESTIONS") {
    return (
      <div>
        <QuestionsDisplay courses={courses} selectedCourses={selectedCourses} major={"CS"} setAnswers={setAnswers} setCurScreen={setCurScreen}/>
      </div>
    );
  }
  else if (curScreen === "COURSES") {
    return (
      <div>
        <CourseRecommendations answers={answers} courses={courses} selectedCourses={selectedCourses}/>
      </div>
    );
  }

  return (
    <div>
       <StudentInputs setCourses={setCourses} selectedCourse={selectedCourses}/>
      {selectedCourses.length != 0 && <button id='generate-questions' onClick={()=>changeScreen("QUESTIONS")}>Generate Questions</button>}
       {courses.length > 0 && <CoursesList courses={courses} selectedCourses={selectedCourses} setSelectedCourses={setSelectedCourses}/>}
    </div>
  );
}

export default App;
