from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routers.users import user_router
from routers.events import event_router
import uvicorn

origins = ['*']

app = FastAPI()
app.include_router(user_router, prefix='/users')
app.include_router(event_router, prefix='/events')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)


@app.get('/')
async def home():
    return RedirectResponse(url='/events/')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
