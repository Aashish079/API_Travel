# main.py
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain_community.llms import Ollama
from typing import List
import json
import asyncio

app = FastAPI()

# Load the model
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

async def stream_tokens(prompt: str, websocket: WebSocket):
    try:
        # Use generate method with streaming
        for chunk in model.stream(prompt):
            if chunk:  # Check if chunk is not empty
                await manager.send_message(chunk, websocket)
                await asyncio.sleep(0.01)  # Small delay to prevent flooding
        # Send completion signal
        await manager.send_message("[DONE]", websocket)
    except Exception as e:
        await manager.send_message(f"Error: {str(e)}", websocket)

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await stream_tokens(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Ollama Chat API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)