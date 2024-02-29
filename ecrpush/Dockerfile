# 기본 이미지 설정
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사 (여기에서는 module.py와 main.py를 복사)
COPY . .

# 컨테이너 실행 시 실행할 명령어
CMD ["python", "./main.py"]

