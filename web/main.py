from fastapi import FastAPI, HTTPException, APIRouter, Body, Request, status, Depends, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
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


#Base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter()
#create_tables()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

  
class User(BaseModel):
    userid: str

@app.post("/users/")
async def create_user(userid: str, db: Session = Depends(get_db)):
    # 닉네임 중복 검사
    if check_userid_duplicate(db, userid):
        raise HTTPException(status_code=400, detail="닉네임이 이미 사용 중입니다.")
    
    # 새 사용자 객체 생성
    new_user = User(userid=userid)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"userid": new_user.userid, "id": new_user.id}





# # 예시: 사용자 등록 엔드포인트
# @app.post("/users/")
# async def register_user(user: User):
#     # 여기에서 닉네임이 중복되는지 다시 한 번 확인할 수 있습니다.
#     is_duplicate = check_userid_duplicate(user.userid)
#     if is_duplicate:
#         raise HTTPException(status_code=400, detail="닉네임이 이미 사용 중입니다.")
    
#     # 중복되지 않는 경우, 데이터베이스에 사용자를 추가하는 로직을 수행
#     # 예를 들어:
#     # new_user = UserTable(userid=user.userid) # UserTable은 ORM 모델
#     # db.add(new_user)
#     # db.commit()
#     # db.refresh(new_user)
#     # 데이터베이스에 사용자를 추가하는 등의 작업을 수행합니다.
    
#     return {"userid": user.userid, "registered": True}     

# @router.post("/check-nickname")
# async def check_nickname(nickname: str = Body(..., embed=True)):
#     # 닉네임 중복 확인
#     is_duplicate = check_userid_duplicate(nickname)
#     if is_duplicate:
#         # 이미 존재하는 닉네임인 경우
#         return {"isAvailable": False}
#     else:
#         # 사용 가능한 닉네임인 경우
#         return {"isAvailable": True}

#app.include_router(router)

    
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

# POST 요청 핸들러 함수
@app.post('/submit-answer')
async def submit_answer(answer: Answer, response: Response):
    json_data = load_data('mathcat-bucket', 'irt_result/yyyy=2024/mm=03/dd=13/irt_result.json')
    result_array = []  # result_array 초기화

    # result_array 생성
    for i in range(len(json_data['disc'])):
        new_array = [json_data['disc'][i], json_data['diff'][i], 0, 1]
        result_array.append(new_array)

    # 초기화
    initializer = FixedPointInitializer(0)
    selector = UrrySelector()
    estimator = NumericalSearchEstimator()
    stopper = MinErrorStopper(0.6)

    class Simulator:
        def __init__(self, result_array, max_items, initializer, selector, estimator, stopper):
            self.result_array = result_array
            self.max_items = max_items
            self.initializer = initializer
            self.selector = selector
            self.estimator = estimator
            self.stopper = stopper

        def simulate(self, verbose=False):
            administered_items = []
            responses = []

            # 초기 4문제의 문제 ID
            initial_item_ids = ['quiz30049372', 'quiz30064607', 'quiz30048859', 'quiz30062323']

            # 초기 4문제의 인덱스를 찾아서 administered_items에 추가하고 응답 벡터에 대응하는 응답을 추가
            for item_id in initial_item_ids:
                item_index = list(json_data['item_ids'].values()).index(item_id)
                administered_items.append(item_index)

                # 초기 문제에 대한 응답 추가 (사용자 입력 대신 Answer 모델에서 받음)
                responses.append(answer.answer)

            # 초기화 단계
            est_theta = self.initializer.initialize()

            # 초기 4문제 후의 능력치 출력
            if verbose:
                print("Initial 4 items answered. Estimated proficiency:", est_theta)

            while True:
                # 추천 단계
                if len(administered_items) >= len(initial_item_ids):
                    item_index = self.selector.select(items=np.array(self.result_array), administered_items=administered_items, est_theta=est_theta)
                else:
                    # 초기 문제를 추천하지 않도록 건너뛰기
                    item_index = administered_items[len(administered_items)]

                next_item_id = json_data['item_ids'][str(item_index)]

                # 평가 단계
                a, b, c, d = np.array(self.result_array)[item_index]
                prob = icc(est_theta, a, b, c, d)
                correct = answer.answer

                # 결과 기록
                administered_items.append(item_index)
                responses.append(correct)

                # 중단 단계
                if len(administered_items) >= self.max_items or self.stopper.stop(administered_items=np.array(self.result_array)[administered_items], theta=est_theta):
                    break

                # 능력치 업데이트
                est_theta = self.estimator.estimate(
                    items=np.array(self.result_array),
                    administered_items=administered_items,
                    response_vector=responses,
                    est_theta=est_theta
                )

                if verbose:
                    print('Estimated proficiency, given answered items:', est_theta)
                    print('Next item to be administered:', next_item_id)
                    print('Probability to correctly answer item:', prob)
                    print('Did the user answer the selected item correctly?', correct)
                    print("responses: ", responses)

            if verbose:
                print("responses: ", responses)
            print("사용자의 최종 능력치 (Estimated Proficiency):", est_theta)
            return est_theta

    s = Simulator(result_array, 20, initializer, selector, estimator, stopper)
    est_theta = s.simulate(verbose=True)

    # 쿠키에 값 저장
    response.set_cookie(key="est_theta", value=est_theta)
    
    if answer.answer:
        return {"message": "정답입니다!", "estimated_proficiency": est_theta}
    else:
        return {"message": "오답입니다.", "estimated_proficiency": est_theta}



    # 사용자의 응답에 기반한 처리 로직
    # 예: 사용자의 능력치 업데이트, 다음 문제 선택 등

    # 클라이언트에게 JSON 형태로 다음 문제 데이터 및 기타 정보 반환
    # return {"next_question": "some_question_data", "other_info": "value"}

@app.get("/result", response_class=HTMLResponse)
async def get_result_page(request: Request):

    est_theta = request.cookies.get("est_theta")

    # result.html을 렌더링하여 반환합니다.
    return templates.TemplateResponse("result.html", {"request": request, "est_theta": est_theta})