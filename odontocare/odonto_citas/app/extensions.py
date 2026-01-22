# Inicializa SQLAlchemy. Mantiene la base de datos de citas separada de admin y evita el acoplamiento de servicios
# (Tema 3b: ORM y persistencia. Separación de bases de datos por servicio)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
