import itsdangerous
from core.config import conf
from core.cache_cli import redis_client
from passlib.context import CryptContext
from user.models import User

token_handler = itsdangerous.TimedJSONWebSignatureSerializer(conf.salt(), expires_in=3600)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_token(name, pk):
    res = token_handler.dumps({name: name, pk: pk})
    token = res.decode()
    await redis_client.set(f'{name}_{str(pk)}', token)
    return token


async def auth_token(pk, name, token):
    real_token = await redis_client.get(f'{name}_{str(pk)}')
    if real_token == token:
        return True
    else:
        return False


def gen_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await User.filter(user_name=username).first()
    if not user:
        return False
    if not verify_password(password, user.pass_word):
        return False
    return user
