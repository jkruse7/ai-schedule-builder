import React from "react";
import { useState } from "react";

function StudentInputs() {
  const [major, setMajor] = useState("");
  const [majorError, setMajorError] = useState(null);
  const [semsLeft, setSemsLeft] = useState("");
  const [semsError, setSemsError] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`http://localhost:5000/ai-schedule-builder/api/courses/get/${major}`, {
      method: 'POST',
      
    })
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
        {majorError !== null && <label>Error: {majorError}</label>}
        <label>How many semesters do you have left?
          <input
            type="number"
            value={semsLeft}
            onChange={(e) => setSemsLeft(e.target.value)}
          />
        </label>
        {semsError !== null && <label>Error: {semsError}</label>}
        <button type="submit">Submit</button>
      </form>
      <button onClick={resetInputs}>Reset Inputs</button>
    </div>
  );
}

export default StudentInputs;