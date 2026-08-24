from flask import Flask, jsonify, request, redirect
from flasgger import Swagger
from Models.Monastery import Monastery
from Models.Monastery import db
from flask_migrate import Migrate
import os
from exceptions import (
    MonasteryError,
    DbConnectionError,
    MonasteryNotFoundError,
    MonasterySaveError,
    MonasteryUpdateError,
    MonasteryDeleteError
)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API V1",
        "description": "Monasteries CRUD API",
        "version": "1.0.0"
    },
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "definitions": {
        "Monastery": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "location": {"type": "string"},
                "year_of_construction": {"type": "integer"}
            }
        },
        "MonasteryInput": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "location": {"type": "string"},
                "year_of_construction": {"type": "integer"}
            },
            "required": ["name", "location"],
            "example": {
              "name": "Studenica",
              "location": "Kraljevo",
              "year_of_construction": 1190
            }
        }
    }
}

app = Flask(__name__)
swagger = Swagger(app, template=swagger_template)

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'mysql+pymysql://user:[REDACTED]@db/monastery_db'  # fallback
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Create tables on startup (wrap in try-except for startup safety)
def init_db():
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"Database initialization warning: {e}")

@app.before_request
def ensure_db_initialized():
    """Lazy initialization of database"""
    try:
        with app.app_context():
            db.create_all()
    except Exception:
        pass  # Silently fail if DB not ready yet

@app.route('/')
def index():
    return redirect('/apidocs')  # Redirect to Swagger UI
  
@app.route('/api/monasteries', methods=['GET'])
def get_monasteries():
    """
    Get all monasteries
    ---
    tags:
      - Monasteries CRUD
    responses:
      200:
        description: List of monasteries
        schema:
          type: array
          items:
            $ref: '#/definitions/Monastery'
    """
    monasteries = Monastery.get_all()
    return jsonify([monastery.to_dict() for monastery in monasteries] if monasteries else []), 200 #response -> OK
 
@app.route('/api/monasteries/<int:id>', methods=['GET'])
def get_monastery_by_id(id):
    """
    Get Monastery by ID
    ---
    tags:
      - Monasteries CRUD
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        minimum: 1
        description: Positive ID of the monastery (must be >= 1)
    responses:
      200:
        description: Monastery found
        schema:
          $ref: '#/definitions/Monastery'
      404:
        description: Monastery not found
      400:
        description: Invalid ID (must be >= 1)
    """
    monastery = Monastery.get_by_id(id)
    if not monastery:
        raise MonasteryNotFoundError("Monastery not found")
    return jsonify(monastery.to_dict()), 200 # response -> OK

@app.route('/api/monasteries/location/<string:location>', methods=['GET'])
def get_monasteries_by_location(location):
    """
    Get monasteries by location
    ---
    tags:
      - Monasteries CRUD
    parameters:
      - name: location
        in: path
        type: string
        required: true
        description: Location of the monasteries
    responses:
      200:
        description: List of monasteries
        schema:
          type: array
          items:
            $ref: '#/definitions/Monastery'
    """
    monasteries = Monastery.get_by_location(location)
    if not monasteries:
        return jsonify([]), 200  # Return empty array if none found
    return jsonify([monastery.to_dict() for monastery in monasteries]), 200 # response -> OK

@app.route('/api/monasteries/year/<int:year>', methods=['GET'])
def get_monasteries_by_year_of_construction(year):
    """
    Get monasteries by year of construction
    ---
    tags:
      - Monasteries CRUD
    parameters:
      - name: year
        in: path
        type: integer
        required: true
        minimum: 1
        description: Year of construction (must be >= 1)
    responses:
      200:
        description: List of monasteries
        schema:
          type: array
          items:
            $ref: '#/definitions/Monastery'
      404:
        description: No monasteries found for that year
      400:
        description: Invalid year (must be >= 1)
    """
    monasteries = Monastery.get_by_year_of_construction(year)
    if not monasteries:
        return jsonify([]), 200  # Return empty array if none found
    return jsonify([m.to_dict() for m in monasteries]), 200

