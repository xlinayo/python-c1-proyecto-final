# odonto_admin es el Microservicio 1: Usuarios/Auth + Admin. Se trata de arquitectura distribuida y microservicios
# Este mismo archivo run.py es el punto de entrada para arrancar el servicio, se separa lo que sería el arranque del resto del código
# para más claridad y está reflejado en las buenas prácticas de estructura que indican que no se debe tener todo en un único archivo
# Se utiliza Flask para ejecutar la app
# (Tema 2: REST API con Flask)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5001, debug = True)