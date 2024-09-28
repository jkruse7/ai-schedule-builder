import React from "react";
import { useState } from "react";

function StudentInputs({ setCourses }) {
  const [major, setMajor] = useState("");
  const [semsLeft, setSemsLeft] = useState("");
  const [error, setError] = useState(null);

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
    }).catch(error => {
      console.error("you fool");
      console.error(error);
      setError(error.message)
    });
  };

  const resetInputs = (e) => {
    setMajor("");
    setSemsLeft("");
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>What is your major?
          <input
            type="text"
            value={major}
            onChange={(e) => setMajor(e.target.value)}
          />
        </label>
        <label>How many semesters do you have left?
          <input
            type="number"
            value={semsLeft}
            onChange={(e) => setSemsLeft(e.target.value)}
          />
        </label>
        <button type="submit">Submit</button>
        {error !== null && <label>Error: {error}</label>}
      </form>
      <button onClick={resetInputs}>Reset Inputs</button>
    </div>
  );
}

export default StudentInputs;