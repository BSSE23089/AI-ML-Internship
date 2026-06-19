from pydantic import BaseModel

class  Model(BaseModel):
    version: int
    name: str
    description: str

class responseModel(BaseModel):
     inserted_id: str
     message: str
    