@app.route('/api/monasteries/name/<string:name>', methods=['GET'])
def get_monasteries_by_name(name):
    """
    Get monasteries by name
    ---
    tags:
      - Monasteries CRUD
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: Name of the monastery
    responses:
      200:
        description: List of monasteries with the given name
        schema:
          type: array
          items:
            $ref: '#/definitions/Monastery'
      404:
        description: No monasteries found for that name
    """
    monasteries = Monastery.get_by_name(name)
    if not monasteries:
        return jsonify([]), 200  # Return empty array if none found
    return jsonify([m.to_dict() for m in monasteries]), 200

@app.route('/api/monasteries', methods=['POST'])
def add_monastery():
    """
    Add a new Monastery
    ---
    tags:
      - Monasteries CRUD
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/MonasteryInput'
    responses:
      201:
        description: Monastery created
        schema:
          $ref: '#/definitions/Monastery'
    """
    data = request.get_json()
    if "name" not in data or "location" not in data or "year_of_construction" not in data:
        raise MonasterySaveError("Missing required fields: name, location, or year_of_construction")
    new_monastery = Monastery(
        name=data["name"],
        location=data["location"],
        year_of_construction=data.get("year_of_construction")
    )
    new_monastery.save()
    return jsonify(new_monastery.to_dict()), 201 # response -> Created

@app.route('/api/monasteries/<int:id>', methods=['PUT'])
def update_monastery(id):
    """
    Update Monastery by ID
    ---
    tags:
      - Monasteries CRUD
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        minimum: 1
        description: Positive ID of the monastery (must be >= 1)
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/MonasteryInput'
    responses:
      200:
        description: Monastery updated
        schema:
          $ref: '#/definitions/Monastery'
      404:
        description: Monastery not found
      400:
        description: Invalid ID (must be >= 1)
    """
    data = request.get_json()
    monastery = Monastery.get_by_id(id)
    if not monastery:
        raise MonasteryNotFoundError("Monastery not found")
    required_fields = ["name", "location", "year_of_construction"]
    for field in required_fields:
      if field not in data:
        raise MonasteryUpdateError(f"Missing field: {field}")
    monastery.update(
        data["name"],
        data["location"],
        data["year_of_construction"]
    )
    updated = Monastery.get_by_id(id)
    return jsonify(updated.to_dict()), 200 # response -> OK

@app.route('/api/monasteries/<int:id>', methods=['PATCH'])
def patch_monastery(id):
    """
    Partially update Monastery by ID
    ---
    tags:
      - Monasteries CRUD
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        minimum: 1
        description: Positive ID of the monastery (must be >= 1)
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/MonasteryInput'
    responses:
      200:
        description: Monastery updated
        schema:
          $ref: '#/definitions/Monastery'
      404:
        description: Monastery not found
      400:
        description: Invalid ID (must be >= 1)
    """
    data = request.get_json()
    monastery = Monastery.get_by_id(id)
    if not monastery:
        raise MonasteryNotFoundError("Monastery not found")
    name = data.get("name", monastery.name)
    location = data.get("location", monastery.location)
    year = data.get("year_of_construction", monastery.year_of_construction)

    monastery.update(name, location, year)
    updated = Monastery.get_by_id(id)
    return jsonify(updated.to_dict()), 200 # -> OK

@app.route('/api/monasteries/<int:id>', methods=['DELETE'])
def delete_monastery(id):
    """
    Delete Monastery by ID
    ---
    tags:
      - Monasteries CRUD
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        minimum: 1
        description: Positive ID of the monastery (must be >= 1)
    responses:
      200:
        description: Monastery deleted
      404:
        description: Monastery not found
      400:
        description: Invalid ID (must be >= 1)
    """
    monastery = Monastery.get_by_id(id)
    if not monastery:
        raise MonasteryNotFoundError("Monastery not found")
    monastery.delete()
    return jsonify({"message": "Monastery deleted"}), 200 # response -> OK
  
# handle errors in json format
@app.errorhandler(MonasteryError)
def handle_monastery_error(error):
    return jsonify({"error": error.message}), error.status_code

@app.errorhandler(DbConnectionError)
def handle_db_error(error):
    return jsonify({"error": error.message}), error.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader = False)
