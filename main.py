import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from DB import USER_DATA
from models import User

app = FastAPI(title="Authentication")
security = HTTPBasic()

# симуляционный пример
def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

#  Пример из курса
@app.get("/protected_resource/")
def get_protected_resource(user: User = Depends(authenticate_user)):
    return {"message": "You have access to the protected resource!", "user_info": user}


#  Выполненное задание
@app.get('/login')
async def get_login(user: User = Depends(authenticate_user)):
    return "You got my secret, welcome"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
