import React, { useEffect } from "react";
import { useState } from "react";

function QuestionsDisplay({courses, selectedCourses, major}) {

    const [questions, setQuestions] = useState([]);


    useEffect(() => {
        const questionsBody = JSON.stringify(questions);
        fetch("http://localhost:5000/ai-schedule-builder/api/get/questions", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000',
            },
            body: {
                'taken_courses': questionsBody,
                "major": 'CS' 
            }
             
        }).then(response => {
            if(!response.ok){
                console.error("rip");
            }
            return response.json();
        }).then(data => {
            console.warn(data);
        })

    }, []);

    return (
        <div>
            {questions.length === 0
                ?<label>Loading...</label>
                :<ul></ul>
            }
        </div>
    )

}
export default QuestionsDisplay;