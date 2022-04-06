import models
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = ''

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Scripts(BaseModel):
    script_name: str
    filename: str
    is_active: bool


@app.get("/")
async def read_all_values(db: Session = Depends(get_db)):
    return db.query(models.Scripts).all()


@app.post("/")
async def write_script_to_file(scripts: Scripts, db: Session = Depends(get_db)):
    scripts_model = models.Scripts()
    scripts_model.script_name = scripts.script_name
    scripts_model.filename = scripts.filename
    scripts_model.is_active = scripts.is_active

    db.add(scripts_model)
    db.commit()


@app.put("/{name_script}")
async def update_script(name_script: str, scripts: Scripts,
                        db: Session = Depends(get_db)):
    scripts_model = db.query(models.Scripts)\
        .filter(models.Scripts.script_name == name_script)\
        .first()

    if scripts_model is None:
        return http_exception()

    scripts_model.script_name = scripts.script_name
    scripts_model.filename = scripts.filename
    scripts_model.is_active = scripts.is_active

    db.add(scripts_model)
    db.commit()

    return successful_response(200, f"successful update => {name_script}")


def successful_response(status_code: int, transaction: str):
    return {
        'status': status_code,
        'transaction': transaction
    }


def http_exception():
    raise HTTPException(status_code=404, detail="value not found")
