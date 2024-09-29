import React, { useEffect, useState }  from "react";

function ScheduleDisplay({ selectedRecs, semsLeft }) {

  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    const scheduleBody = JSON.stringify({
      "selected_recs": selectedRecs,
      "sems_left": semsLeft
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
        console.warn(data);
        console.warn(typeof data);
        data.trim().split("\n").forEach(sem => schedule.push(sem));
        console.warn(schedule);
    }).catch(error => {
        console.error(error);
    });

  }, [selectedRecs])

  return (
    <div>
      {schedule.length === 0
        ? <label>Loading...</label>
        : (
          <div>
            {schedule.map(cur => {
              <div>{cur}</div>
            })}
          </div>
        )
      }
    </div>
  );
}

export default ScheduleDisplay;