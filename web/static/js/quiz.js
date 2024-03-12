async function startTest() {
    try {
        const response = await fetch('/start-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            window.location.href = '/quiz'; // 퀴즈 페이지로 리다이렉트
        } else {
            console.error('테스트를 시작할 수 없습니다. 서버 응답:', await response.text());
        }
    } catch (error) {
        console.error('테스트 시작 중 에러가 발생했습니다:', error);
    }
}
