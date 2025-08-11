"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code



@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/member', methods=['GET'])
def handle_hello():
  
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200

@app.route('/members/<int_id>', methods=['GET'])
def get_member(member_id):
   
     if member_id <= 0 :
        return jsonify({"error": "El id debe ser un numero positivo"}), 400
     

     member = jackson_family.get_member(member_id)
    

     if member is None:
        return jsonify({"error": "miembro no encontrado"}), 400

     return jsonify(member), 200

@app.route('/members', methods=['POST'])
def add_member():
    if not request.is_json:
        return jsonify({"error": "La solicitud debe tener content-type: application/json"}), 400

    data = request.get_json()

    if not data or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    new_member = {
        "first_name": data["first_name"],
        "age": data["age"],
        "lucky_numbers": data["lucky_numbers"]
    }

    if "id" in data:
        new_member["id"] = data["id"]

    jackson_family.add_member(new_member)

    return jsonify({"mensaje": "Miembro agregado correctamente", "miembro": new_member}), 200

   
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if member_id <= 0:
        return jsonify({"error": "El ID debe ser un número positivo"}), 400

    was_deleted = jackson_family.delete_member(member_id)

    if was_deleted:
        return jsonify({"mensaje": f"Miembro con ID {member_id} eliminado"}), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404   

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
