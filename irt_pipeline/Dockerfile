# 파이썬 베이스 이미지 사용
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 Python 패키지 설치
COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN apt-get update

# 애플리케이션 코드 및 실행 스크립트 추가
COPY . /app
COPY run.sh /app

# 실행 스크립트에 실행 권한 부여
RUN chmod +x /app/run.sh

# 실행 스크립트 실행
CMD ["/app/run.sh"]

