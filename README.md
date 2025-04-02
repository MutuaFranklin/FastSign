# FastSign - Digital Signature Solution

A FastAPI-based digital signature solution that enables users to sign documents electronically. Built with FastAPI, MySQL, and JWT authentication.

## Project Overview

FastSign allows users to:
- Upload and manage documents
- Create and store digital signatures
- Sign documents securely
- Share signed documents via secure links

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: MySQL
- **Authentication**: JWT (OAuth2)
- **File Processing**: PyPDF2, Pillow
- **Development Environment**: Laragon


## API Endpoints

### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/token` - Login and get access token

### Documents
- `POST /documents/upload` - Upload new document
- `GET /documents/list` - List user's documents
- `GET /documents/metadata/{access_token}` - Retrieve metadata for a document using its access token
- `GET /documents/view/{access_token}` - View the document directly (signed if available, otherwise the original)

### Signatures
- `POST /signatures/add-signature/` - Create new signature
  - **Request Body**: 
    ```json
    {
      "document_id": 1,
      "signature_type": "drawn",
      "signature_data": "path/to/signature/image.png"
    }
    ```
  - **Response**: Returns the created signature details.


## Setup Instructions

### Standard Setup
1. **Prerequisites**
   - Python 3.8+
   - MySQL (via Laragon)
   - Git

2. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd FastSign
   ```

3. **Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Database Setup**
   ```sql
   CREATE DATABASE fastsign;
   ```

6. **Environment Configuration**
   Create `.env` file:
   ```
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL=mysql://root@localhost:3306/fastsign
   ```

7. **Run Application**
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup

1. **Prerequisites**
   - Docker
   - Docker Compose

2. **Build and Run**
   ```bash
   # Build and start containers
   docker-compose up --build

   # Run in background
   docker-compose up -d
   ```

3. **Stop Containers**
   ```bash
   docker-compose down
   ```

The application will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- MySQL: localhost:3306

## Development

- API Documentation: http://localhost:8000/docs
- Database tables are auto-created on first run
- JWT tokens required for protected endpoints
- File uploads stored in local filesystem

## Security Features

- Password hashing with bcrypt
- JWT-based authentication
- Document access tokens
- SQL injection protection via SQLAlchemy
- CORS middleware enabled

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - Test update test buana