# prueba_beitech
El desarrollo del API se hizo con el framework flask y postgesSQL
Version de python 3.9.12
# configuraciones a tener en cuenta
1.	Instalar flask  (pip install flask).
2.	Subir el API (FLASK run)
3.	Configurar modo de desarrollo   CMD WINDOWS(set FLASK_APP=app.py,  set FLASK_ENV=development)
4.	Instalar sqlalchemy (pip install flask-sqlalchemy)
5.	pip install flask-migrate
6.	pip install psycopg2 (se uso postgres sql)
7.	flask db init --  crea el directorio con la migraciones
8.	flask db migrate --  genera el sql a ejecutar
9.	flask db upgrade – creación de tablas en base de datos
10.	flask db stamp head – actualiza todo a la ultima version
