# Learning Log Project Requirements

## Project Overview

This project involves creating a Learning Log application using Django. The application will allow users to log their learning topics and entries. Users will be able to register, log in, and manage their own topics and entries. The project will be containerized using Docker and Docker Compose, and will include Gunicorn for serving the application.

## Functional Requirements

### User Authentication

- User registration
- User login
- User logout

### Topic Management

- Create new topics
- View list of topics
- View topic details

### Entry Management

- Add new entries to topics
- Edit existing entries
- View entries within a topic

### User Isolation

- Users can only view and manage their own topics and entries
- Users cannot access other users' topics and entries directly via URL

## Technical Requirements

### Django Setup

- Create a Django project named `learning_log`
- Create a Django app named `learning_logs`
- Configure `settings.py` with necessary settings
- Set up URLs for the project

### Models

- Create a `Topic` model with fields:
  - `text` (CharField)
  - `date_added` (DateTimeField)
  - `owner` (ForeignKey to User)
- Create an `Entry` model with fields:
  - `topic` (ForeignKey to Topic)
  - `text` (TextField)
  - `date_added` (DateTimeField)
- Ensure proper Meta classes for ordering

### Views

- Implement views for:
  - User registration
  - User login
  - User logout
  - Topic list
  - Topic detail
  - Entry creation
  - Entry edit

### URLs

- Set up URL patterns for:
  - Home page
  - Registration
  - Login
  - Logout
  - Topics
  - Topic detail
  - Entry creation
  - Entry edit

### Templates

- Create templates for:
  - Base template
  - Home page
  - Registration
  - Login
  - Topic list
  - Topic detail
  - Entry creation
  - Entry edit

### Forms

- Create forms for:
  - User registration
  - Topic creation
  - Entry creation
  - Entry edit

### Static Files

- Configure static files using WhiteNoise
- Ensure static files are collected and served correctly

### Environment Variables

- Use `.env` for:
  - `DJANGO_SECRET_KEY`
  - `DJANGO_DEBUG`
  - `DJANGO_ALLOWED_HOSTS`
  - `DJANGO_CSRF_TRUSTED_ORIGINS`
  - `SQLITE_PATH`
  - `APP_BIND_IP`
  - `APP_PORT`

### Docker

- Create a `Dockerfile` for the project
- Configure Docker to:
  - Install dependencies
  - Copy the application
  - Run migrations
  - Collect static files
  - Run Gunicorn

### Docker Compose

- Create a `compose.yaml` file to:
  - Build and run the application
  - Use a persistent volume for SQLite
  - Set up environment variables
  - Run migrations
  - Collect static files

### Git Security

- Ensure `.gitignore` includes:
  - `.env`
  - `db.sqlite3`
  - Virtual environment
  - Python cache
  - Local files

### README

- Create a `README.md` with:
  - Project description
  - Requirements
  - Local development instructions
  - Docker instructions
  - Database information
  - Environment variables
  - Static files information
  - Production instructions
  - Security information
  - Testing instructions

### Testing

- Create automated tests for:
  - User registration
  - User login
  - User logout
  - Topic creation
  - Entry creation
  - Entry edit
  - User isolation

### Final Verification

- Perform manual end-to-end testing
- Verify Docker setup
- Verify database persistence
- Verify production configuration
- Verify code quality
- Verify Django checks
- Verify migrations
- Verify all requirements in TASK.md are met

## Final Checklist

- [x] Django project and app created
- [x] Models implemented
- [x] Views implemented
- [x] URLs configured
- [x] Templates created
- [x] Forms implemented
- [x] User authentication working
- [x] User isolation enforced
- [x] Bootstrap integrated
- [x] Static files configured
- [x] Environment variables set up
- [x] Docker configured
- [x] Docker Compose configured
- [x] Git security configured
- [x] README created
- [x] Automated tests created
- [x] Manual testing completed
- [ ] Final verification completed (Docker runtime verification remains; Vercel and CI verified)

## Conclusion

This project will be completed by following the above requirements and ensuring all checks are passed. The final application will be a fully functional Learning Log with all specified features and security measures.
## Verification notes

21 tests pass locally and in GitHub Actions on Python 3.12. Production Vercel home, static files, admin login, registration and entry workflow verified over HTTP. Docker configuration is provided; Docker Engine was unavailable locally, so container runtime and SQLite volume recreation are not yet verified.
