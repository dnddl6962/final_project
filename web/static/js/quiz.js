// // const questionDisplay = document.getElementById('question-display');

// // document.addEventListener('DOMContentLoaded', function() {
// //     let currentQuestionId;
// //     let currentQuestionNum = 1; // 예시로 1로 시작합니다.
// //     let questionDisplay = document.getElementById('question-display');
    
// //     fetch('/get-question')
// //     .then(response => response.json())
// //     .then(data => {
// //         console.log(data);  // 전체 데이터 구조 확인
// //         const item_id = data.item_id;
// //         questionDisplay.textContent = `문제: ${item_id}`;
// //     })
// //     .catch(error => console.error('Error:', error));


// // // 버튼 참조
// // const oButton = document.getElementById('o-button');
// // const xButton = document.getElementById('x-button');

// // document.getElementById('o-button').addEventListener('click', function() {
// //     updateSelection(oButton);
// //     sendAnswer(true, currentQuestionNum, currentQuestionId); // 문제를 맞힘
// // });

// // document.getElementById('x-button').addEventListener('click', function() {
// //     updateSelection(xButton);
// //     sendAnswer(false, currentQuestionNum, currentQuestionId); // 문제를 틀림
// // });

// // document.getElementById('next-button').addEventListener('click', function() {
// //     loadNextQuestion(); // 다음 문제 로드
// // });



// // // 선택된 버튼 강조 및 다른 버튼의 강조 해제
// // function updateSelection(selectedButton) {
// //     // 먼저 모든 버튼에서 'selected' 클래스 제거
// //     oButton.classList.remove('selected');
// //     xButton.classList.remove('selected');
    
// //     // 선택된 버튼에만 'selected' 클래스 추가
// //     selectedButton.classList.add('selected');
// // }

// // function sendAnswer(answer, questionId) {
// //     // 서버로 응답을 전송하는 로직
// //     fetch('/submit-answer', {
// //         method: 'POST',
// //         headers: {
// //             'Content-Type': 'application/json',
// //         },
// //         body: JSON.stringify({
// //             answer: answer
// //         }),
// //     })
// //     .then(response => response.json())
// //     .then(data => {
// //         console.log('Response:', data);
        
// //         // 현재 문제 ID 업데이트
// //         currentQuestionId = data.next_item_id;
        
// //         // 새로운 문제 가져오기
// //         loadNextQuestion();
// //     })

// //     .catch(error => console.error('Error:', error));
// // }

// // function loadNextQuestion() {
// //     currentQuestionNum++; // 문제 번호를 업데이트
// //     // 다음 문제 데이터 로드 로직 (여기서는 간단히 문제 번호와 텍스트를 업데이트)
// //     document.getElementById('question-number').textContent = `${currentQuestionNum}번째 문제`;
// //     document.getElementById('question-text').textContent = '새로운 문제가 여기에 표시됩니다.';
    
// //     // 실제 애플리케이션에서는 여기에서 서버로부터 다음 문제 데이터를 요청하고,
// //     // 받아온 데이터로 문제 내용을 업데이트해야 합니다.
// // }



// // });



// document.addEventListener('DOMContentLoaded', function() {
//     let currentQuestionId;
//     let currentQuestionNum = 1; // 예시로 1로 시작합니다.
//     let questionDisplay = document.getElementById('question-display');
    
//     fetch('/get-question')
//     .then(response => response.json())
//     .then(data => {
//         console.log(data);  // 전체 데이터 구조 확인
//         const item_id = data.item_id;
//         questionDisplay.textContent = `문제: ${item_id}`;
//         currentQuestionId = item_id; // 현재 문제 ID를 설정
//     })
//     .catch(error => console.error('Error:', error));


// // 버튼 참조
// const oButton = document.getElementById('o-button');
// const xButton = document.getElementById('x-button');

// document.getElementById('o-button').addEventListener('click', function() {
//     updateSelection(oButton);
//     sendAnswer(true, currentQuestionId); // 문제를 맞힘
// });

// document.getElementById('x-button').addEventListener('click', function() {
//     updateSelection(xButton);
//     sendAnswer(false, currentQuestionId); // 문제를 틀림
// });


// // 선택된 버튼 강조 및 다른 버튼의 강조 해제
// function updateSelection(selectedButton) {
//     // 먼저 모든 버튼에서 'selected' 클래스 제거
//     oButton.classList.remove('selected');
//     xButton.classList.remove('selected');
    
