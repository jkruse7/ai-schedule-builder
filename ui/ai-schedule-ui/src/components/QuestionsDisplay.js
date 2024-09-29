import React, { useEffect } from "react";
import { useState } from "react";

function QuestionsDisplay({courses, selectedCourses, major, setAnswers, setCurScreen}) {

    const [questions, setQuestions] = useState([]);
    const answers = [];

    useEffect(() => {
        const questionsBody = JSON.stringify({
            taken_courses: selectedCourses,
            major: major
        });
        fetch("http://localhost:5000/ai-schedule-builder/api/get/questions", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000',
            },
            body: questionsBody
        }).then(response => {
            if(!response.ok){
                console.error(response.status);
                throw new Error(response.error);
            }
            return response.json();
        }).then(data => {
            console.warn(data);
            const questionsArray = data.trim().split("\n");
            setQuestions(questionsArray);
        }).catch(error => {
            console.error(error);
        })

    }, [selectedCourses]);

    const handleChange = (curQ, answer) => {
        answers.push({
            question: curQ,
            answer: answer
        })
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.warn(answers);
        setAnswers(answers);
        setCurScreen("COURSES");
    };

    return (
        <div>
            {questions.length === 0
                ?<label>Loading...</label>
                : (
                    <form onSubmit={handleSubmit}>
                        <ul>
                            {questions.map(curQ => {
                                return (
                                    <li key={curQ}>
                                        <label>{curQ}</label>
                                        <div> 
                                            <input
                                                type="radio"
                                                name={curQ}
                                                value="Yes"
                                                onChange={() => handleChange(curQ, "Yes")}
                                            />
                                            <label>Yes</label>
                                            <input
                                                type="radio"
                                                name={curQ}
                                                value="No"
                                                onChange={() => handleChange(curQ, "No")}
                                            />
                                            <label>No</label>
                                        </div>
                                    </li>
                                )
                            })}
                        </ul>
                        <button type="submit">Submit All Answers</button>
                    </form>
                )
            }
        </div>
    )

}
export default QuestionsDisplay;