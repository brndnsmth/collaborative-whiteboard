from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import random
import uuid
from typing import Dict, List, Set

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Connection manager for WebSockets
class ConnectionManager:
    def __init__(self):
        # Active connections
        self.active_connections: Dict[str, WebSocket] = {}
        # Canvas state - store drawing data
        self.canvas_state: List[Dict] = []
        # User names
        self.user_names: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

        # Generate a random goofy name
        adjectives = [
            "Bouncy",
            "Wobbly",
            "Fluffy",
            "Sparkly",
            "Giggly",
            "Wiggly",
            "Bubbly",
            "Fuzzy",
            "Silly",
            "Zippy",
            "Loopy",
            "Squishy",
        ]
        nouns = [
            "Penguin",
            "Banana",
            "Noodle",
            "Pickle",
            "Unicorn",
            "Muffin",
            "Potato",
            "Panda",
            "Cupcake",
            "Doodle",
            "Waffle",
            "Marshmallow",
        ]

        user_name = f"{random.choice(adjectives)}{random.choice(nouns)}"
        self.user_names[client_id] = user_name

        # Send current canvas state and user list to new user
        await self.send_canvas_state(client_id)
        await self.broadcast_user_list()

        # Notify others that a new user joined
        join_message = {
            "type": "user_joined",
            "client_id": client_id,
            "user_name": user_name,
        }
        await self.broadcast(json.dumps(join_message), exclude=client_id)

    async def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.user_names:
            user_name = self.user_names[client_id]
            del self.user_names[client_id]

            # Notify others that a user left
            leave_message = {
                "type": "user_left",
                "client_id": client_id,
                "user_name": user_name,
            }
            await self.broadcast(json.dumps(leave_message))
            await self.broadcast_user_list()

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

    async def broadcast(self, message: str, exclude: str = None):
        for client_id, connection in self.active_connections.items():
            if exclude is None or client_id != exclude:
                await connection.send_text(message)

    async def send_canvas_state(self, client_id: str):
        if client_id in self.active_connections:
            state_message = {"type": "canvas_state", "data": self.canvas_state}
            await self.send_personal_message(json.dumps(state_message), client_id)

    async def broadcast_user_list(self):
        user_list = [{"id": cid, "name": name} for cid, name in self.user_names.items()]
        user_list_message = {"type": "user_list", "users": user_list}
        await self.broadcast(json.dumps(user_list_message))

    def add_to_canvas(self, data: Dict):
        self.canvas_state.append(data)

    def clear_canvas(self):
        self.canvas_state = []


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def get():
    with open("static/index.html", "r") as f:
        return f.read()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "draw":
                # Add drawing data to canvas state
                manager.add_to_canvas(message["data"])
                # Broadcast to all clients
                await manager.broadcast(data)

            elif message["type"] == "clear":
                # Clear the canvas
                manager.clear_canvas()
                # Broadcast clear command
                await manager.broadcast(data)

            elif message["type"] == "chat":
                # Add username to chat message
                message["user_name"] = manager.user_names.get(client_id, "Unknown")
                # Broadcast chat message
                await manager.broadcast(json.dumps(message))

    except WebSocketDisconnect:
        await manager.disconnect(client_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