//     // 선택된 버튼에만 'selected' 클래스 추가
//     selectedButton.classList.add('selected');
// }

// function sendAnswer(answer, questionId) {
//     // 서버로 응답을 전송하는 로직
//     fetch('/submit-answer', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             answer: answer,
//             currentQuestionId: questionId // 현재 문제 ID도 함께 전송
//         }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Response:', data);
//         if (!data.error) {
//             // 응답이 에러가 아닌 경우에만 처리
//             if (data.message) {
//                 console.log(data.message); // 서버로부터 받은 메시지 출력
//             }
//         } else {
//             console.error('Error:', data.error); // 에러가 발생한 경우 에러 메시지 출력
//         }
//     })
//     .catch(error => console.error('Error:', error)); // 네트워크 에러 등 예외 발생 시 에러 메시지 출력
// }

// function loadNextQuestion() {
//     currentQuestionNum++; // 문제 번호를 업데이트
//     document.getElementById('question-number').textContent = `${currentQuestionNum}번째 문제`;
//     fetch('/get-question')
//     .then(response => response.json())
//     .then(data => {
//         console.log(data);  // 전체 데이터 구조 확인
//         const nextItemId = data.item_id;
//         questionDisplay.textContent = `문제: ${nextItemId}`;
//         currentQuestionId = nextItemId; // 현재 문제 ID를 설정
        
//         // 마지막 문제인 경우
//         if (data.last_quiz) {
//             // 다음 문제 로드 버튼을 비활성화하거나 숨김 처리
//             document.getElementById('next-button').style.display = 'none';
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }

// document.getElementById('next-button').addEventListener('click', function() {
//     loadNextQuestion(); // 다음 문제 로드
// });

// });


////////////////////////////////////////////////////////////////////
// 다음을 누르지 않고 O나 X를 누를 때마다 응답이 전송되는 버그가 있음 / 값을 계속 전달해줄 수 있음
// (마지막 문제 이후에는 O나 X 버튼 눌러도 응답을 받지 않게끔 버그 수정해줘야 함)
document.addEventListener('DOMContentLoaded', function() {
    let currentQuestionId;
    let currentQuestionNum = 0; // 0으로 초기화
    let questionDisplay = document.getElementById('question-display');
    let lastQuiz = false; // 마지막 퀴즈 여부를 저장하는 변수

    function loadNextQuestion() {
        currentQuestionNum++; // 문제 번호를 업데이트
        document.getElementById('question-number').textContent = `${currentQuestionNum}번째 문제`;
        fetch('/get-question')
        .then(response => response.json())
        .then(data => {
            console.log(data);  // 전체 데이터 구조 확인
            const nextItemId = data.item_id;
            if (data.last_quiz) {
                lastQuiz = true;
            } else {
                questionDisplay.textContent = `문제: ${nextItemId}`;
                currentQuestionId = nextItemId; // 현재 문제 ID를 설정
            }
        })
        .catch(error => console.error('Error:', error));
    }

    document.getElementById('next-button').addEventListener('click', function() {
        if (!lastQuiz) {
            loadNextQuestion(); // 다음 문제 로드
            resetSelection(); // 선택된 상태 초기화
        }
    });

    const oButton = document.getElementById('o-button');
    const xButton = document.getElementById('x-button');

    function updateSelection(selectedButton) {
        // 먼저 모든 버튼에서 'selected' 클래스 제거
        oButton.classList.remove('selected');
        xButton.classList.remove('selected');
        
        // 선택된 버튼에만 'selected' 클래스 추가
        selectedButton.classList.add('selected');
    }

    oButton.addEventListener('click', function() {
        if (!lastQuiz) {
            updateSelection(oButton);
            sendAnswer(true, currentQuestionId); // 문제를 맞힘
        }
    });

    xButton.addEventListener('click', function() {
        if (!lastQuiz) {
            updateSelection(xButton);
            sendAnswer(false, currentQuestionId); // 문제를 틀림
        }
    });

    function sendAnswer(answer, questionId) {
        if (!lastQuiz) { // 마지막 퀴즈가 아닌 경우에만 응답을 전송합니다.
            // 서버로 응답을 전송하는 로직
            fetch('/submit-answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    answer: answer,
                    currentQuestionId: questionId // 현재 문제 ID도 함께 전송
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response:', data);
                if (!data.error) {
                    // 응답이 에러가 아닌 경우에만 처리
                    if (data.message) {
                        console.log(data.message); // 서버로부터 받은 메시지 출력
                    }
                    if (data.last_quiz) {
                        // 마지막 퀴즈일 경우 다음 버튼 숨기기
                        //document.getElementById('next-button').style.display = 'none';
                        alert("테스트가 완료되었습니다!");
                        window.location.href = '/result';
                        document.getElementById('result').addEventListener('click', testResult);
                    }
                } else {
                    console.error('Error:', data.error); // 에러가 발생한 경우 에러 메시지 출력
                }
            })
            .catch(error => console.error('Error:', error)); // 네트워크 에러 등 예외 발생 시 에러 메시지 출력
        }
    }

    function resetSelection() {
        // 모든 버튼에서 'selected' 클래스 제거
        oButton.classList.remove('selected');
        xButton.classList.remove('selected');
    }

    // 페이지 로드 시 첫 번째 문제 로드
    loadNextQuestion();
});
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
// 12번째 문제(마지막 문제)에서 13번째 문제 페이지로 넘어갈 수 있음
// document.addEventListener('DOMContentLoaded', function() {
//     let currentQuestionId;
//     let currentQuestionNum = 0; // 0으로 초기화
//     let questionDisplay = document.getElementById('question-display');
//     let lastQuiz = false; // 마지막 퀴즈 여부를 저장하는 변수

