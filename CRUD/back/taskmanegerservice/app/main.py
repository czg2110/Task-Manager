from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from app.service import TaskService, AuthService
from app.repository import users_collection
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    idem_key = request.headers.get('Idempotency-Key')
    new_task = TaskService.create(data, idempotency_key=idem_key)
    
    socketio.emit('task_created', new_task) 
    return jsonify(new_task), 201

@app.route('/api/tasks/<id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    updated_task = TaskService.update(id, data)
    
    socketio.emit('task_updated', updated_task)
    return jsonify(updated_task), 200

@app.route('/api/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    TaskService.delete(id)
    
    socketio.emit('task_deleted', id)
    return jsonify({"message": "Deleted"}), 200

# LOGIN
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    auth_data = AuthService.login(data.get('email'), data.get('password'))
    
    if auth_data:
        return jsonify(auth_data), 200
    else:
        return jsonify({"error": "Correo o contraseña incorrectos"}), 401


# ADMINISTRACIÓN DE USUARIOS
@app.route('/api/users', methods=['GET'])
def get_users():
    users = []
    for u in users_collection.find():
        users.append({
            "id": str(u["_id"]),
            "name": u["name"],
            "email": u["email"],
            "role": u.get("role", "user")
        })
    return jsonify(users), 200

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or 'token-seguro-' not in auth_header: return jsonify({"error": "No token"}), 401
    
    admin_id = auth_header.split("token-seguro-")[1]
    admin_user = users_collection.find_one({"_id": ObjectId(admin_id)})
    if not admin_user or admin_user.get("role") != "admin": return jsonify({"error": "Denegado"}), 403
    
    if str(admin_id) == str(user_id): 
        return jsonify({"error": "No puedes eliminarte a ti mismo"}), 400
        
    users_collection.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": "Usuario eliminado"}), 200

@app.route('/api/users/<user_id>/role', methods=['PUT'])
def update_role(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or 'token-seguro-' not in auth_header: return jsonify({"error": "No token"}), 401
    
    admin_id = auth_header.split("token-seguro-")[1]
    admin_user = users_collection.find_one({"_id": ObjectId(admin_id)})
    if not admin_user or admin_user.get("role") != "admin": return jsonify({"error": "Denegado"}), 403
    
    data = request.get_json()
    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": data.get("role")}})
    return jsonify({"message": "Rol actualizado"}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'token-seguro-' not in auth_header: return jsonify({"error": "No token"}), 401
            
        admin_id = auth_header.split("token-seguro-")[1]
        admin_user = users_collection.find_one({"_id": ObjectId(admin_id)})
        
        if not admin_user or admin_user.get("role") != "admin": return jsonify({"error": "Denegado"}), 403

        data = request.get_json()
        from werkzeug.security import generate_password_hash
        from datetime import datetime
        
        new_user = {
            "name": data.get('name'),
            "email": data.get('email'),
            "password": generate_password_hash(data.get('password')),
            "role": data.get('role', 'user'), 
            "createdAt": datetime.utcnow()
        }
        result = users_collection.insert_one(new_user)
        new_user["_id"] = str(result.inserted_id)
        del new_user["password"]
        
        return jsonify(new_user), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)