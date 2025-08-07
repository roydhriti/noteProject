import time
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.api import routes
from app.core.config import settings
from app.db.session import get_db


app = FastAPI(title="Note FAST API")

class CustomProxyHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get("x-forwarded-proto") == "https":
            request.scope["scheme"] = "https"
        return await call_next(request)

app.add_middleware(CustomProxyHeaderMiddleware)


SENSITIVE_KEYS = {"password", "token", "access_token", "refresh_token", "email"}

def redact_sensitive_data(data: str) -> str:
    try:
        parsed = dict(x.split("=") for x in data.split("&") if "=" in x)
        for key in parsed:
            if key.lower() in SENSITIVE_KEYS:
                parsed[key] = "****"
        return "&".join(f"{k}={v}" for k, v in parsed.items())
    except Exception:
        return "[REDACTED]"

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_time = time.time()
    body = await request.body()

    try:
        body.decode("utf-8")
        redact_sensitive_data(body.decode("utf-8"))
    except:
        pass

    response: Response = await call_next(request)
    return response


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.on_event("startup")
async def on_startup():
    try:
        db = next(get_db())
    except Exception:
        pass

app.include_router(routes)

@app.get("/")
def read_root():
    return {"app_name": settings.app_name}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="PMS FAST API",
        version="1.0.0",
        description="API documentation for PMS Application",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]

    try:
        user_update_schema = openapi_schema["components"]["schemas"]["UpdateUserSchema"]["properties"]
        if "email" in user_update_schema:
            user_update_schema["email"]["default"] = None
            user_update_schema["email"].pop("nullable", None)
    except KeyError:
        pass

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
