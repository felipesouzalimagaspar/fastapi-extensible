# FastAPI Extensible

Generic and extensible api using fastapi

## Get started

```
service redis-server start
redis-cli
> SELECT 0
>CONFIG SET dir /workspaces/fastapi-extensible/backup
>CONFIG SET dbfilename snapshot.rdb
>SHUTDOWN NOSAVE
service redis-server restart
uvicorn main:API --reload
```

Access http://localhost:8000/docs/swagger