// document.getElementById('o-button').addEventListener('click', function() {
//     sendAnswer(true); // 맞다고 응답
// });

// document.getElementById('x-button').addEventListener('click', function() {
//     sendAnswer(false); // 틀렸다고 응답
// });
// function sendAnswer(isCorrect) {
//     fetch('/submit-answer', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             answer: isCorrect
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         // 서버로부터 받은 응답으로 UI를 업데이트
//         console.log(data);
//         displayNextQuestion(data.next_question);
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });

//     function displayNextQuestion(questionData) {
//         // 문제 데이터를 사용하여 페이지에 다음 문제를 표시하는 로직
//         // 예: 문제 텍스트, 선택지 등을 업데이트
//         // 문제 텍스트 업데이트
//     const questionTextElement = document.getElementById('question-text');
//     questionTextElement.textContent = questionData.questionText;

//     // 선택지 업데이트
//     const optionsContainer = document.getElementById('options-container');
//     optionsContainer.innerHTML = ''; // 이전 선택지를 모두 제거
//     questionData.options.forEach((option, index) => {
//         const optionButton = document.createElement('button');
//         optionButton.textContent = option;
//         optionButton.addEventListener('click', () => {
//             sendAnswer(index); // 선택지를 클릭할 때마다 해당 인덱스를 서버로 보냄
//         });
//         optionsContainer.appendChild(optionButton);
//     });
//     }
// }

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('o-button').addEventListener('click', function() {
        sendAnswer(true); // 맞다고 응답
    });

    document.getElementById('x-button').addEventListener('click', function() {
        sendAnswer(false); // 틀렸다고 응답
    });
});

function sendAnswer(isCorrect) {
    fetch('/submit-answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            answer: isCorrect
        })
    })
    .then(response => response.json())
    .then(data => {
        // 서버로부터 받은 응답으로 UI를 업데이트
        console.log(data);
        displayNextQuestion(data.next_question);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayNextQuestion(questionData) {
    // 문제 데이터를 사용하여 페이지에 다음 문제를 표시하는 로직
    // 예: 문제 텍스트, 선택지 등을 업데이트
    const questionTextElement = document.getElementById('question-text');
    if (questionTextElement) {
        questionTextElement.textContent = questionData.questionText;

        // 선택지 업데이트
        const optionsContainer = document.getElementById('options-container');
        optionsContainer.innerHTML = ''; // 이전 선택지를 모두 제거
        questionData.options.forEach((option, index) => {
            const optionButton = document.createElement('button');
            optionButton.textContent = option;
            optionButton.addEventListener('click', () => {
                sendAnswer(index); // 선택지를 클릭할 때마다 해당 인덱스를 서버로 보냄
            });
            optionsContainer.appendChild(optionButton);
        });
    } else {
        console.error('Question text element not found.');
    }
}
