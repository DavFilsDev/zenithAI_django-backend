# ZenithAI Documentation

## 📚 Documentation Structure

```
docs/
├── api/                                          # API documentation
│   ├── zenith-ai-api.postman_collection.json       # Postman collection
│   ├── zenith-ai-api.postman_environment.json      # Postman environment
│   └── api-documentation.md                        # Manual API docs
└── README.md                                     # This file
```

## 🚀 Quick Start

### Using Postman

1. Open Postman
2. Click "Import" → "Upload Files"
3. Select both:
   - `api/zenith-ai-api.postman_collection.json`
   - `api/zenith-ai-api.postman_environment.json`
4. Select "Zenith AI - Development" environment from dropdown
5. Start testing!

### Testing Flow

1. **Register** a new user
2. **Login** to get tokens (automatically saved in environment)
3. **Create conversation**
4. **Send messages**
5. **View conversations**

## 🔧 Environment Variables

- `base_url`: API base URL (default: http://127.0.0.1:8000)
- `access_token`: Automatically set after login
- `refresh_token`: Automatically set after login
- `conversation_id`: ID of current conversation

## 📖 API Reference

See [API Documentation](api/api-documentation.md) for detailed endpoint information.

## 🔄 Updating Documentation

When adding new endpoints:
1. Update Postman collection JSON
2. Update API documentation markdown
3. Commit changes to repository
```