from src.model.user import User, UserType
from src.model.local import Local
from src.model.device import Device
from src.model.thing import Thing
from src.model.event import Event
from fastapi import Depends
from routes.router import fastapi_init, get_current_user, get_current_user_admin
from typing import Annotated

def get_entity_services():
    return {'user': User, 'local': Local, 'device': Device, 'thing': Thing, 'event': Event}

def launch(API, crud):
    app = fastapi_init(API, crud, get_entity_services())
    @app.get("/users/logged", tags=["User"], summary=f"Get logged user", description=f"Get logged user", response_description=f"Get logged user")
    async def get_logged_user(current_user: Annotated[User, Depends(get_current_user)]):
        return current_user
    return app