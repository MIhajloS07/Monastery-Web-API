# from Database.dbConnection import DbConnection
from flask_sqlalchemy import SQLAlchemy
from exceptions import (
    MonasteryError,
    DbConnectionError,
    MonasteryNotFoundError,
    MonasterySaveError,
    MonasteryUpdateError,
    MonasteryDeleteError
)

db = SQLAlchemy()

# Model for Monastery 
class Monastery(db.Model):
    __tablename__ = "monasteries"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    location = db.Column(db.String(255), nullable = False)
    year_of_construction = db.Column(db.Integer, nullable = False)

    def save(self) -> 'Monastery':
        if not self.name or not self.location:
            raise MonasterySaveError("Name or location are required")
        if self.year_of_construction is None or self.year_of_construction <= 0:
            raise MonasterySaveError("Year of construction must be a positive number")
        db.session.add(self)
        db.session.commit()
        return self
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "year_of_construction": self.year_of_construction
        }
    
    @staticmethod
    def get_all() -> list['Monastery']:
        return Monastery.query.all()

    @staticmethod
    def get_by_id(monastery_id) -> 'Monastery' or None:
        return Monastery.query.get(monastery_id)

    @staticmethod
    def get_by_location(location) -> 'Monastery' or None:
        return Monastery.query.filter_by(location=location).all()

    @staticmethod
    def get_by_year_of_construction(year) -> 'Monastery' or None:
         return Monastery.query.filter_by(year_of_construction=year).all()
            
    @staticmethod
    def get_by_name(name) -> 'Monastery' or None:
        return Monastery.query.filter_by(name=name).all()
    
    def update(self, name, location, year_of_construction) -> bool:
        name = name.strip() if name else None
        location = location.strip() if location else None
        if not name:
            raise MonasteryUpdateError("Name cannot be empty")
        if not location:
            raise MonasteryUpdateError("Location cannot be empty")
        if year_of_construction is None or year_of_construction <= 0:
            raise MonasteryUpdateError("Year of construction must be a positive number")
        
        from datetime import datetime
        if year_of_construction > datetime.now().year:
            raise MonasteryUpdateError("Year of construction cannot be in the future")

        self.name = name
        self.location = location
        self.year_of_construction = year_of_construction
        db.session.commit()
        return self
       
    def delete(self) -> bool:
        db.session.delete(self)
        db.session.commit()
        return True
