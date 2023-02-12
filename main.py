from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.connection import init_db
from routers.users import user_router
from routers.events import event_router
import uvicorn

app = FastAPI()
app.include_router(user_router, prefix='/users')
app.include_router(event_router, prefix='/events')


@app.on_event('startup')
async def on_startup():
    await init_db()


@app.get('/')
async def home():
    return RedirectResponse(url='/events/')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
