from pymongo import MongoClient
import uuid
from datetime import datetime

# 1. Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
db = client["taskmanager"]
tasks_collection = db["tasks"]

print("🧹 Limpiando tareas anteriores...")
tasks_collection.delete_many({}) 

# 2. Lista masiva de 20 tareas mapeadas a los USUARIOS REALES actuales
tareas_base = [
    # --- TAREAS DE CARLOS ZAZUETA (Admin) ---
    {"title": "Revisar permisos de usuarios", "description": "Auditar la tabla de usuarios y asignar roles correctamente.", "status": "completed", "assignee": "Carlos Zazueta", "startDate": "2026-03-25", "endDate": "2026-03-30"},
    {"title": "Presentación de Q1", "description": "Preparar diapositivas para la junta de inversores.", "status": "pending", "assignee": "Carlos Zazueta", "startDate": "2026-04-10", "endDate": "2026-04-15"},
    {"title": "Entrevistas para QA", "description": "Entrevistar a los 3 candidatos finales para el puesto de QA.", "status": "in-progress", "assignee": "Carlos Zazueta", "startDate": "2026-04-01", "endDate": "2026-04-05"},
    {"title": "Aprobar presupuesto de AWS", "description": "Revisar los costos proyectados para el nuevo servidor.", "status": "pending", "assignee": "Carlos Zazueta", "startDate": "2026-04-05", "endDate": "2026-04-07"},
    
    # --- TAREAS DE ANA V. ---
    {"title": "Diseñar nueva Landing Page", "description": "Crear wireframes y mockups de alta fidelidad en Figma.", "status": "completed", "assignee": "Ana V.", "startDate": "2026-03-25", "endDate": "2026-03-30"},
    {"title": "Optimización SEO", "description": "Mejorar meta tags y tiempos de carga de la web principal.", "status": "pending", "assignee": "Ana V.", "startDate": "2026-04-10", "endDate": "2026-04-15"},
    {"title": "Variaciones de Logo", "description": "Diseñar 3 opciones en modo oscuro para la nueva marca.", "status": "in-progress", "assignee": "Ana V.", "startDate": "2026-04-01", "endDate": "2026-04-05"},
    {"title": "Implementar Feedback de Cliente", "description": "Cambiar la paleta de colores del dashboard según la última junta.", "status": "on-review", "assignee": "Ana V.", "startDate": "2026-04-01", "endDate": "2026-04-04"},
    {"title": "Ilustraciones para Blog", "description": "Crear 5 vectores para los nuevos artículos.", "status": "completed", "assignee": "Ana V.", "startDate": "2026-03-15", "endDate": "2026-03-20"},
    
    # --- TAREAS DE BEN L. ---
    {"title": "Configurar Servidor AWS", "description": "Levantar instancia EC2 y configurar balanceador de carga.", "status": "in-progress", "assignee": "Ben L.", "startDate": "2026-04-01", "endDate": "2026-04-05"},
    {"title": "Arreglar CSS en Móvil", "description": "El menú hamburguesa no se abre en iPhone 13.", "status": "on-review", "assignee": "Ben L.", "startDate": "2026-04-01", "endDate": "2026-04-02"},
    {"title": "Auditoría de Dependencias", "description": "Actualizar librerías de Node.js que tengan vulnerabilidades.", "status": "completed", "assignee": "Ben L.", "startDate": "2026-03-28", "endDate": "2026-03-29"},
    {"title": "Integrar pasarela de pago", "description": "Conectar Stripe en el checkout principal.", "status": "blocked", "assignee": "Ben L.", "startDate": "2026-04-02", "endDate": "2026-04-09"},
    {"title": "Refactorizar Componente Login", "description": "Pasar el componente a Reactive Forms para mejorar seguridad.", "status": "completed", "assignee": "Ben L.", "startDate": "2026-03-20", "endDate": "2026-03-25"},

    # --- TAREAS DE DIEGO ---
    {"title": "Migración de Base de Datos", "description": "Pasar registros antiguos de MySQL a MongoDB.", "status": "blocked", "assignee": "Diego", "startDate": "2026-03-28", "endDate": "2026-04-05"},
    {"title": "Corrección de Bug en Login", "description": "El usuario se queda en pantalla blanca al iniciar sesión.", "status": "completed", "assignee": "Diego", "startDate": "2026-04-01", "endDate": "2026-04-02"},
    {"title": "Configurar CI/CD", "description": "Automatizar despliegues con GitHub Actions.", "status": "blocked", "assignee": "Diego", "startDate": "2026-04-02", "endDate": "2026-04-09"},
    {"title": "Plantillas de Email HTML", "description": "Maquetar correos de recuperación de contraseña y bienvenida.", "status": "in-progress", "assignee": "Diego", "startDate": "2026-04-01", "endDate": "2026-04-06"},
    {"title": "Documentación de API", "description": "Escribir endpoints en Swagger para los desarrolladores móviles.", "status": "pending", "assignee": "Diego", "startDate": "2026-04-15", "endDate": "2026-04-20"},
    {"title": "Testing QA - Release 1.2", "description": "Probar todos los flujos de pago antes de salir a producción.", "status": "in-progress", "assignee": "Diego", "startDate": "2026-04-02", "endDate": "2026-04-08"}
]

print("🌱 Generando llaves de idempotencia y fechas de creación...")

# 3. Formateamos las tareas para que incluyan los nuevos campos
tareas_demo = []
for tarea in tareas_base:
    tarea_completa = tarea.copy()
    tarea_completa["idempotency_key"] = str(uuid.uuid4())
    tarea_completa["createdAt"] = datetime.utcnow()
    tareas_demo.append(tarea_completa)

# 4. Insertamos las tareas
if tareas_demo:
    tasks_collection.insert_many(tareas_demo)
    print(f"✅ ¡Se inyectaron {len(tareas_demo)} tareas idempotentes con éxito!")

print("🎉 ¡Base de datos de tareas sincronizada con tus usuarios!")