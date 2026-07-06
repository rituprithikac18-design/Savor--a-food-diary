# API Documentation
## Base URL
/api/v1

---
# Authentication
## Register User
POST /auth/register
Creates a new user account.
### Request Body
```json
{
    "username":"ritu",
    "email":"ritu@gmail.com",
    "password":"123456"
}
```
### Success Response
```json
{
    "message":"User registered successfully"
}
```
---
## Login
POST /auth/login
### Request
```json
{
    "email":"ritu@gmail.com"
    "password":"123456"
}
```
### Success
```json
{
    "token":"JWT_TOKEN"
}
```

