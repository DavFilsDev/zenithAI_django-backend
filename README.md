# Backend Repository README

## Chatbot Platform - Backend (Django + PostgreSQL)

### 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/DavFilsDev/zenithAI_django-backend.git
cd zenithAI_django-backend

# Set up virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your configuration

# Run with Docker (recommended)
docker-compose up --build

# Or run locally (requires PostgreSQL running)
python manage.py migrate
python manage.py runserver
```

### 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
- Git

### 🏗️ Project Structure

```
chatgpt-backend/
├── backend/          # Django project settings
├── chat/            # Chat app (conversations, messages)
├── users/           # User management app
├── requirements.txt # Python dependencies
├── .env.example     # Environment variables template
├── docker-compose.yml # Docker setup
└── Dockerfile       # Container configuration
```

### 🔧 Configuration

1. **Environment Variables** (`/.env`):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=chatgpt_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

2. **Database Setup**:
   - Using Docker: `docker-compose up`
   - Manual: Create PostgreSQL database named `chatgpt_db`

### 🐳 Docker Deployment

```bash
# Build and start containers
docker-compose up --build

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### 📚 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | User registration | No |
| POST | `/api/auth/token/` | Get JWT token | No |
| GET | `/api/auth/profile/` | User profile | Yes |
| GET | `/api/chat/conversations/` | List conversations | Yes |
| POST | `/api/chat/conversations/` | Create conversation | Yes |
| GET | `/api/chat/conversations/{id}/` | Conversation detail | Yes |
| POST | `/api/chat/chat/` | Send message (new conversation) | Yes |
| POST | `/api/chat/chat/{id}/` | Send message (existing conversation) | Yes |

### 🔌 API Documentation

- **📊 Interactive API Testing**: [Swagger UI](/api/docs/)
- **📖 Readable Reference**: [ReDoc](/api/redoc/)
- **📋 OpenAPI Schema**: [schema.json](/api/schema/)


### 🔐 Authentication

Uses JWT (JSON Web Tokens) for authentication:
- Access tokens valid for 1 day
- Refresh tokens valid for 7 days
- Include token in headers: `Authorization: Bearer <token>`

### 🗄️ Database Models

#### User Model
- Custom user with email as username
- API key storage
- Credit system
- Premium status

#### Conversation Model
- Belongs to a user
- Has many messages
- Title and timestamps

#### Message Model
- Belongs to a conversation
- Role (user/assistant/system)
- Content and token count

### 🧪 Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test chat
```

### 🚀 Deployment

#### Free Options:
1. **Railway.app** (recommended)
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login and deploy
   railway login
   railway up
   ```

2. **Render.com**
   - Connect GitHub repository
   - Set environment variables
   - Deploy with PostgreSQL addon

3. **Fly.io**
   ```bash
   # Install Fly CLI
   curl -L https://fly.io/install.sh | sh
   
   # Deploy
   fly launch
   fly deploy
   ```

### 📈 Monitoring

- Django Admin: `/admin/`
- Database: Use Django shell or pgAdmin
- Logs: Check Docker logs or server logs

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### 📄 License

MIT License - see LICENSE file for details

### 🆘 Support

- Issues: [GitHub Issues](https://github.com/DavFilsDev/zenithAI_django-backend/issues)
- Documentation: Check the Wiki
- Email: miharisoadavidfils@gmail.com

---

**Author:** Fanampinirina Miharisoa David Fils RATIANDRAIBE