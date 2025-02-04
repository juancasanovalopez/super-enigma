# My Django App

This is a simple Django project that uses an SQLite database. Below are the instructions to set up and run the application.

## Prerequisites

- Python 3.x
- Docker (optional, for containerization)
- Docker Compose (optional, for orchestration)
- AWS EC2 Instance

## Setup Instructions

### Local Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-django-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```

### Docker Setup

1. Build the Docker image:
   ```
   docker-compose build
   ```

2. Run the application:
   ```
   docker-compose up
   ```

## Usage

- Access the application at `http://127.0.0.1:1000/`.
- Use the Django admin interface at `http://127.0.0.1:8000/admin/` (create a superuser to access it).


Desplegar una aplicación Django contenedorizada en Docker en dos entornos:
	1.	Servidor Local (Pruebas)
	2.	AWS EC2 (Producción)

GitHub Actions para automatizar el despliegue en ambos entornos.

1. Configuración del Proyecto con Docker

Asegúrate de que tu aplicación Django tenga los siguientes archivos:

1.1. Dockerfile (para Django)

# Usa una imagen oficial de Python
FROM python:3.9

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mi_proyecto.wsgi:application"]

1.2. docker-compose.yml

version: '3.8'

services:
  db:
    image: postgres:13
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_DB: mi_bd
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: contraseña
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    container_name: django_app
    restart: always
    depends_on:
      - db
    ports:
      - "8000:8000"
    environment:
      DEBUG: "False"
      DATABASE_URL: "postgres://usuario:contraseña@db:5432/mi_bd"

volumes:
  pgdata:

2. Despliegue en Servidor Local (Pruebas)

Asegúrate de tener instalado Docker en tu servidor de pruebas.

2.1. Configurar Servidor Local
	1.	Instala Docker y Docker Compose:

sudo apt update && sudo apt install -y docker.io docker-compose


	2.	Copia el código fuente de Django al servidor de pruebas.
	3.	Construye y ejecuta los contenedores:

docker-compose up -d --build


	4.	Verifica que el contenedor esté corriendo:

docker ps

	5.	Accede a http://localhost:8000 para verificar la aplicación.

3. Despliegue en AWS EC2 (Producción)

3.1. Configurar la instancia EC2
	1.	Crea una instancia EC2 (Ubuntu 22.04)
	2.	Abre los puertos en el Security Group:
	•	22 (SSH)
	•	80 (HTTP)
	•	443 (HTTPS)
	•	8000 (para pruebas, opcional)
	•	5432 (si usas PostgreSQL externo)
	3.	Conéctate a la instancia por SSH:

ssh -i "mi_clave.pem" ubuntu@mi-servidor-aws


	4.	Instala Docker y Docker Compose:

sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker


	5.	Clona el repositorio de la aplicación Django:

git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio


	6.	Levanta los contenedores en AWS:

docker-compose up -d --build


	7.	Verifica el estado de los contenedores:

docker ps


	8.	Configurar Nginx (opcional)
Si deseas usar Nginx como proxy inverso, instala Nginx:

sudo apt install nginx -y

Configura /etc/nginx/sites-available/django:

server {
    listen 80;
    server_name mi-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

Habilita la configuración:

sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled
sudo systemctl restart nginx

4. Automatización con GitHub Actions

Para desplegar automáticamente la aplicación en entorno de pruebas y producción, crea un archivo:

.github/workflows/deploy.yml

4.1. Configurar Secrets en GitHub

Define las siguientes secrets en GitHub → Settings → Secrets:
	•	AWS_SSH_KEY → Clave privada .pem
	•	AWS_HOST → IP pública de AWS
	•	AWS_USER → ubuntu
	•	LOCAL_HOST → IP del servidor de pruebas
	•	LOCAL_USER → Usuario SSH del servidor local

4.2. Archivo deploy.yml

name: Deploy Django to Local & AWS

on:
  push:
    branches:
      - develop  # Para pruebas
      - main  # Para producción

jobs:
  deploy-test:
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Deploy to Local Server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.LOCAL_HOST }}
          username: ${{ secrets.LOCAL_USER }}
          key: ${{ secrets.AWS_SSH_KEY }}
          script: |
            cd /home/${{ secrets.LOCAL_USER }}/tu_proyecto
            git pull origin develop
            docker-compose down
            docker-compose up -d --build

  deploy-prod:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Deploy to AWS EC2
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.AWS_HOST }}
          username: ${{ secrets.AWS_USER }}
          key: ${{ secrets.AWS_SSH_KEY }}
          script: |
            cd /home/ubuntu/tu_proyecto
            git pull origin main
            docker-compose down
            docker-compose up -d --build

5. Verificación del Despliegue

5.1. Entorno de Pruebas
	•	URL: http://LOCAL_IP:8000

5.2. Producción (AWS)
	•	URL: http://AWS_PUBLIC_IP

Si usaste un dominio:
	•	http://tu-dominio.com

6. Configurar HTTPS con Let’s Encrypt (Opcional)

Si usas un dominio, instala Let’s Encrypt para HTTPS:

sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com

Renovación automática:

sudo crontab -e

Añade:

0 0 1 * * certbot renew --quiet

Resumen del Pipeline

Acción	Rama	Desplegado en
push	develop	Servidor de pruebas (Docker)
push	main	AWS EC2 (Producción)

Con esta configuración, cada cambio en develop o main se reflejará automáticamente en el servidor de pruebas o en producción mediante Docker y GitHub Actions.

¡Tu despliegue ahora es completamente automatizado!