from Database.dbConnection import DbConnection
from exceptions import (
    MonasteryError,
    DbConnectionError,
    MonasteryNotFoundError,
    MonasterySaveError,
    MonasteryUpdateError,
    MonasteryDeleteError
)

# Model for Monastery 
class Monastery:
    def __init__(self, id, name, location, year_of_construction) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.year_of_construction = year_of_construction

    def save(self) -> 'Monastery':
        try:
            if not self.name or not self.location:
                raise MonasterySaveError("Name and location are required")
            if self.year_of_construction is None or self.year_of_construction <= 0:
                raise MonasterySaveError("Year of construction must be a positive number")
            conn = DbConnection.get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO monasteries (id, name, location, year_of_construction) VALUES (%s, %s, %s, %s)"
            values = (self.id, self.name, self.location, self.year_of_construction)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return self
        except DbConnectionError as e:
            raise e
        except MonasteryError as e:  
            raise e
        except Exception as e:
            raise MonasterySaveError("Error occurred while saving monastery")
    
    @staticmethod
    def get_all() -> list['Monastery']:
        try:
            conn = DbConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM monasteries")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return [Monastery(**row) for row in rows]
        except DbConnectionError as e:
            raise e
        except Exception as e:
            raise MonasteryError("Error occurred while fetching all monasteries")

    @staticmethod
    def get_by_id(monastery_id) -> 'Monastery' or None:
        try:
            conn = DbConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM monasteries WHERE id = %s", (monastery_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return Monastery(**row) if row else None
        except DbConnectionError as e:
            raise e
        except Exception as e:
            raise MonasteryNotFoundError("Monastery not found")

    @staticmethod
    def get_by_location(location) -> 'Monastery' or None:
        try:
            conn = DbConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM monasteries WHERE location = %s", (location,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return [Monastery(**row) for row in rows]
        except DbConnectionError as e:
            raise e
        except Exception as e:
            raise MonasteryError("Error occurred while fetching monasteries by location")

    @staticmethod
    def get_by_year_of_construction(year_of_construction) -> 'Monastery' or None:
        try:
            conn = DbConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM monasteries WHERE year_of_construction = %s", (year_of_construction,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return [Monastery(**row) for row in rows]
        except DbConnectionError as e:
            raise e
        except Exception as e:
            raise MonasteryError("Error occurred while fetching monasteries by year of construction")
            
    @staticmethod
    def get_by_name(name) -> 'Monastery' or None:
        try:
            conn = DbConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM monasteries WHERE name = %s", (name,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return [Monastery(**row) for row in rows]
        except DbConnectionError as e:
            raise e
        except Exception as e:
            raise MonasteryError("Error occurred while fetching monasteries by name")
    
    @staticmethod
    def update(monastery_id, name, location, year_of_construction) -> bool:
        try:
            name = name.strip() if name else None
            location = location.strip() if location else None

            if not name:
                raise MonasteryUpdateError("Name cannot be empty")
            if not location:
                raise MonasteryUpdateError("Location cannot be empty")
            if year_of_construction is None or year_of_construction <= 0:
                raise MonasteryUpdateError("Year of construction must be a positive number")

            from datetime import datetime
            current_year = datetime.now().year
            if year_of_construction > current_year:
                raise MonasteryUpdateError("Year of construction cannot be in the future")

            conn = DbConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM monasteries WHERE id = %s", (monastery_id,))
            if cursor.fetchone()[0] == 0:
                raise MonasteryNotFoundError(f"Monastery with id {monastery_id} not found")
            sql = """
                UPDATE monasteries 
                SET name = %s, location = %s, year_of_construction = %s 
                WHERE id = %s
            """
            values = (name, location, year_of_construction, monastery_id)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except DbConnectionError as e:
            raise e
        except MonasteryError as e:
            raise e
        except Exception as e:
            raise MonasteryUpdateError(str(e))

    @staticmethod
    def delete(monastery_id) -> bool:
        try:
            if monastery_id is None or monastery_id <= 0:
                raise MonasteryDeleteError("Invalid monastery ID")
            
            conn = DbConnection.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM monasteries WHERE id = %s",(monastery_id,))
            if cursor.fetchone()[0] == 0:
                 raise MonasteryNotFoundError(f"Monastery with id {monastery_id} not found")
            
            cursor.execute("DELETE FROM monasteries WHERE id = %s", (monastery_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except DbConnectionError as e:
            raise e
        except Exception as e:
            raise MonasteryDeleteError("Error occurred while deleting monastery")