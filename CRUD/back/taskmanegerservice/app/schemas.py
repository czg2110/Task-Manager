def serialize_task(task):
    if not task:
        return None
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description", ""),
        "status": task.get("status", "pending"),
        "createdAt": task.get("createdAt").isoformat() if "createdAt" in task else None,
        "assignee": task.get("assignee", ""),
        "startDate": task.get("startDate", ""),
        "endDate": task.get("endDate", "")
    }


def validate_task_create(data):
    if not data or not data.get('title'):
        raise ValueError("El título es obligatorio.")
    return data


def serialize_user(user):
    if not user:
        return None
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }