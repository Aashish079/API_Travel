# main.py
import os
from fastapi import Depends
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Monument as DBMonument
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Body
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from pydantic import BaseModel
from langchain_community.llms import Ollama
import json
import asyncio
from recommendation import recommend_monuments

class Monument(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    type: str
    popularity: float
    indoor: bool
    type: str
    description: str
    image_url: str
    location: str

    class Config:
        orm_mode = True



app = FastAPI()

assets_dir = Path("assets")
assets_dir.mkdir(exist_ok=True)

# Mount the static files directory
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Load the model
model = Ollama(model="Aashish54/travelComp")  

class RecommendationRequest(BaseModel):
    latitude: Optional[float] = 27.7104
    longitude: Optional[float] = 85.3487
    preferred_type: Optional[str] = "Hindu Temple" #Need to update here by fetching actual user preference from db

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

@app.get("/say_hello")
async def read_item():
    return {"message": "Hello World"}

@app.get("/getMonuments", response_model=List[Monument])
async def get_monuments(db: Session = Depends(get_db)):
    """
    Get a list of all monuments with their details including image URLs from the database.
    
    The images can be accessed directly via their URLs, for example:
    http://localhost:8000/assets/Pashupatinath_Temple.jpg
    """
    # Query monuments from database
    db_monuments = db.query(DBMonument).all()
    
    # Convert DB models to Pydantic models
    monuments = []
    for db_monument in db_monuments:
        # Check if image exists
        if db_monument.image_url:
            image_path = Path(db_monument.image_url.replace("/assets/", ""))
            full_path = assets_dir / image_path
            if not full_path.exists():
                print(f"Warning: Image {db_monument.image_url} not found at {full_path}")
        
        # Get events as a list - adjust this based on your database schema
        events = []
        if hasattr(db_monument, 'monument_events'):  # Assuming a relationship
            events = [event.name for event in db_monument.monument_events]
        
        # Convert to Pydantic model format
        monument = Monument(
            id=db_monument.monument_id,  # Adjust field name if different
            name=db_monument.name,
            latitude=db_monument.latitude,
            longitude=db_monument.longitude,
            popularity=db_monument.popularity,
            indoor=db_monument.indoor,
            type=db_monument.type,
            description=db_monument.description,
            image_url=db_monument.image_url,
            location = db_monument.location
        )
        monuments.append(monument)
    
    return monuments

# @app.post("/recognizeMonument")
# async def get_Monument(request: Optionl[Image] ):
#     """
#     Returns Recognized Monuments based on photo and location from the frontend


#      """



@app.post("/getRecommendations")
async def get_recommendations(request: Optional[RecommendationRequest] = Body(None)):
    """
    Get recommended monuments based on user preferences.
    
    Parameters:
    - latitude: User's current latitude (optional, default: 27.7104)
    - longitude: User's current longitude (optional, default: 85.3487)
    - preferred_type: Type of monument the user prefers (optional, default: "Hindu Temple")
    
    Returns:
    - A sorted list of monument objects based on recommendation score
    """
    if request is None:
        request = RecommendationRequest()
        
    return recommend_monuments(
        user_lat=request.latitude,
        user_long=request.longitude,
        preferred_type=request.preferred_type
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)