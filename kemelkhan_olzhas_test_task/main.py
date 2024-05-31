from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import engine, SessionLocal
from db.models import student_model
from dto.student_base import StudentBase


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


student_model.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

app = FastAPI()


@app.post("/student/")
async def create_student(student: StudentBase, db: db_dependency):
    db_student = student_model.Students(name=student.name, score=student.score)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)


@app.get("/student/{id}")
async def get_students(id: int, db: db_dependency):
    result = db.query(student_model.Students).filter(id == student_model.Students.id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return result


@app.put("/student/{id}")
async def update_student(id: int, student: StudentBase, db: db_dependency):
    db_student = db.query(student_model.Students).filter(id == student_model.Students.id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.name is not None:
        db_student.name = student.name
    if student.score is not None:
        db_student.score = student.score
    db.commit()
    db.refresh(db_student)
    return db_student


@app.delete("/student/{id}")
async def delete_student(id: int, db: db_dependency):
    db_student = db.query(student_model.Students).filter(id == student_model.Students.id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
