import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from langchain_community.llms import Ollama
from typing import List, Dict
import json
import asyncio
from ConnectionManager import ConnectionManager
from RAGAgent import RAGAgent
from recommendation import recommend_monuments
from typing import Optional

app = FastAPI()

# Initialize components
try:
    model = Ollama(
    model="Aashish54/travelComp:latest",
)
    rag_agent = RAGAgent()
    manager = ConnectionManager()
    # Store WebSocket connections and their chat histories
    websocket_histories: Dict[WebSocket, List[str]] = {}
      
except Exception as e:
    print(f"Error initializing components: {str(e)}")
    raise

async def stream_tokens(prompt: str, websocket: WebSocket):
    try:
        # Get RAG-enhanced prompt
        enhanced_prompt = rag_agent.get_rag_prompt(prompt)
        response_chunks = []
        
        if websocket.client_state.CONNECTED:
            for chunk in model.stream(enhanced_prompt):
                if chunk and websocket.client_state.CONNECTED:
                    response_chunks.append(chunk)
                    await manager.send_message(chunk, websocket)
                    await asyncio.sleep(0.01)
            
            if websocket.client_state.CONNECTED:
                # Combine chunks and add to history
                full_response = "".join(response_chunks)
                rag_agent.add_to_history(prompt, full_response)
                await manager.send_message("[DONE]", websocket)
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        if websocket.client_state.CONNECTED:
            try:
                await manager.send_message(f"Error: {str(e)}", websocket)
            except:
                pass

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await stream_tokens(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # Clear history when connection closes
        rag_agent.clear_history()
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        if websocket.client_state.CONNECTED:
            manager.disconnect(websocket)
            rag_agent.clear_history()


@app.post("/clear-history")
async def clear_chat_history():
    """Endpoint to clear chat history"""
    try:
        rag_agent.clear_history()
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Ollama Chat API"}

@app.get("/say_hello")
async def read_item():
    return {"message": "Hello World"}

@app.post("/getRecommendations")
async def get_recommendations(prompt: Optional[str] = None):
    return recommend_monuments()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)