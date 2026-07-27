from flask import Flask, jsonify, request, redirect
from flasgger import Swagger
from Models.Monastery import Monastery
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
    if not monasteries:
        raise MonasteryNotFoundError("No monasteries found")
    else:
        return jsonify([monastery.__dict__ for monastery in monasteries]), 200 #response -> OK
 
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
    return jsonify(monastery.__dict__), 200 # response -> OK

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
        raise MonasteryNotFoundError("No monasteries found for the specified location")
    else:
        return jsonify([monastery.__dict__ for monastery in monasteries]), 200 # response -> OK

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
        raise MonasteryNotFoundError(f"No monasteries found for year {year}")
    return jsonify([m.__dict__ for m in monasteries]), 200

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
        raise MonasteryNotFoundError(f"No monasteries found for name {name}")
    return jsonify([m.__dict__ for m in monasteries]), 200

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
        id=get_first_free_id(),
        name=data["name"],
        location=data["location"],
        year_of_construction=data.get("year_of_construction")
    )
    new_monastery.save()
    return jsonify(new_monastery.__dict__), 201 # response -> Created

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
    Monastery.update(
        id,
        data["name"],
        data["location"],
        data["year_of_construction"]
    )
    updated = Monastery.get_by_id(id)
    return jsonify(updated.__dict__), 200 # response -> OK

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

    Monastery.update(id, name, location, year)
    updated = Monastery.get_by_id(id)
    return jsonify(updated.__dict__), 200 # -> OK

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
    Monastery.delete(id) 
    return jsonify({"message": "Monastery deleted"}), 200 # response -> OK

# helper method
def get_first_free_id():
    existing_ids = [m.id for m in Monastery.get_all()]
    if not existing_ids:
      return 1
    existing_ids.sort()
    for i in range(1, max(existing_ids) + 1):
      if i not in existing_ids:
        return i
    return max(existing_ids) + 1
  
# handle errors in json format
@app.errorhandler(MonasteryError)
def handle_monastery_error(error):
    return jsonify({"error": error.message}), error.status_code

@app.errorhandler(DbConnectionError)
def handle_db_error(error):
    return jsonify({"error": error.message}), error.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader = False)