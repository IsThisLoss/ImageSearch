import typing
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ... import auth
from ...models import config, user
from ...db import users

router = APIRouter(prefix='/api')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> typing.Optional[user.User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    secret = config.get_config().secret
    username = auth.decode_username(token, secret)
    if not username:
        raise credentials_exception
    user = await users.get_users().find(username)
    if not user:
        raise credentials_exception
    return user


@router.post("/user/token", response_model=user.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = form_data.username
    password = form_data.password

    hashed_password = await users.get_users().get_hashed_password(username)
    if not hashed_password:
        raise credentials_exception

    if not auth.verify_password(password, hashed_password):
        raise credentials_exception

    cfg = config.get_config()
    access_token_expires = timedelta(minutes=cfg.access_token_expire_minutes)
    access_token = auth.create_access_token(
        data={"sub": username},
        secret=cfg.secret,
        expires_delta=access_token_expires
    )
    return user.Token(
        access_token=access_token,
        token_type='bearer'
    )


@router.get("/user/me")
async def read_users_me(current_user: user.User = Depends(get_current_user)):
    return {
        'username': current_user.username,
    }