//     function loadNextQuestion() {
//         currentQuestionNum++; // 문제 번호를 업데이트
//         document.getElementById('question-number').textContent = `${currentQuestionNum}번째 문제`;
//         fetch('/get-question')
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);  // 전체 데이터 구조 확인
//             const nextItemId = data.item_id;
//             if (data.last_quiz) {
//                 // 마지막 퀴즈인 경우 퀴즈 영역을 숨깁니다.
//                 document.getElementById('quiz-container').style.display = 'none';
//                 lastQuiz = true;
//             } else {
//                 questionDisplay.textContent = `문제: ${nextItemId}`;
//                 currentQuestionId = nextItemId; // 현재 문제 ID를 설정
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     }

//     document.getElementById('next-button').addEventListener('click', function() {
//         if (!lastQuiz) {
//             loadNextQuestion(); // 다음 문제 로드
//             // 여기서 이전에 선택한 'o'나 'x'에 대한 응답을 전송
//             const selectedButton = document.querySelector('.selected');
//             if (selectedButton) {
//                 const isCorrect = selectedButton === document.getElementById('o-button');
//                 const questionId = currentQuestionId;
//                 sendAnswer(isCorrect, questionId);
//             }
//         }
//     });

//     const oButton = document.getElementById('o-button');
//     const xButton = document.getElementById('x-button');

//     function updateSelection(selectedButton) {
//         // 먼저 모든 버튼에서 'selected' 클래스 제거
//         oButton.classList.remove('selected');
//         xButton.classList.remove('selected');
        
//         // 선택된 버튼에만 'selected' 클래스 추가
//         selectedButton.classList.add('selected');
//     }

//     oButton.addEventListener('click', function() {
//         if (!lastQuiz) {
//             updateSelection(oButton);
//         }
//     });

//     xButton.addEventListener('click', function() {
//         if (!lastQuiz) {
//             updateSelection(xButton);
//         }
//     });

//     function sendAnswer(answer, questionId) {
//         // 서버로 응답을 전송하는 로직
//         fetch('/submit-answer', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 answer: answer,
//                 currentQuestionId: questionId // 현재 문제 ID도 함께 전송
//             }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log('Response:', data);
//             if (!data.error) {
//                 // 응답이 에러가 아닌 경우에만 처리
//                 if (data.message) {
//                     console.log(data.message); // 서버로부터 받은 메시지 출력
//                 }
//                 if (data.last_quiz) {
//                     // 마지막 퀴즈일 경우 다음 버튼 숨기기
//                     document.getElementById('next-button').style.display = 'none';
//                 }
//             } else {
//                 console.error('Error:', data.error); // 에러가 발생한 경우 에러 메시지 출력
//             }
//         })
//         .catch(error => console.error('Error:', error)); // 네트워크 에러 등 예외 발생 시 에러 메시지 출력
//     }

//     // 페이지 로드 시 첫 번째 문제 로드
//     loadNextQuestion();
// });
////////////////////////////////////////////////////////////////////