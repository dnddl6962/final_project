from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"웅이네 샤인매스캣은 우주최강 팀입니다. 아시겠죠?"}

@app.post("/start-test")
async def start_test():
    # 여기에서 CAT 테스트 시작 로직을 구현합니다.
    return {"message": "Test started"}
