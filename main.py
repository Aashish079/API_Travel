# main.py
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain_community.llms import Ollama
from typing import List
import json
import asyncio
from ConnectionManger import ConnectionManager

app = FastAPI()

# Load the model
model = Ollama(model="llama3.1:latest")  

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
    return {"message": "Welcome to Travel Companion API"}



@app.post("/getRecommendations")
async def get_recommendations(currentPlace: str):
    try:
        # Use generate method with streaming
        recommendations = model.stream(currentPlace)
        # To do: Implement a better recommendation system
        return {"recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)