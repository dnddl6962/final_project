from fastapi import FastAPI, HTTPException, APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text, func, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from database import SessionLocal
from sqlalchemy.orm import Session
from load import load_data
import numpy as np
from catsim.initialization import FixedPointInitializer
from catsim.selection import UrrySelector
from catsim.estimation import NumericalSearchEstimator
from catsim.stopping import MinErrorStopper
from simulator import Simulator
from quiz import json_to_array, get_quiz
from datetime import datetime, timedelta
import base64

app = FastAPI()
router = APIRouter()
Base = declarative_base()

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


def encode_userid(userid: str) -> str:
    # userid를 UTF-8로 인코딩한 다음, Base64 인코딩을 적용합니다.
    return base64.urlsafe_b64encode(userid.encode('utf-8')).decode('ascii')
def decode_userid(encoded_userid: str) -> str:
    # Base64로 인코딩된 userid를 디코딩합니다.
    return base64.urlsafe_b64decode(encoded_userid.encode('ascii')).decode('utf-8')

@app.post("/users/")
async def create_user(user_create: User, response: Response,  db: Session = Depends(get_db)):
    # 중복 검사
    user = db.execute(text("SELECT * FROM id_test WHERE userid = :userid"), {'userid': user_create.userid}).fetchone()
    if user:
        raise HTTPException(status_code=400, detail="닉네임이 이미 사용 중입니다.")
    
    # 새 사용자 추가
    db.execute(text("INSERT INTO id_test (userid) VALUES (:userid)"), {'userid': user_create.userid})
    db.commit()
    
    # 사용자의 userid를 쿠키에 저장하기 전에 Base64로 인코딩
    encoded_userid = encode_userid(user_create.userid)
    decoded_userid = decode_userid(encoded_userid)
    response.set_cookie(key="userid", value=encoded_userid)
    
    return {"userid": decoded_userid}

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home_page(response: Response, request: Request):

    global simulator_manager
    simulator_manager.initialize_simulator()

    # est_theta 쿠키 초기화
    response.set_cookie(key="est_theta", value="0")
    
    # 홈 페이지를 렌더링하여 반환
    return templates.TemplateResponse("home.html", {"request": request})

async def get_next_question():
    global simulator_manager
    
    # Simulator 초기화
    if simulator_manager.simulator is None:
        simulator_manager.initialize_simulator()    
    
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
    
    # quiz.html을 렌더링하여 반환
    return templates.TemplateResponse("quiz.html", {"request": request})

class Answer(BaseModel):
    answer: bool

class CatResult(Base):
    __tablename__ = 'cat_result'

    id = Column(Integer, primary_key=True)
    userid = Column(String, nullable=False)
    quizcode = Column(String, nullable=False)
    correct = Column(Integer, nullable=False)
    no = Column(Integer, nullable=False)
    datetime = Column(String, nullable=False)
    proficiency = Column(Float, nullable=False)

no = 0

# POST 요청 핸들러 함수
@app.post('/submit-answer')
async def submit_answer(answer: Answer, response: Response, request: Request, db: Session = Depends(get_db)):
    global simulator_manager
    global no

    if simulator_manager.simulator is None:
        simulator_manager.initialize_simulator()
    
    # 서버로부터 응답을 전송하는 로직
    est_theta, administered_items, responses, index, last_quiz = simulator_manager.simulator.recommend_next(answer.answer)

    # 사용자 id 가져오기
    user_id = decode_userid(request.cookies.get('userid'))
    
    # 사용자의 시험 시작 시간 가져오기
    start_time = request.cookies.get('startTime')  # startTime 쿠키 가져오기

    # 시작 시간이 없으면 에러 반환
    if not start_time:
        raise HTTPException(status_code=400, detail="시험 시작 시간이 없습니다.")
    
    # 시작 시간 출력 형식 변경
    start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')

    # UTC에서 9시간을 더해 서울 시간대로 변환
    korean_start_time = start_time + timedelta(hours=9)
    formatted_start_time = korean_start_time.strftime('%Y-%m-%d %H:%M')

    # 사용자의 학습 능력 가져오기
    proficiency = request.cookies.get('est_theta')

    # 문제 번호를 1씩 증가
    no += 1

    # cat_result 테이블에 새로운 결과 추가
    db_result = CatResult(
        userid=user_id,
        quizcode=json_data['item_ids'][str(simulator_manager.simulator.administered_items[-1])], # 다음 문제의 아이디를 가져와서 사용
        correct=1 if answer.answer else 0, # 정답 여부에 따라 1 또는 0 저장
        no = no, # userid와 datetime이 같은 경우를 고려하여 no 값 계산
        datetime=formatted_start_time,  # 시험 시작 시간 사용
        proficiency=proficiency if proficiency is not None else 0
    )
    db.add(db_result)
    db.commit()

    if last_quiz:
        # 마지막 퀴즈인 경우 다음 문제 반환하지 않고, 빈 응답을 보냄
        response.set_cookie(key="est_theta", value=est_theta)
        response.delete_cookie("administered_items")
        response.delete_cookie("responses")
        response.delete_cookie("index")
        response.set_cookie("last_quiz", "True")

        # no 초기화
        no = 0

        # 시험이 종료되면 Simulator 초기화
        simulator_manager.initialize_simulator()

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
