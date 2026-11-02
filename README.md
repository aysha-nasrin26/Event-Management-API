# Event Management API

A backend REST API built with **Python and FastAPI** to create, manage, and organize events with secure user authentication, database integration, and AI-powered event description generation.

## 🚀 Project Overview

The Event Management API allows registered users to create and manage their own events. It provides secure authentication, event ownership, filtering, pagination, and automated event description generation using Google Gemini AI.

The project demonstrates practical backend development concepts, database management, API security, testing, and containerization.

## ✨ Features

- **User Authentication:** Register and log in using JWT-based authentication.
- **Event Management:** Create, retrieve, update, and delete events.
- **Event Ownership:** Users can manage only the events they own.
- **Data Validation:** Validate incoming request data using Pydantic.
- **Filtering:** Retrieve events based on selected criteria, such as location.
- **Pagination:** Retrieve records using `skip` and `limit` parameters.
- **Database Relationships:** One-to-many relationship between users and events.
- **Database Migrations:** Manage database schema changes using Alembic.
- **AI Integration:** Generate event descriptions using Google Gemini AI when a description is not provided.
- **API Testing:** Test API endpoints and access restrictions using Pytest and FastAPI TestClient.
- **Docker Support:** Run the API and PostgreSQL database using Docker Compose.
- **API Documentation:** Explore and test endpoints through Swagger UI.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Data Validation | Pydantic |
| Authentication | JWT |
| Database Migrations | Alembic |
| AI Integration | Google Gemini API |
| Testing | Pytest, FastAPI TestClient |
| Containerization | Docker, Docker Compose |
| API Documentation | Swagger UI, OpenAPI |
| Version Control | Git, GitHub |

## 📂 Project Structure

```text
Event-Management-API/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── services/
│   └── ai_services.py
│
├── tests/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── security.py
│
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md
```

## 🔐 Authentication and Authorization

The application uses JWT-based authentication to protect private API endpoints.

1. A user registers with their details.
2. The user logs in with their credentials.
3. The application generates an access token.
4. The client sends the token in the Authorization header.
5. FastAPI verifies the token before allowing access to protected endpoints.

**Event Ownership:** Each event is associated with its creator through a foreign key (`user_id`). Users cannot update or delete events belonging to other users.

## 🗄️ Database Design

The application uses PostgreSQL with SQLAlchemy ORM.

### Users Table

| Column | Description |
|---|---|
| id | Primary key |
| name | User name |
| email | Unique user email |
| password_hash | Hashed password |

### Events Table

| Column | Description |
|---|---|
| id | Primary key |
| title | Event title |
| description | Event description |
| location | Event location |
| event_date | Event date |
| start_time | Event start time |
| end_time | Event end time |
| category | Event category |
| max_attendees | Maximum attendees |
| status | Event status |
| user_id | Foreign key referencing users |

**Relationship:** One user can create multiple events, while each event belongs to one user.

## 🤖 AI Integration

Google Gemini AI is integrated to generate event descriptions.

When a user creates an event without providing a description, the application uses the event details to request an AI-generated description.

The AI functionality is maintained separately in the `services/ai_services.py` module to keep the application organized.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aysha-nasrin26/Event-Management-API.git
cd Event-Management-API
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/Event
SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
```

Replace the sample values with your own database credentials and API keys.

**Important:** Never upload your actual `.env` file or secret keys to GitHub.

### 5. Run database migrations

Make sure PostgreSQL is running and the configured database exists.

```bash
alembic upgrade head
```

### 6. Start the FastAPI application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 📖 API Documentation

FastAPI automatically generates interactive API documentation.

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

Use Swagger UI to explore endpoints, provide request data, and test API responses.

## 🐳 Run with Docker

The project includes Docker support for running the API and PostgreSQL database in containers.

Start the application:

```bash
docker compose up --build
```

Stop the containers:

```bash
docker compose down
```

The API is configured to be accessible through:

```text
http://localhost:8001
```

For Docker execution, configure the database connection to use the PostgreSQL Compose service name (`db`) as the database host.

## 🧪 Run Tests

Run the test suite using:

```bash
pytest -v
```

The tests cover API operations and important scenarios, including:

- Retrieving events
- Creating events
- Updating events
- Deleting events
- Authentication requirements
- Invalid event handling
- Event ownership restrictions

## 🔒 Security Practices

- JWT-based authentication for protected endpoints.
- Password hashing rather than storing plain-text passwords.
- Ownership checks for event modification and deletion.
- Environment variables for sensitive configuration.
- Input validation using Pydantic.

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Building RESTful APIs using FastAPI.
- Working with SQLAlchemy ORM and relational databases.
- Implementing JWT authentication and authorization.
- Managing database relationships and migrations.
- Integrating AI services into backend applications.
- Writing API tests using Pytest.
- Containerizing applications using Docker.
- Organizing backend code into maintainable modules.

## 👩‍💻 Author

**Aysha Nasrin M**

BCA Gold Medalist | Aspiring Full Stack Python Developer

- GitHub: https://github.com/aysha-nasrin26
- LinkedIn: https://www.linkedin.com/in/aysha-nasrin

---

⭐ If you find this project useful, feel free to explore the repository!
