from config.bootstrap import API, DATABASES
from routes import routes
from src.database.crud import CRUD
#from src.model.user import User, UserType
#from src.auth.oauth2 import get_password_hash

crud = CRUD(DATABASES['master'])
#crud.truncate(User)
#crud.insert(User(name="admin", mail="admin@fastapi", password=get_password_hash("secret"), type=UserType.ADMIN))
#crud.insert(User(name="guest", mail="guest@fastapi", password=get_password_hash("secret"), type=UserType.DEFAULT))
API = routes.launch(API, crud)