from fastapi import FastAPI, HTTPException, Body, Request, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from database import create_tables
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse


#Base.metadata.create_all(bind=engine)
app = FastAPI()
create_tables()
# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()       

# @app.post("/users/")
# def create_tables():
#     Base.metadata.create_all(bind=engine)
#     print("Tables created successfully")
# def create_user(nickname: NicknameCreate):
    
#     try:
#         # 닉네임 생성 로직
#         # nickname.nickname 값을 사용하여 닉네임을 생성합니다.
#         return {"message": "Nickname created successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# @app.post("/start-test")
# async def start_test():
#     return RedirectResponse(url='/quiz', status_code=status.HTTP_303_SEE_OTHER)

@app.get("/start-test", response_class=JSONResponse)
async def start_test():
    # 초기 문제 ID 배열
    initial_item_ids = ['quiz30049372', 'quiz30064607', 'quiz30048859', 'quiz30062323']
    # 실제 로직은 데이터베이스에서 문제 정보를 가져오는 코드로 대체되어야 함
    questions = [
        # 데이터베이스에서 문제 데이터를 가져오는 함수를 호출하여 각 ID에 해당하는 문제 정보를 배열로 만듦
        get_question_data(item_id) for item_id in initial_item_ids
    ]
    return {"initial_questions": questions}
#유틸리티 함수: 각 문제 ID에 대한 문제 데이터를 조회
def get_question_data(initial_item_ids: str):
    # 여기서는 예시 데이터를 반환함
    # 실제로는 데이터베이스에서 해당 문제 ID에 맞는 문제 데이터를 가져와야 함
    return {
        "id": initial_item_ids,
        # 기타 필요한 문제 정보
    }


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

class Answer(BaseModel):
    answer: bool

@app.post('/submit-answer')
async def submit_answer(answer: Answer):  # 본문으로부터 Answer 모델 객체를 자동으로 얻음
    # 사용자의 응답에 기반한 처리 로직
    # 예: 사용자의 능력치 업데이트, 다음 문제 선택 등

    # 클라이언트에게 JSON 형태로 다음 문제 데이터 및 기타 정보 반환
    return {"next_question": "some_question_data", "other_info": "value"}

@app.get("/result", response_class=HTMLResponse)
async def get_result_page(request: Request):
    # quiz.html을 렌더링하여 반환합니다.
    return templates.TemplateResponse("result.html", {"request": request})