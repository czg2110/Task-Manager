from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["taskmanager"]
users_collection = db["users"]

print("🧹 Limpiando usuarios antiguos...")
users_collection.delete_many({})

# 👇 AQUÍ ESTÁ LA MAGIA: Tú eres el admin, los demás son usuarios normales
usuarios_demo = [
    {"name": "Carlos Zazueta", "email": "admin@empresa.com", "password": "123456", "role": "admin"},
    {"name": "Ana V.", "email": "ana@empresa.com", "password": "password123", "role": "user"},
    {"name": "Ben L.", "email": "ben@empresa.com", "password": "password123", "role": "user"},
    {"name": "Diego", "email": "diego@empresa.com", "password": "password123", "role": "user"}
]

for u in usuarios_demo:
    nuevo_usuario = {
        "name": u["name"],
        "email": u["email"],
        "password": generate_password_hash(u["password"]), 
        "role": u["role"], # 👈 Inyectamos el rol
        "createdAt": datetime.utcnow()
    }
    users_collection.insert_one(nuevo_usuario)
    print(f"{'👑 ADMIN' if u['role'] == 'admin' else '👤 USER'}: {u['name']} inyectado.")

print("🎉 ¡Roles asignados!")