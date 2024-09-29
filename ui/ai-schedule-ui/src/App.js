import './App.css';
import logo from './assets/al-logo.png';
import React from 'react';
import { useState } from 'react';
import StudentInputs from './components/StudentInputs';
import CoursesList from './components/CoursesList';
import QuestionsDisplay from './components/QuestionsDisplay';
import CourseRecommendations from './components/CourseRecommendations';
import ScheduleDisplay from './components/ScheduleDisplay';

function App() {
  const [semsLeft, setSemsLeft] = useState("");
  const [major, setMajor] = useState("")
  const [courses, setCourses] = useState([]);
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [curScreen, setCurScreen] = useState("HOME");
  const [answers, setAnswers] = useState([]);
  const [selectedRecs, setSelectedRecs] = useState([]);

  const changeScreen = (type) => {
    setCurScreen(type)
  };

  if (curScreen === "QUESTIONS") {
    return (
      <div>
        <QuestionsDisplay courses={courses} selectedCourses={selectedCourses} major={major} setAnswers={setAnswers} setCurScreen={setCurScreen}/>
      </div>
    );
  }
  else if (curScreen === "COURSES") {
    return (
      <div>
        <CourseRecommendations answers={answers} courses={courses} selectedCourses={selectedCourses} setSelectedRecs={setSelectedRecs} setCurScreen={setCurScreen}/>
      </div>
    );
  }
  else if (curScreen === "SCHEDULE") {
    return (
      <div>
        <header className='app-header'>
          <img src={logo}/>
        </header>
        <ScheduleDisplay
          selectedRecs={selectedRecs}
          semsLeft={semsLeft}
        />
      </div>
    )
  }

  return (
    
    <div className='main-container'>
      <header className='app-header'>
        <img src={logo}/>
        <h1 className='app-header-title'>AL-Genda</h1>
      </header>
      <div className='header'>
       <h1>Hi! I'm Al!</h1><br/>
       <h3>I will be your trusty guide to naviagting Pitt classes</h3>
       <p>This is what this does ....</p>
       <div className='special-side'><h2>Get Started!</h2></div>
       
       </div>
       <div className='questions'>
      
       <StudentInputs 
        setCourses={setCourses}
        selectedCourse={selectedCourses}
        major={major}
        setMajor={setMajor}
        semsLeft={semsLeft}
        setSemsLeft={setSemsLeft}
       />
      {selectedCourses.length != 0 && <button id='generate-questions' onClick={()=>changeScreen("QUESTIONS")}>Generate Questions</button>}
       {courses.length > 0 && <CoursesList courses={courses} selectedCourses={selectedCourses} setSelectedCourses={setSelectedCourses}/>}
       </div>
       
    </div>
  );
}

export default App;
