# Cliente externo que consume la API con request y ejecuta el flujo al completo,
# demuestra que la API funciona desde fuera
# Documenta pruebas de endpoints
# (Tema 2: Consumo de API REST, Tema 4: Comunicación entre servicios)

import json
from datetime import datetime, timedelta
import requests
import os

ADMIN_BASE = os.getenv("ADMIN_BASE_URL", "http://localhost:5001")
CITAS_BASE  = os.getenv("CITAS_BASE_URL",  "http://localhost:5002")

def pretty(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)

def req(method: str, url: str, *, token: str | None = None, json_body=None):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    r = requests.request(method, url, headers=headers, json=json_body, timeout=10)

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    print(f"\n[{method}] {url}")
    if json_body is not None:
        print("Request JSON:")
        print(pretty(json_body))
    print(f"Status: {r.status_code}")
    print("Response JSON:")
    print(pretty(data))

    return r.status_code, data

def login_admin(username="admin", password="admin123") -> str:
    status, data = req(
        "POST",
        f"{ADMIN_BASE}/auth/login",
        json_body={"username": username, "password": password},
    )
    if status != 200 or not data.get("ok"):
        raise RuntimeError("Login failed")
    return data["token"]

def create_patient(token: str, name: str, active: bool = True):
    return req(
        "POST",
        f"{ADMIN_BASE}/admin/pacientes",
        token=token,
        json_body={"name": name, "active": active},
    )

def create_doctor(token: str, name: str, specialty: str | None = None, active: bool = True):
    body = {"name": name, "active": active}
    if specialty is not None:
        body["specialty"] = specialty
    return req("POST", f"{ADMIN_BASE}/admin/doctors", token=token, json_body=body)

def create_center(token: str, name: str, address: str | None = None, active: bool = True):
    body = {"name": name, "active": active}
    if address is not None:
        body["address"] = address
    return req("POST", f"{ADMIN_BASE}/admin/centers", token=token, json_body=body)

def create_appointment(token: str, doctor_id: int, center_id: int, patient_name: str, when_iso: str):
    return req(
        "POST",
        f"{CITAS_BASE}/appointments",
        token=token,
        json_body={
            "doctor_id": doctor_id,
            "center_id": center_id,
            "patient_name": patient_name,
            "appointment_time": when_iso,
        },
    )

def main():
    # 0) checks
    req("GET", f"{ADMIN_BASE}/ping")
    # /ping en citas puede no existir en tu versión; se comprueba existencia de appointments
    req("GET", f"{CITAS_BASE}/appointments")  # debería dar 405

    # 1) Login  token
    token = login_admin()
    print("\nTOKEN OK ✅")

    # 2) Crear datos base 
    # Evita tildes o no funciona
    create_patient(token, "Xeila", True)
    create_doctor(token, "Dr Brais", "Maxilofacial", True)
    create_center(token, "Batalla", "Centro Rib 3", True)

    # 3) Crear cita en una hora futura cercana (para no pisar citas anteriores)
    when = (datetime.now() + timedelta(minutes=5)).replace(second=0, microsecond=0)
    when_iso = when.isoformat()

    # doctor_id=1 y center_id=1 (ya se sabe que existen)
    status_ok, _ = create_appointment(token, doctor_id=1, center_id=1, patient_name="Ana Perez", when_iso=when_iso)

    # 4) Probar conflicto: misma hora / mismo doctor
    if status_ok in (200, 201):
        create_appointment(token, doctor_id=1, center_id=1, patient_name="Luis Gomez", when_iso=when_iso)

    # 5) Probar NOT_FOUND: doctor inexistente
    create_appointment(token, doctor_id=999, center_id=1, patient_name="Ana Perez", when_iso=(when + timedelta(hours=1)).isoformat())

    print("\nDEMO COMPLETA ✅")

if __name__ == "__main__":
    main()
