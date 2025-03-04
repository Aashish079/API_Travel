# main.py
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
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
    best_season: str
    best_time: str
    events: List[str]
    description: str
    image_url: str


monuments_data = [ {"id": 1, "name": "Pashupatinath Temple", "latitude": 27.7104, "longitude": 85.3487, "type": "Hindu Temple", "popularity": 0.95, "indoor": False, "best_season": "all", "best_time": "morning", "events": ["Maha Shivaratri", "Tihar Festival"], "description": "Ancient Hindu temple dedicated to Lord Shiva located on the banks of the Bagmati River.", "image_url": "/assets/Pashupatinath_Temple.jpg"}, {"id": 2, "name": "Boudhanath Stupa", "latitude": 27.7139, "longitude": 85.3600, "type": "Buddhist Stupa", "popularity": 0.92, "indoor": False, "best_season": "spring", "best_time": "morning", "events": ["Buddha Jayanti"], "description": "One of the largest spherical stupas in Nepal and the holiest Tibetan Buddhist temple outside Tibet.", "image_url": "/assets/Boudhanath_Stupa.jpg"}, {"id": 3, "name": "Swayambhunath Stupa", "latitude": 27.7149, "longitude": 85.2904, "type": "Buddhist Stupa", "popularity": 0.88, "indoor": False, "best_season": "all", "best_time": "morning", "events": ["Tihar Festival", "Buddha Jayanti"], "description": "Ancient religious architecture atop a hill in the Kathmandu Valley, nicknamed 'Monkey Temple'.", "image_url": "/assets/Swayambhunath_Stupa.jpg"}, {"id": 4, "name": "Durbar Square", "latitude": 27.7101, "longitude": 85.3000, "type": "Historical Monument", "popularity": 0.85, "indoor": False, "best_season": "autumn", "best_time": "afternoon", "events": ["New Year Celebration"], "description": "Popular plaza in front of the old royal palace featuring traditional Newari architecture.", "image_url": "/assets/Durbar_Square.jpg"}, {"id": 5, "name": "Patan Durbar Square", "latitude": 27.6710, "longitude": 85.3245, "type": "Historical Monument", "popularity": 0.9, "indoor": False, "best_season": "autumn", "best_time": "afternoon", "events": ["Holi Festival", "Bisket Jatra"], "description": "One of the three Durbar Squares in the Kathmandu Valley, located in the city of Lalitpur.", "image_url": "/assets/Patan_Durbar_Square.jpg"}, {"id": 6, "name": "Bhaktapur Durbar Square", "latitude": 27.6749, "longitude": 85.4290, "type": "Historical Monument", "popularity": 0.87, "indoor": False, "best_season": "spring", "best_time": "morning", "events": ["Bisket Jatra"], "description": "Former royal palace complex showcasing 15th-century Newari architecture and temples.", "image_url": "/assets/Bhaktapur_Durbar_Square.jpg"}, {"id": 7, "name": "Garden of Dreams", "latitude": 27.7170, "longitude": 85.2920, "type": "Garden", "popularity": 0.75, "indoor": False, "best_season": "all", "best_time": "afternoon", "events": ["Christmas Celebration"], "description": "Neo-classical historical garden featuring fountains, pavilions, and amphitheaters.", "image_url": "/assets/Garden_of_Dreams.jpg"}, {"id": 9, "name": "Kumari Ghar", "latitude": 27.7111, "longitude": 85.2964, "type": "Palace", "popularity": 0.79, "indoor": True, "best_season": "winter", "best_time": "morning", "events": ["Dashain Festival", "Tihar Festival"], "description": "A three-story brick building that is home to Nepal's living goddess, the Kumari.", "image_url": "/assets/Kumari_Ghar.jpg"}, {"id": 10, "name": "Rani Pokhari", "latitude": 27.7100, "longitude": 85.2930, "type": "Historical Site", "popularity": 0.7, "indoor": False, "best_season": "summer", "best_time": "afternoon", "events": ["Nepal Sambat New Year"], "description": "Historical artificial pond featuring a temple in the center, located near Durbar Square.", "image_url": "/assets/Rani_Pokhari.jpg"}, {"id": 11, "name": "Changu Narayan Temple", "latitude": 27.6749, "longitude": 85.4316, "type": "Hindu Temple", "popularity": 0.72, "indoor": False, "best_season": "all", "best_time": "morning", "events": ["Maha Shivaratri", "Tihar Festival"], "description": "Ancient Hindu temple from the 4th century dedicated to Lord Vishnu.", "image_url": "/assets/Changu_Narayan_Temple.jpg"}, {"id": 12, "name": "Lalitpur (Patan) Museum", "latitude": 27.6699, "longitude": 85.3250, "type": "Museum", "popularity": 0.77, "indoor": True, "best_season": "all", "best_time": "afternoon", "events": ["Art Exhibition"], "description": "Museum featuring collections of historical and ancient artworks from Nepal.", "image_url": "/assets/Lalitpur_Patan_Museum.jpg"}, {"id": 13, "name": "The National Museum", "latitude": 27.7041, "longitude": 85.2899, "type": "Museum", "popularity": 0.8, "indoor": True, "best_season": "all", "best_time": "morning", "events": ["National Holiday Celebration"], "description": "Nepal's largest museum, showcasing its history, art, and culture.", "image_url": "/assets/The_National_Museum.jpg"}, {"id": 14, "name": "Gosaikunda Temple", "latitude": 28.1970, "longitude": 85.4486, "type": "Hindu Temple", "popularity": 0.85, "indoor": False, "best_season": "winter", "best_time": "morning", "events": ["Janai Purnima Festival"], "description": "Hindu temple located at high altitude surrounding Gosaikunda lakes.", "image_url": "/assets/Gosaikunda_Temple.jpg"}, {"id": 15, "name": "Sundhara", "latitude": 27.7009, "longitude": 85.3033, "type": "Historical Site", "popularity": 0.68, "indoor": False, "best_season": "summer", "best_time": "afternoon", "events": ["Independence Day"], "description": "Medieval stone spout and important historical site in Kathmandu.", "image_url": "/assets/Sundhara.jpg"}, {"id": 16, "name": "Taleju Temple", "latitude": 27.7108, "longitude": 85.2980, "type": "Hindu Temple", "popularity": 0.9, "indoor": False, "best_season": "all", "best_time": "morning", "events": ["Dashain Festival", "Tihar Festival"], "description": "Important Hindu temple located in the old royal palace complex of Kathmandu.", "image_url": "/assets/Taleju_Temple.jpg"}, {"id": 17, "name": "Maha Laxmi Temple", "latitude": 27.7100, "longitude": 85.3005, "type": "Hindu Temple", "popularity": 0.88, "indoor": False, "best_season": "all", "best_time": "morning", "events": ["Tihar Festival"], "description": "Hindu temple dedicated to goddess of wealth and fortune Lakshmi.", "image_url": "/assets/Maha_Laxmi_Temple.jpg"}, {"id": 18, "name": "Narayanhiti Palace Museum", "latitude": 27.7124, "longitude": 85.3201, "type": "Museum", "popularity": 0.84, "indoor": True, "best_season": "spring", "best_time": "afternoon", "events": ["Republic Day"], "description": "Former royal palace converted into a museum showcasing artifacts from Nepal's monarchy.", "image_url": "/assets/Narayanhiti_Palace_Museum.jpg"}, {"id": 19, "name": "Bikram Sambat Park", "latitude": 27.7012, "longitude": 85.2873, "type": "Park", "popularity": 0.71, "indoor": False, "best_season": "spring", "best_time": "morning", "events": ["Bikram Sambat New Year"], "description": "Public park named after Nepal's Bikram Sambat calendar.", "image_url": "/assets/Bikram_Sambat_Park.jpg"}, {"id": 20, "name": "Chobhar Caves", "latitude": 27.6267, "longitude": 85.3250, "type": "Cave", "popularity": 0.65, "indoor": True, "best_season": "autumn", "best_time": "afternoon", "events": ["Autumn Festival"], "description": "Natural limestone caves located in the southern part of Kathmandu Valley.", "image_url": "/assets/Chobhar_Caves.jpg"} ]

app = FastAPI()

assets_dir = Path("assets")
assets_dir.mkdir(exist_ok=True)

# Mount the static files directory
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Load the model
model = Ollama(model="anoob/simp2:latest")  

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
async def get_monuments():
    """
    Get a list of all monuments with their details including image URLs.
    
    The images can be accessed directly via their URLs, for example:
    http://localhost:8000/assets/Pashupatinath_Temple.jpg
    """
    # Verify that the image files exist in the assets directory
    for monument in monuments_data:
        image_path = Path(monument["image_url"].replace("/assets/", ""))
        full_path = assets_dir / image_path
        if not full_path.exists():
            print(f"Warning: Image {monument['image_url']} not found at {full_path}")
    
    return monuments_data

@app.post("/getRecommendations")
async def get_recommendations(prompt: Optional[str] = None):
    return recommend_monuments()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)