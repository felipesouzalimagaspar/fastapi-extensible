from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from src.model.entity import Entity
from src.database.crud import CRUD
from typing import List, Type, Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends, status
from src.model.user import User, UserType
from src.model.local import Local
from src.database.crud import CRUD
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth.oauth2 import authenticate_user, create_access_token
from jose import JWTError, jwt
from config.bootstrap import API, DATABASES
crud = CRUD(DATABASES['master'])
from fastapi.requests import Request
import logging, os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorization")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, API['oauth2']['secret_key'], API['oauth2']['algorithm'])
        userid: str = payload.get("user")
        if userid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get(User, userid)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_admin(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.type == UserType.ADMIN:
         return current_user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
def fastapi_init(API, crud, CLASSES) -> FastAPI:
    META_TAGS = get_meta_tags(CLASSES)
    app = fastapi_meta(API, META_TAGS)
    for _, entity_class in CLASSES.items():
        entity_router = get_crud_router(entity_class, crud)
        app.include_router(entity_router, prefix=f"/{entity_class.__name__.lower()}")

    # Middleware de log
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        request_logger = logging.getLogger('request_logger')
        request_logger.info(f"Receiving HTTP Request: {request.method} {request.url}")
        response = await call_next(request)
        return response


    @app.post("/authorization", include_in_schema=False)
    async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        user = authenticate_user(crud, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"access_token": create_access_token(
            data={"user": user.id}, API=API
        ), "token_type": "bearer"}
    return app

def get_meta_tags(CLASSES) -> List:
    list = [] 
    for key,value in CLASSES.items():
        list.append({"name":key})
    return list

def fastapi_meta(API, META_TAGS):
    app = FastAPI(
        title=API['name'],
        description=API['description'],
        version=API['version'],
        docs_url=API['docs'],
        tags_metadata = META_TAGS,
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        }
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if API['forceHTTPS']:
        app.add_middleware(HTTPSRedirectMiddleware)
    return app

def get_crud_router(entity_class: Type[Entity], crud: CRUD) -> APIRouter:
    router = APIRouter()
    clazz = entity_class.__name__
    @router.post("/", response_model=entity_class, summary=f"Create a new {clazz}", description=f"Create a new {clazz}", response_description=f"New {clazz}", status_code=201, tags=[f"{clazz}"])
    def create_entity(entity: entity_class, current_user: Annotated[User, Depends(get_current_user_admin)]):
        key = crud.insert(entity)
        entity.id = key
        return JSONResponse(content={"data": entity.dict()}, status_code=201)

    @router.get("/{id}", response_model=entity_class, summary=f"Read an {clazz}", description=f"Read an {clazz}", response_description=f"Finded {clazz}", tags=[f"{clazz}"])
    def read_entity(id: str, current_user: Annotated[User, Depends(get_current_user_admin)]):
        entity = crud.get(entity_class, id)
        if not entity:
            raise HTTPException(status_code=404, detail=f"{clazz} not found")
        return JSONResponse(content={"data": entity.dict()})

    @router.put("/{id}", response_model=entity_class, summary=f"Update an {clazz}", description=f"Update an {clazz}", response_description=f"Updated {clazz}", tags=[f"{clazz}"])
    def update_entity(id: str, entity: entity_class, current_user: Annotated[User, Depends(get_current_user_admin)]):
        entity.id = id
        if not crud.update(entity):
            raise HTTPException(status_code=404, detail=f"{clazz} not found")
        return JSONResponse(content={"data": entity.dict()})

    @router.delete("/{id}", summary=f"Delete an {clazz}", description=f"Delete an {clazz}", response_description=f"Deleted {clazz}", tags=[f"{clazz}"])
    def delete_entity(id: str, current_user: Annotated[User, Depends(get_current_user_admin)]):
        entity = crud.get(entity_class, id)
        if not entity:
            raise HTTPException(status_code=404, detail=f"{clazz} not found")
        crud.delete(entity)
        return JSONResponse(content={"data": {"detail": f"{clazz} deleted"}})

    @router.get("/", response_model=List[entity_class], summary=f"List {clazz}s", description=f"List {clazz}s", response_description=f"List of {clazz}s", tags=[f"{clazz}"])
    def list_entities(current_user: Annotated[User, Depends(get_current_user_admin)], page: int = 1, per_page: int = 10):
        entities = crud.list(entity_class, page=page, per_page=per_page)
        return JSONResponse(content={"data": [entity.dict() for entity in entities]})

    return router
