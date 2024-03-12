from fastapi import FastAPI, HTTPException, Body, Request, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from database import SessionLocal, engine
from schemas import NicknameCreate
from sqlalchemy.orm import Session
from models import Nickname
from database import SessionLocal, engine, Base
import schemas, models
from fastapi.responses import JSONResponse


load_dotenv()  #환경 변수 불러오기.

#Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()       

@app.post("/users/")
def create_user(nickname: NicknameCreate):
    try:
        # 닉네임 생성 로직
        # nickname.nickname 값을 사용하여 닉네임을 생성합니다.
        return {"message": "Nickname created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/start-test")
async def start_test():
    return RedirectResponse(url='/quiz', status_code=status.HTTP_303_SEE_OTHER)


@app.get("/quiz", response_class=HTMLResponse)
async def get_quiz_page(request: Request):
    # quiz.html을 렌더링하여 반환합니다.
    return templates.TemplateResponse("quiz.html", {"request": request})

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

