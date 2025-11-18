# Proyecto_Final_Back
Este es el Backend del proyecto final de la Tecnicatura Universitaria en Programación de la Universidad Tecnologia de Tucumán

## Puesta en marcha rápida

1. Crear el archivo `.env` en la raíz con algo como:

```
FLASK_ENV=development
SECRET_KEY=dev-secret
SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:password@localhost:3306/devvproyectofinal?charset=utf8mb4
```

2. Crear el esquema en MySQL (usa el script incluido como referencia):

```
mysql -u <user> -p -e "SOURCE docs/devvproyectofinal_schema.sql"
```

3. Aplicar migraciones y correr la app:

```
flask --app manage.py db upgrade
flask --app manage.py run
```

Los endpoints expuestos quedan bajo `http://localhost:5000/api/v1`.
