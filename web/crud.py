# from sqlalchemy.orm import Session
# from . import models, schemas

# def get_nickname_by_name(db: Session, nickname: str):
#     return db.query(models.Nickname).filter(models.Nickname.nickname == nickname).first()

# def create_nickname(db: Session, nickname: schemas.NicknameCreate):
#     db_nickname = models.Nickname(nickname=nickname.nickname)
#     db.add(db_nickname)
#     db.commit()
#     db.refresh(db_nickname)
#     return db_nickname