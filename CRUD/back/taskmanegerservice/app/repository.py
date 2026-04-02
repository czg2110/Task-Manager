from datetime import datetime
from bson.objectid import ObjectId
from .database import tasks_collection, users_collection
class TaskRepository:
    @staticmethod
    def get_all_tasks():
        return list(tasks_collection.find().sort("createdAt", -1))

    @staticmethod
    def get_task_by_id(task_id):
        return tasks_collection.find_one({"_id": ObjectId(task_id)})

    @staticmethod
    def create_task(title, description, status, assignee, start_date, end_date, idempotency_key=None):
        if idempotency_key:
            existing_task = tasks_collection.find_one({"idempotency_key": idempotency_key})
            if existing_task:
                print("♻️ Petición duplicada detectada. Devolviendo tarea existente.")
                return existing_task 
                
        new_task = {
            "title": title,
            "description": description,
            "status": status,
            "assignee": assignee,
            "startDate": start_date,
            "endDate": end_date,
            "idempotency_key": idempotency_key,
            "createdAt": datetime.utcnow()
        }
        result = tasks_collection.insert_one(new_task)
        new_task["_id"] = result.inserted_id
        return new_task

    @staticmethod
    def update_task(task_id, data):
        update_fields = {}
        if 'title' in data: update_fields['title'] = data['title']
        if 'description' in data: update_fields['description'] = data['description']
        if 'status' in data: update_fields['status'] = data['status']
        if 'assignee' in data: update_fields['assignee'] = data['assignee']
        if 'startDate' in data: update_fields['startDate'] = data['startDate']
        if 'endDate' in data: update_fields['endDate'] = data['endDate']

        tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_fields}
        )
        return TaskRepository.get_task_by_id(task_id)

    @staticmethod
    def delete_task(task_id):
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0


class UserRepository:
    @staticmethod
    def get_user_by_email(email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def create_user(name, email, password_hash, role="user"):
        new_user = {
            "name": name,
            "email": email,
            "password": password_hash,
            "role": role,
            "createdAt": datetime.utcnow()
        }
        result = users_collection.insert_one(new_user)
        new_user["_id"] = result.inserted_id
        return new_user

    @staticmethod
    def get_all_users():
        return list(users_collection.find().sort("name", 1))