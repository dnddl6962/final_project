from fastapi import FastAPI, HTTPException, APIRouter, Body, Request, status, Depends, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from database import check_userid_duplicate, sessionmaker, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from load import load_data
import numpy as np
from catsim.irt import icc
from catsim.initialization import FixedPointInitializer
from catsim.selection import UrrySelector
from catsim.estimation import NumericalSearchEstimator
from catsim.stopping import MinErrorStopper
from simulator import Simulator
from quiz import json_to_array, get_quiz

app = FastAPI()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 초기화
json_data = load_data('mathcat-bucket', 'irt_result/yyyy=2024/mm=03/dd=13/irt_result.json')
result_array = json_to_array(json_data)
initial_item_ids = get_quiz(json_data, result_array)
    
initializer = FixedPointInitializer(0)
selector = UrrySelector()
estimator = NumericalSearchEstimator()
stopper = MinErrorStopper(0.6)

# administered_items = []
# responses = []
# index = 0
# simulator = None

class SimulatorManager:
    def __init__(self):
        self.simulator = None
    
    def initialize_simulator(self):
        self.simulator = Simulator(np.array(result_array), 4, initializer, selector, estimator, stopper)

simulator_manager = SimulatorManager()

class Simulator:
    def __init__(self, result_array, init_items, initializer, selector, estimator, stopper):
        self.result_array = result_array
        self.init_items = init_items
        self.initializer = initializer
        self.selector = selector
        self.estimator = estimator
        self.stopper = stopper
        self.administered_items = []
        self.responses = []
        self.index = 0

    def recommend_next(self, user_answer=None, quiz=False):
        
        ## 다음 문제 추천
        # 초기 4문제는 리스트에서 반환
        if len(self.administered_items) < self.init_items:
            if quiz:
                return initial_item_ids[self.index]

            item_index = list(json_data['item_ids'].values()).index(initial_item_ids[self.index])
            self.administered_items.append(item_index)

            # 문제에 대한 응답 추가
            correct = user_answer
            self.responses.append(correct == True)
            print(f'Did the user answer the item {initial_item_ids[self.index]} correctly?: {self.responses[self.index]}')


        # 5번째 문제부터는 사용자의 학습 수준에 맞게 추천
        else:
            item_index = self.selector.select(items=self.result_array, administered_items=self.administered_items, est_theta=self.est_theta)
            if quiz:
                return json_data['item_ids'][str(item_index)]
            
            self.administered_items.append(item_index)

            # 문제에 대한 응답 추가
            correct = user_answer
            self.responses.append(correct == True)
            print(f"Did the user answer the item {json_data['item_ids'][str(item_index)]} correctly?: {self.responses[self.index]}")


        # 사용자의 학습 수준 추정
        if self.index == 3:
            self.est_theta = self.initializer.initialize()
            self.est_theta = self.estimator.estimate(
                items=np.array(self.result_array),
                administered_items=self.administered_items,
                response_vector=self.responses,
                est_theta=self.est_theta
            )
        elif self.index > 3:
            self.est_theta = self.estimator.estimate(
                items=np.array(self.result_array),
                administered_items=self.administered_items,
                response_vector=self.responses,
                est_theta=self.est_theta
            )
        else:
            self.est_theta = 0
            
        if self.stopper.stop(administered_items=np.array(self.result_array)[self.administered_items], theta=self.est_theta):
            # 사용자의 학습 수준 출력
            print("시험 종료")
            print("Final estimated proficiency:", self.est_theta)
            return self.est_theta, self.administered_items, self.responses, self.index, True

        self.index += 1
        return self.est_theta, self.administered_items, self.responses, self.index, False
            

class User(BaseModel):
    userid: str


@app.post("/users/")
async def create_user(user_create: User,  db: Session = Depends(get_db)):
    # 중복 검사
    user = db.execute(text("SELECT * FROM id_test WHERE userid = :userid"), {'userid': user_create.userid}).fetchone()
    if user:
        raise HTTPException(status_code=400, detail="닉네임이 이미 사용 중입니다.")
    
    # 새 사용자 추가
    db.execute(text("INSERT INTO id_test (userid) VALUES (:userid)"), {'userid': user_create.userid})
    db.commit()

    return {"userid": user_create.userid}

@app.get("/get-userid")
async def get_userid(session_id: str, response: Response,  db: Session = Depends(get_db)):
    # session_id로 사용자를 찾습니다.
    db_user = db.query(User).filter(User.session_id == session_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # 찾은 사용자의 userid를 쿠키에 저장합니다.
    response.set_cookie(key="userid", value=db_user.userid)
    return {"userid": db_user.userid}

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    global simulator_manager
    simulator_manager.initialize_simulator()
    # 홈 페이지를 렌더링하여 반환합니다.
    return templates.TemplateResponse("home.html", {"request": request})

async def get_next_question():
    global simulator_manager
    
    if simulator_manager.simulator is None:
        raise HTTPException(status_code=500, detail="Simulator not initialized")
    item_id = simulator_manager.simulator.recommend_next(quiz=True)
    
    if not item_id:
        raise HTTPException(status_code=404, detail="더 이상 다음 문제가 없습니다.")
    
    return {"item_id": item_id}

@app.get("/get-question")
async def get_question():
    # 다음 문제 반환
    return await get_next_question()

@app.get("/quiz", response_class=HTMLResponse)
async def get_quiz_page(request: Request):
    # quiz.html을 렌더링하여 반환합니다.
    return templates.TemplateResponse("quiz.html", {"request": request})

class Answer(BaseModel):
    answer: bool

# POST 요청 핸들러 함수
@app.post('/submit-answer')
async def submit_answer(answer: Answer, response: Response):
    global simulator_manager
    if simulator_manager.simulator is None:
        raise HTTPException(status_code=500, detail="Simulator not initialized")
    
    # 서버로부터 응답을 전송하는 로직
    est_theta, administered_items, responses, index, last_quiz = simulator_manager.simulator.recommend_next(answer.answer)

    if last_quiz:
        # 마지막 퀴즈인 경우 다음 문제 반환하지 않고, 빈 응답을 보냄
        response.set_cookie(key="est_theta", value=est_theta)
        response.delete_cookie("administered_items")
        response.delete_cookie("responses")
        response.delete_cookie("index")
        response.set_cookie("last_quiz", "True")
        return {"message": "마지막 문제입니다.", "estimated_proficiency": est_theta, "last_quiz": last_quiz}
    else:
        # 다음 문제 반환
        next_item_id = await get_next_question()
        # 쿠키에 값 저장
        response.set_cookie(key="est_theta", value=est_theta)
        response.set_cookie(key="administered_items", value=administered_items)
        response.set_cookie(key="responses", value=responses)
        response.set_cookie(key="index", value=index)
        response.set_cookie(key="last_quiz", value=last_quiz)
        if answer.answer:
            return {"message": "정답입니다!", "estimated_proficiency": est_theta, "next_item_id": next_item_id, "last_quiz": last_quiz}
        else:
            return {"message": "오답입니다.", "estimated_proficiency": est_theta, "next_item_id": next_item_id, "last_quiz": last_quiz}


@app.get("/result", response_class=HTMLResponse)
async def get_result_page(request: Request):
    est_theta = request.cookies.get("est_theta")
    
    # result.html을 렌더링하여 반환합니다.
    return templates.TemplateResponse("result.html", {"request": request, "est_theta": est_theta})
