## Identity Service

### Responsibilities
- Register users
- Authenticate users
- Generate JWTs
- Verify JWTs

### Schemas
- UserCreate
- UserResponse
- LoginRequest
- Token

### Services
- hash_password()
- verify_password()
- create_access_token()
- verify_access_token()

### CRUD
- create_user()
- get_user_by_email()
- get_user_by_username()
- get_user_by_id()

### Endpoints
- POST /auth/register
- POST /auth/login
- GET /users/me
