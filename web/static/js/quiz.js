document.addEventListener('DOMContentLoaded', function() {
    let currentQuestionId;
    let currentQuestionNum = 1; // 예시로 1로 시작합니다.
    fetch('/get-first-question')
    .then(response => response.json())
    .then(data => {
        console.log(data);  // 전체 데이터 구조 확인
        currentQuestionId = data.id;
        displayQuestion(data);
        document.getElementById('question-text').textContent = data;
        // 필요한 경우, 문제의 옵션 등을 페이지에 추가로 표시하는 코드
    })
    .catch(error => console.error('Error:', error));


// 버튼 참조
const oButton = document.getElementById('o-button');
const xButton = document.getElementById('x-button');

document.getElementById('o-button').addEventListener('click', function() {
    updateSelection(oButton);
    sendAnswer(true, currentQuestionNum, currentQuestionId); // 문제를 맞힘
});

document.getElementById('x-button').addEventListener('click', function() {
    updateSelection(xButton);
    sendAnswer(false, currentQuestionNum, currentQuestionId); // 문제를 틀림
});

document.getElementById('next-button').addEventListener('click', function() {
    loadNextQuestion(); // 다음 문제 로드
});



// 선택된 버튼 강조 및 다른 버튼의 강조 해제
function updateSelection(selectedButton) {
    // 먼저 모든 버튼에서 'selected' 클래스 제거
    oButton.classList.remove('selected');
    xButton.classList.remove('selected');
    
    // 선택된 버튼에만 'selected' 클래스 추가
    selectedButton.classList.add('selected');
}

function sendAnswer(answer, questionId) {
    // 서버로 응답을 전송하는 로직
    fetch('/submit-answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            questionId: questionId,
            answer: answer
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data);
        currentQuestionId = data.next_item_id;  // 다음 문제 ID 업데이트
        //loadNextQuestion(data.next_item_id);  // 수정: 다음 문제 로드 함수에 다음 문제 ID 전달
    })

    .catch(error => console.error('Error:', error));
}

function loadNextQuestion() {
    currentQuestionNum++; // 문제 번호를 업데이트
    // 다음 문제 데이터 로드 로직 (여기서는 간단히 문제 번호와 텍스트를 업데이트)
    document.getElementById('question-number').textContent = `${currentQuestionNum}번째 문제`;
    document.getElementById('question-text').textContent = '새로운 문제가 여기에 표시됩니다.';
    
    // 실제 애플리케이션에서는 여기에서 서버로부터 다음 문제 데이터를 요청하고,
    // 받아온 데이터로 문제 내용을 업데이트해야 합니다.
}
function updateQuestionDisplay(data) {
    document.getElementById('question-number').textContent = `1번째 문제`;
    document.getElementById('question-text').textContent = data.content;  // 예: 문제 내용
    // 추가적으로, 선택지 등을 화면에 표시하는 로직을 여기에 구현
}
function displayQuestion(data) {
    // 문제 내용 표시
    document.getElementById('question-text').textContent = data.content;
    console.log(data.content);
}


});