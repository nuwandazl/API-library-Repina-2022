import jwt 
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

class AuthHandler():
    security=HTTPBearer()
    pwd_context=CryptContext(
        schemes = ['bcrypt'],
        deprecated = 'auto'
    )
    secret='Я сплю'

# хеширование пароля
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
# проверка хэшированного пароля
    def verify_password(self, input_pass, hash_pass):
        return self.pwd_context.verify(input_pass, hash_pass)

# создание джвти токена
    def encode_token(self,username):
        payload={
            # увремя, когда токен станет просроченным
            'exp':datetime.utcnow()+timedelta(minutes=5),
            # время создания токен
            'iat':datetime.utcnow(),
            'sub':username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )
# токен это строка с тремя частями конкретно здесь, в программирование как ключ от дома
    def decode_token(self, token):
        try:
            payload=jwt.decode(
                token,
                self.secret,
                algorithms=['HS256']
            )
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(401,'Просрочено')
        except jwt.InvalidTokenError as e:
            raise HTTPException(401, 'Плохой токен')

    def auth_wrapper(self, auth:HTTPAuthorizationCredentials=Security(security)):
        return self.decode_token(auth.credentials)    