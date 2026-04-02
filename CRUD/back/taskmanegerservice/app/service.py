from werkzeug.security import generate_password_hash, check_password_hash
from .repository import TaskRepository, UserRepository
from .schemas import serialize_task, validate_task_create, serialize_user

class TaskService:
    @staticmethod
    def get_all():
        tasks = TaskRepository.get_all_tasks()
        return [serialize_task(task) for task in tasks]

    @staticmethod
    def create(data, idempotency_key=None):
        valid_data = validate_task_create(data)
        new_task = TaskRepository.create_task(
            title=valid_data['title'],
            description=valid_data.get('description', ''),
            status=valid_data.get('status', 'pending'),
            assignee=valid_data.get('assignee', ''),
            start_date=valid_data.get('startDate', ''),
            end_date=valid_data.get('endDate', ''),
            idempotency_key=idempotency_key
        )
        return serialize_task(new_task)
    @staticmethod
    def update(task_id, data):
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            return None
            
        updated_task = TaskRepository.update_task(task_id, data)
        return serialize_task(updated_task)

    @staticmethod
    def delete(task_id):
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            return False
            
        TaskRepository.delete_task(task_id)
        return True

class AuthService:
    @staticmethod
    def register(name, email, password):
        if UserRepository.get_user_by_email(email):
            raise ValueError("El correo ya está registrado.")
            
        hashed_password = generate_password_hash(password)
        user = UserRepository.create_user(name, email, hashed_password)
        return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}

    @staticmethod
    def login(email, password):
        user = UserRepository.get_user_by_email(email)
        
        if user and "password" in user and check_password_hash(user["password"], password):
            return {
                "token": "token-seguro-" + str(user["_id"]), 
                "user": {
                    "id": str(user["_id"]), 
                    "name": user["name"], 
                    "email": user["email"],
                    "role": user.get("role", "user")
                }
            }
        return None

    @staticmethod
    def get_all_users():
        users = UserRepository.get_all_users()
        return [serialize_user(user) for user in users]