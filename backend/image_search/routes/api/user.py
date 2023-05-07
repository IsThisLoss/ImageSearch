import typing
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import models
from ... import auth
from ... import db
from ...db.users import User
from ...models.config import Settings, get_config

router = APIRouter(prefix='/api')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    database: db.Database = Depends(db.get_db),
    config: Settings = Depends(get_config),
) -> typing.Optional[User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    secret = config.secret
    username = auth.decode_username(token, secret)
    if not username:
        raise credentials_exception
    user = await database.users.find(username)
    if not user:
        raise credentials_exception
    return user


@router.post("/user/token", response_model=models.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    database: db.Database = Depends(db.get_db),
    config: Settings = Depends(get_config),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = form_data.username
    password = form_data.password

    hashed_password = await database.users.get_hashed_password(username)
    if not hashed_password:
        raise credentials_exception

    if not auth.verify_password(password, hashed_password):
        raise credentials_exception

    access_token_expires = timedelta(
        minutes=config.access_token_expire_minutes,
    )
    access_token = auth.create_access_token(
        data={"sub": username},
        secret=config.secret,
        expires_delta=access_token_expires
    )
    return models.Token(
        access_token=access_token,
        token_type='bearer'
    )


@router.get("/user/me")
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return {
        'username': current_user.username,
    }
