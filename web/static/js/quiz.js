document.addEventListener('DOMContentLoaded', function() {
let currentQuestionId = 1; // 예시로 1로 시작합니다.

document.getElementById('o-button').addEventListener('click', function() {
    sendAnswer(true, currentQuestionId); // 문제를 맞힘
});

document.getElementById('x-button').addEventListener('click', function() {
    sendAnswer(false, currentQuestionId); // 문제를 틀림
});

document.getElementById('next-button').addEventListener('click', function() {
    loadNextQuestion(); // 다음 문제 로드
});

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
        document.getElementById('question-text').textContent = `다음 문제 ID: ${data.next_item_id}`;
        // 다음 문제 로드를 여기서 호출하지 않음
        // loadNextQuestion(); // 이 줄을 제거하거나 주석 처리
    })
    .catch(error => console.error('Error:', error));
}

function loadNextQuestion() {
    currentQuestionId++; // 문제 번호를 업데이트
    // 다음 문제 데이터 로드 로직 (여기서는 간단히 문제 번호와 텍스트를 업데이트)
    document.getElementById('question-number').textContent = `${currentQuestionId}번째 문제`;
    document.getElementById('question-text').textContent = '새로운 문제가 여기에 표시됩니다.';
    
    // 실제 애플리케이션에서는 여기에서 서버로부터 다음 문제 데이터를 요청하고,
    // 받아온 데이터로 문제 내용을 업데이트해야 합니다.
}
});