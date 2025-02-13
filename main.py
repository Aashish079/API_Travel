from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from llama_cpp import Llama
from typing import List
import json

app = FastAPI()

# Initialize Llama model
model = Llama(
    model_path="models/llama-2-7b-chat.gguf",  # Update this path to your model location
    n_ctx=2048,
    n_threads=4
)

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
                # Generate response from Llama model with streaming
                stream = model.create_chat_completion(
                    messages=[{"role": "user", "content": data}],
                    stream=True,
                    max_tokens=2048,
                    temperature=0.7
                )

                # Stream the response
                for chunk in stream:
                    if chunk and 'choices' in chunk and len(chunk['choices']) > 0:
                        content = chunk['choices'][0].get('delta', {}).get('content', '')
                        if content:
                            await manager.send_message(content, websocket)
                
                # Send a special token to indicate completion
                await manager.send_message("[DONE]", websocket)

            except Exception as e:
                await manager.send_message(f"Error: {str(e)}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Llama Chat API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)