from typing import List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session

class CRUD:
    def __init__(self, model):
        self._model = model
    
    def create(self, db: Session, schema):
        obj_data = schema.model_dump(exclude_none=True, exclude_unset=True)
        db_obj = self._model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_with_user(self, db: Session, schema, id):
        obj_data = schema.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        db_obj = self._model(**obj_data, user_id=id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj, schema):
        obj_data = schema.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj):
        db.delete(db_obj)
        db.commit()
        return db_obj

    def get_one(self, db: Session, *args, **kwargs):
        return db.query(self._model).filter(*args).filter_by(**kwargs).first()
    
    def get_many(self, db: Session, limit, *args, **kwargs):
        return db.query(self._model).filter(*args).filter_by(**kwargs).limit(limit).all()

    def get_many_from_user(self, db: Session, limit, id, *args, **kwargs):
        return self.get_many(db, limit=limit, *args, user_id=id, **kwargs)