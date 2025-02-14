import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain_community.llms import Ollama
from typing import List
import json

app = FastAPI()

# Initialize Ollama model (change "simp2:latest" to your desired model)
model = Ollama(model="llama3.1:latest")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
   
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Invoke the Ollama model (returns the complete response)
                response = model.invoke(data)
                await manager.send_message(response, websocket)
                await manager.send_message("[DONE]", websocket)
            except Exception as e:
                await manager.send_message(f"Error: {str(e)}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Ollama Chat API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)