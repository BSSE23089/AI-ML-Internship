from fastapi import APIRouter
from .model import Model,responseModel
from .services import get_models, post_model, delete_model, update_model

router = APIRouter()


@router.get("/")
def get_data():  
     return get_models() 
    

@router.post("/post", response_model=responseModel)
def add_model(model: Model):
    return post_model(model)

@router.delete("/delete/{model_id}")
def delete(model_id: str):
    return delete_model(model_id)  

@router.put("/update/{model_id}")
def update(model_id: str, model: Model):
    return update_model(model_id, model)