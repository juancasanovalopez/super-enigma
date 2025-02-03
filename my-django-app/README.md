# My Django App

This is a simple Django project that uses an SQLite database. Below are the instructions to set up and run the application.

## Prerequisites

- Python 3.x
- Docker (optional, for containerization)
- Docker Compose (optional, for orchestration)

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

- Access the application at `http://127.0.0.1:8000/`.
- Use the Django admin interface at `http://127.0.0.1:8000/admin/` (create a superuser to access it).

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.