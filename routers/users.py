from fastapi import APIRouter, HTTPException, status, Depends
from database.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, UserResponse, TokenResponse
from auth.hash_password import hash_password

user_router = APIRouter(
    tags=['User']
)


@user_router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def sign_new_user(data: User, session: AsyncSession = Depends(get_session)):
    statement = select(User).where(User.email == data.email)
    result = await session.execute(statement)
    user = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with email "{}" already exist.'.format(data.email)
        )
    hashed_password = hash_password.create_hash(data.password)
    data.password = hashed_password
    session.add(data)
    await session.commit()
    await session.refresh(data)

    return data


@user_router.post('/signin', response_model=TokenResponse)
async def sign_user_in(user_in: OAuth2PasswordRequestForm = Depends(),
                       session: AsyncSession = Depends(get_session)):
    statement = select(User).where(User.email == user_in.username)
    result = await session.execute(statement)
    user = result.scalars().first()

    if user and hash_password.verify_hash(user_in.password, user.password):
        access_token = create_access_token(
            user.email
        )
        return {
            'access_token': access_token,
            'token_type': 'Bearer'
        }

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='auth fail'
    )
