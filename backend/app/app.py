import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from core.proc import aiml

app = FastAPI()

kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

origins = ['http://127.0.0.1:5173']

answers = {
  "Блок 1, вопрос 1": ["Блок 1, ответ 1.1", "Блок 1, ответ 1.2", "Блок 1, ответ 1.3"], 
  "Блок 1, вопрос 2": ["Блок 1, ответ 2"], 
  "Блок 1, вопрос 3": ["Блок 1, ответ 3.1", "Блок 1, ответ 3.2"], 
  "Блок 2, вопрос 1": ["Блок 2, ответ 1"], 
  "Блок 2, вопрос 2": ["Блок 2, ответ 2.1", "Блок 2, ответ 2.2", "Блок 2, ответ 2.3", "Блок 2, ответ 2.4"], 
  "Блок 3, вопрос 1": ["Блок 3, ответ 1"], 
  "Блок 3, вопрос 2": ["Блок 3, ответ 2"], 
  "Блок 3, вопрос 3": ["Блок 3, ответ 3"], 
  "Блок 3, вопрос 4": ["Блок 3, ответ 4"], 
  
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
      data = await websocket.receive_text()
     # user_input = process_input(data)
     # ans = kernel.respond(user_input)
      for answer in answers[data]:
        await websocket.send_text(answer)

def start():
  """
  Launched with 'poetry run start' at root level
  """
  uvicorn.run(
    app='app.app:app', 
    host='localhost', 
    port=9191, 
    reload=True,
    workers=1,
  )