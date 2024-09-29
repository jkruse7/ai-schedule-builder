import React, { useEffect, useState }  from "react";
import "../App.css";

function ScheduleDisplay({ selectedRecs, semsLeft, selectedCourses }) {

  const [schedule, setSchedule] = useState([]);

  const formatSchedule = (curSchedule) => {

    const groupedSchedule = curSchedule.reduce((acc, line) => {
      const linePieces = line.split(';');
      const key = linePieces[0];
      if (!acc[key]) {
        acc[key] = [];
      }
      acc[key].push(linePieces);
      return acc;
    }, {});

    return Object.keys(groupedSchedule).map((key, index) => (
      <div key={index} className="grid-card">
        <h3>{key}</h3>
        {groupedSchedule[key].map((linePieces, subIndex) => (
          <div key={subIndex}>
            <h5>{linePieces[1]}</h5>
            <div>
              <span>{linePieces[2]}</span>
            </div>
          </div>
        ))}
      </div>
    ));
  };

  useEffect(() => {
    const scheduleBody = JSON.stringify({
      "selected_recs": selectedRecs,
      "sems_left": semsLeft,
      "taken_courses": selectedCourses
    });
    fetch("http://localhost:5000/ai-schedule-builder/api/get/schedule", {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'Origin': 'http://localhost:3000',
      },
      body: scheduleBody
    }).then(response => {
      if (!response.ok) {
          throw new Error(response.message)
      }
      return response.json();
    }).then(data => {
      console.warn("unfort");
      console.warn(data.trim().split("\n"));
      setSchedule(data.trim().split("\n"));
    }).catch(error => {
        console.error(error);
    });
  }, [selectedRecs])

  return (
    <div className="schedule-container">
      <div className="schedule-header">
        <h2>Here's my recommendations!</h2>
      </div>
      <div className="schedule-grid-conrainer">
        {schedule.length === 0
          ? <label>Loading...</label>
          : (
            <div className="schedule-grid">{formatSchedule(schedule)}</div>
          )
        }
      </div>
    </div>
  );
}

export default ScheduleDisplay;