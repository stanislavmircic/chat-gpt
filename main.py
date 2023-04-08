from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import openai
#openai.api_key = 'enter-your-key'

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

chat_history = {}


class Item(BaseModel):
       name:str
       price: float
       is_offer: Union[bool,None] = None


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def read_item(id:str, q:str):
        if id not in chat_history:
            chat_history[id] = []
        message_to_send = []
        message_to_send.append({"role": "system", "content": "You are a Backyard Brains helpful chat assistant. If you don't know the answer say: I am sorry I don't know the answer to your question."});
        if(len(chat_history[id])>1):
            message_to_send.append({"role": "user", "content": chat_history[id][-2]["question"]});
            message_to_send.append({"role": "assistant", "content": chat_history[id][-2]["answer"]});
        if(len(chat_history[id])>0):
            message_to_send.append({"role": "user", "content": chat_history[id][-1]["question"]});
            message_to_send.append({"role": "assistant", "content": chat_history[id][-1]["answer"]});
        message_to_send.append({"role": "user", "content": q});
        print(message_to_send);
        #model="gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.0,
            messages=message_to_send
        )
        answer = response['choices'][0]['message']['content']
        chat_history[id].append({"question":q,"answer":answer})
        #print(chat_history[id])
        #status = response['choices'][0]['finish_reason']
        #print("Answer: "+answer)
        return {"question":q, "answer":answer}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}