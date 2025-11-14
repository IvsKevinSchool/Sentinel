from typing import Type, TypeVar, Generic, List
from sqlalchemy.orm import Session

Model = TypeVar("Model")

class BaseRepository(Generic[Model]):
    """
    Params: 
        - Model

    def __init__(self, model: Type[Model]):
        self.model = model

    Return: 
        - get
        - get_all
        - create
        - update
        - delete
    """

    def __init__(self, model: Type[Model]):
        self.model = model

    def get(self, db: Session, id: int) -> Model | None:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, db: Session) -> List[Model]:
        return db.query(self.model).all()
    
    def create(self, db: Session, obj_data: dict) -> Model:
        obj = self.model(**obj_data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def update(self, db: Session, obj_data: dict, id: int) -> Model | None:
        obj = self.get(db, id) # Search the obj on the db

        if not obj:
            return None # If the obj does not exist, return None
        
        for key, value in obj_data.items():
            setattr(obj, key, value) # Update the obj per each field

        db.commit()
        db.refresh(obj)
        return obj
    
    def delete(self, db: Session, id: int) -> bool:
        obj = self.get(db, id)

        if not obj:
            return False
        
        db.delete(obj)
        db.commit()
        return True
        

