import React, { useState, useEffect } from "react";

function CourseRecommendations({ answers, courses, selectedCourses }) {
    const [recomendations, setRecomendations] = useState("");
    
    useEffect(() => {
        const recBody = JSON.stringify({
            q_and_a: answers,
            class_list: courses,
            taken_courses: selectedCourses
        });
        fetch("http://localhost:5000/ai-schedule-builder/api/get/recommendations", {
            method: 'GET',
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
        }).catch(error => {
            console.error(data);
        });

    }, [answers]);

    return (
        <div>
            {recomendations.length === 0 
                ? <label>Loading...</label>
                : <label>good shit brother</label>
            }
        </div>
    );
}

export default CourseRecommendations;