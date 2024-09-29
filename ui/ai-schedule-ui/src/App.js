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
        <header className='app-header'>
          <img src={logo}/>
          <h1 className='app-header-title'>AL-Genda</h1>
        </header>
        <QuestionsDisplay courses={courses} selectedCourses={selectedCourses} major={major} setAnswers={setAnswers} setCurScreen={setCurScreen}/>
      </div>
    );
  }
  else if (curScreen === "COURSES") {
    return (
      <div>
        <header className='app-header'>
          <img src={logo}/>
          <h1 className='app-header-title'>AL-Genda</h1>
        </header>
        <CourseRecommendations answers={answers} courses={courses} selectedCourses={selectedCourses} setSelectedRecs={setSelectedRecs} setCurScreen={setCurScreen}/>
      </div>
    );
  }
  else if (curScreen === "SCHEDULE") {
    return (
      <div>
        <header className='app-header'>
          <img src={logo}/>
          <h1 className='app-header-title'>AL-Genda</h1>
        </header>
        <ScheduleDisplay
          selectedRecs={selectedRecs}
          semsLeft={semsLeft}
          selectedCourses={selectedCourses}
        />
      </div>
    )
  }

  return (
    <div>
      <header className='app-header'>
        <img src={logo}/>
        <h1 className='app-header-title'>AL-Genda</h1>
      </header>
      <div className='header'>
       <h1>Hi! I'm Al!</h1>
       <h3>I will be your trusty guide to navigating Pitt classes</h3>
       <div className='home-page-grid'>
        <p>After giving AIgenda your major, the semesters you have left, and the classes you have already taken, AIgenda generates questions for you to answer to gauge your interests. Once hearing from you, AIgenda, outputs a list of recommended classes you can take. After you select those that interest you, AIgenda clusters those classes into different semesters based on the difficulty of the class and the time you have left. </p>
        
         <div className='questions'>
          <StudentInputs 
          setCourses={setCourses}
          selectedCourse={selectedCourses}
          major={major}
          setMajor={setMajor}
          semsLeft={semsLeft}
          setSemsLeft={setSemsLeft}
          />
         </div>
        </div>
        {selectedCourses.length != 0 && <button id='generate-questions' onClick={()=>changeScreen("QUESTIONS")}>Generate Questions</button>}
        </div>
        <div className='courselist-container'>
          {courses.length > 0 && <CoursesList courses={courses} selectedCourses={selectedCourses} setSelectedCourses={setSelectedCourses}/>}
        </div>
    </div>
  );
}

export default App;
