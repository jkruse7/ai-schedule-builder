import '../App.css';
import React from "react";
import { useState, useEffect, useRef } from "react";

function StudentInputs({ setCourses, selectedCourses, major, setMajor, semsLeft, setSemsLeft }) {
  const [error, setError] = useState(null);

  const prevMajor = useRef("");
  const prevSemsLeft = useRef("");

  useEffect(() => {
    prevMajor.current = major;
    prevSemsLeft.current = semsLeft;
  }, [major, semsLeft]);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`http://localhost:5000/ai-schedule-builder/api/courses/get/${major}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000',
      }
    }).then(response => {
      console.warn(response);
      if (!response.ok) {
        throw new Error(`Unable to retrieve courses for ${major}`);
      }
      return response.json();
    }).then(data => {
      setError(null);
      setCourses(data);
      console.warn(data);
    }).catch(error => {
      console.error("you fool");
      console.error(error);
      setError(error.message)
    });
  };

  const resetInputs = (e) => {
    setMajor("");
    setSemsLeft("");
    setCourses([]);
    selectedCourses = [];
  };

  return (
    <div className='home-page-grid'>
      <form onSubmit={handleSubmit}>
        <div className="home-input">
        <label>What is your major?&emsp;   
          <input
            type="text"
            value={major}
            onChange={(e) => setMajor(e.target.value)}
          />
          <br></br>
        </label>
        <label>How many semesters do you have left?&emsp;
          <input
            type="number"
            value={semsLeft}
            onChange={(e) => setSemsLeft(e.target.value)}
          />
          
          <br></br>
        </label>
        </div>
        <div className="home-button">
        <button className='submit-btn' type="submit">Submit</button>
        </div >
        {error !== null && <label>Error: {error}</label>}
      </form>
      <br/>
      <div className="home-button">
      <button className='reset-btn' onClick={resetInputs}>Reset Inputs</button>
      </div>
    </div>
  );
}

export default StudentInputs;