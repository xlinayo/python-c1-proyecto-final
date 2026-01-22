# Punto de entrada del microservicio de citas
# Crea Flask y arranca el servidor
# Define el puerto del microservicio
# (Tema 2: API REST con Flask y Tema 4: Arquitectra distribuida y microsservicios)
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
