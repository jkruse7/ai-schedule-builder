import React, { useState, useEffect } from "react";

function CourseRecommendations({ answers, courses, selectedCourses, setSelectedRecs, setCurScreen }) {
    const [recomendations, setRecomendations] = useState("");
    const rec_answers = [];
    
    useEffect(() => {
        const recBody = JSON.stringify({
            q_and_a: answers,
            class_list: courses,
            taken_courses: selectedCourses
        });
        fetch("http://localhost:5000/ai-schedule-builder/api/get/recommendations", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000',
            },
            body: recBody
        }).then(response => {
            if (!response.ok) {
                throw new Error(response.message)
            }
            return response.json();
        }).then(data => {
            console.warn(data);
            const recsArray = data.trim().split("\n");
            setRecomendations(recsArray);
        }).catch(error => {
            console.error(error);
        });

    }, [answers]);


    const handleSubmit = (e) => {
        e.preventDefault();
        console.warn(rec_answers);
        setSelectedRecs(rec_answers);
        setCurScreen("SCHEDULE");
    };

    
    const handleChange = (curR) => {
        rec_answers.push(
            curR)
    };

    return (
        <div>
            {recomendations.length === 0 
                ? <label>Loading...</label>
                : (
                    <form onSubmit={handleSubmit}>
                        <ul>
                            {recomendations.map(curR => {
                                return (
                                    <div> 
                                        <input
                                            type="checkbox"
                                            name={curR}
                                            value={curR}
                                            onChange={() => handleChange(curR)}
                                        />
                                        <label>{curR}</label>
                                    </div>
                                )
                            })}
                        </ul>
                        <button type="submit">Submit All Answers</button>
                    </form>
                )
            }
        </div>
    );
}

export default CourseRecommendations;