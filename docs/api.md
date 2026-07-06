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
    "email":"ritu@gmail.com",
    "password":"123456"
}
```
### Success
```json
{
    "token":"JWT_TOKEN"
}
```
# Users
---
## Get My Profile
GET /users/me
Returns logged in user's profile.

---
## Update Profile
PUT /users/me
Request
```json
{
    "bio":"Food Geek",
    "city":"Mumbai"
}
```
---
## Get User
GET /users/:id
Returns public profile.

# Restaurants
---
## Search Restaurants
GET /restaurants
Query Parameters
name
city 
cusine
/restaurants?city=Mumbai
---
## Restaurant Details
GET /restaurants/:id
#Reviews 
---
## Create Review
POST /reviews
Request
```json
{
    "restaurant_id":18,
    "rating":4.5,
    "title":"Amazing",
    "content":"Loved the pasta."
}
```
---
## Get Restaurant Reviews 
GET /restaurants/:id/reviews
---
## Update Review
PUT /reviews/:id
---
## Delete Review
DELETE /reviews/:id
