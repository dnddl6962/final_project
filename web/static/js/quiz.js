document.addEventListener('DOMContentLoaded', function() {
    let currentQuestionId;
    let currentQuestionNum = 0; // 0으로 초기화
    let questionDisplay = document.getElementById('question-display');
    let lastQuiz = false; // 마지막 퀴즈 여부를 저장하는 변수
    let userHasSelected = false;
    let selectedAnswer = null;// 사용자가 선택한 답변을 임시 저장할 변수
    let currentProficiency; // 현재 학습 능력을 임시 저장할 변수

    function loadNextQuestion() {
        currentQuestionNum++; // 문제 번호를 업데이트
        document.getElementById('question-number').textContent = `${currentQuestionNum}번째 문제`;

        // 현재 학습 능력을 화면에 업데이트
        if (currentProficiency !== undefined) {
            const proficiency = document.getElementById('proficiency');
            if(currentProficiency == 0){
                proficiency.textContent = '초기 사용자 능력치 측정을 위한 문제입니다.'
            }
            else{
                proficiency.textContent = `현재 학습 능력: ${currentProficiency}`;
            }
            currentProficiency = undefined; // 학습 능력치 초기화
        }


        fetch('/get-question')
        .then(response => response.json())
        .then(data => {
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
    document.getElementById('submit-button').addEventListener('click', function() {
        
         // 사용자가 선택하지 않았다면 경고를 표시하고 함수 종료.
         if (!userHasSelected) {
            
            alert('답변을 선택해주세요!');
            return;
        }
        if (!lastQuiz) {
            updateSelection(submitButton);
            userHasSelected = true;
            sendAnswer(selectedAnswer, currentQuestionId); // 여기에서 선택한 답변을 전송

        }
    }
    );


    document.getElementById('next-button').addEventListener('click', function() {
        // 사용자가 선택하지 않았다면 경고를 표시하고 함수 종료.
        if (!userHasSelected) {
            alert('답변을 선택해주세요!');
            return;
        }
        
        if (!lastQuiz) {
            loadNextQuestion(); // 다음 문제 로드
            resetSelection(); // 선택된 상태 초기화
            userHasSelected = false; // 사용자 선택 상태 초기화
            selectedAnswer = null; // 선택한 답변 초기화
        }
    });

    const submitButton = document.getElementById('submit-button');
    const oButton = document.getElementById('o-button');
    const xButton = document.getElementById('x-button');

    function updateSelection(selectedButton) {
        userHasSelected = true;
        // 먼저 모든 버튼에서 'selected' 클래스 제거
        oButton.classList.remove('selected');
        xButton.classList.remove('selected');
        submitButton.classList.remove('selected');
        
        // 선택된 버튼에만 'selected' 클래스 추가
        selectedButton.classList.add('selected');
    }

    oButton.addEventListener('click', function() {
        if (!lastQuiz) {
            updateSelection(oButton);
            selectedAnswer = true; // 사용자가 "O"를 선택한 것으로 저장
            userHasSelected = true; // 답변이 선택되었다고 표시
        }
    });

    xButton.addEventListener('click', function() {
        if (!lastQuiz) {
            updateSelection(xButton);
            selectedAnswer = false; // 사용자가 "X"를 선택한 것으로 저장
            userHasSelected = true; // 답변이 선택되었다고 표시
        }
    });

    function sendAnswer(answer, questionId) {
        if (!lastQuiz ) { // 마지막 퀴즈가 아닌 경우에만 응답 전송.
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
                setTimeout(() => {
                    if (!data.error) {
                        // 응답이 에러가 아닌 경우에만 처리
                        // 응답 성공 시, 현재 학습 능력치 업데이트
                        currentProficiency = data.estimated_proficiency;
                        if (data.message) {
                            console.log(data.message); // 서버로부터 받은 메시지 출력
                        }
                        
                        if (data.last_quiz) {
                            // 마지막 퀴즈일 경우 다음 버튼 숨기기
                            alert("테스트가 완료되었습니다!");
                            window.location.href = '/result';
                            document.getElementById('result').addEventListener('click', testResult);
                        }
                    } else {
                        console.error('Error:', data.error); // 에러가 발생한 경우 에러 메시지 출력
                    }
                }, 100);
            })
            .catch(error => {
                console.error('Error:', error); // 네트워크 에러 등 예외 발생 시 에러 메시지 출력
                setTimeout(hideLoadingIndicator, 100); 
            }); // 예외 발생 시에도 로딩 종료 필요
        }
    }

    function resetSelection() {
        // 모든 버튼에서 'selected' 클래스 제거
        oButton.classList.remove('selected');
        xButton.classList.remove('selected');
        submitButton.classList.remove('selected');
    }
    // 페이지 로드 시 첫 번째 문제 로드
    loadNextQuestion();
});