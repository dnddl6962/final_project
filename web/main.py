from fastapi import FastAPI, HTTPException, Body, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from database import engine, metadata, database
from models import Base, User
from schemas import Nickname



load_dotenv()  #환경 변수 불러오기.

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {DATABASE_URL}")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# @app.on_event("startup")
# async def startup():
#     await database.connect()
#     # 데이터베이스 테이블 생성
#     metadata.create_all(bind=engine)

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/")
async def read_root():
    return {"웅이네 샤인매스캣에 오신것을 환영합니다."}

@app.post("/start-test")
async def start_test():
    # 여기에서 CAT 테스트 시작 로직을 구현합니다.
    return {"message": "Test started"}

class UserResponse(BaseModel):
    question_id: int
    user_answer: str

@app.post("/answer")
async def process_answer(response: UserResponse):
    # 사용자 응답 처리 로직
    # 여기서는 사용자 응답을 바탕으로 능력 추정치 업데이트, 다음 문제 선택 등을 수행합니다.
    # 능력 추정치가 특정 오차 범위 이내로 수렴하는지 검사합니다.
    # 예시 코드이므로, 실제 CAT 알고리즘 구현이 필요합니다.
    
    return {"next_question": "다음 문제 정보", "est_theta": "현재 추정된 능력치"}
# @app.post("/save-results")
# async def save_results(user_id: str, results: dict):
#     save_results_to_s3(user_id, results)
#     return {"message": "Results saved successfully"}

@app.post("/users/", response_model=Nickname, status_code=status.HTTP_201_CREATED)
async def create_user(nickname: Nickname):
    query = users.insert().values(nickname=nickname.nickname)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, "nickname": nickname.nickname}