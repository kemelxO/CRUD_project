from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    score: int
