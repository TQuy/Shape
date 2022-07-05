# Shape

## Content
- [Start the project](#how-to-setup-the-project)
- [Testing](#testing)
- [Commands](#commands)
## How to setup the project
1. Create python virtual environment, named `venv` for instance
```
python -m venv venv
```
2. Activate the virtual environment
```
source venv/bin/activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Migrate the database
```
python manage.py migrate
```
4. Start `Django` server
```
python manage.py runserver
```
## Commands
Run tests
```
python manage.py test
```
Format Python code style
```
python ./scripts/autopep8.py
```
## APIs
### Register user
send `post` request to `/auth/register` with payload as below
```
{
    "username": "quynt",
    "password": "1"
}
```
### Authenticate user
send `post` request to `/auth/login` with payload as below
```
{
    "username": "quynt",
    "password": "1"
}
```
### CRUD APIs related to shape object
All CRUD requests related to Shape object require jwt token.
```
Authorization: "Bearer {token}}"
```
See `manageshape/tests.py` to get some example.
### Create or Update
Send `post` requset to `localhost:8000/shapes/create` to create a shape with given name, or update it if existed.  
Payload example
```
    "name": "first_shape",
    "type": "diamond"
```
### List all shapes (belong to the authenticated user)
send `get` request to `localhost:8000/shapes`
### Read one shape (belong to the authenticated user)
send `get` requset to `localhost:8000/shapes/<id>` to get the info of the shape with `id` equal `<id>`
### Delete one shape
send `delete` requset to `localhost:8000/shapes/<id>` for instance to delete the shape with `id` equal `<id>`
### compute area
send `get` request to `localhost:8000/shapes/area` with params as
```
{
    type string,
    params string 
}
```
- for `triangle`, `params` can be `"3, 6, 7"` in which each number is the length of one edge.
- for `rectangle`, `params` can be `2 , 4` in which each number is the length of 2 edges connected to each other.
- for `square`, `params` can be `2`, the length of each edge.
- for `diamond`, `params` can be `4,6`, the length of two diagonals  

Example url: `/shapes/area?type=triangle&params=3,6,7`
### compute perimeter
send `get` request to `localhost:8000/shapes/perimeter`. The params is the same as `compute area`
- for `triangle`, `params` can be `"3, 6, 7"` in which each number is the length of one edge.
- for `rectangle`, `params` can be `2 , 4` in which each number is the length of 2 edges connected to each other.
- for `square`, `params` can be `2`, the length of each edge.
- for `diamond`, `params` can be `4`, the length of each edge.

Example url: `/shapes/perimeter?type=triangle&params=3,6,7`
