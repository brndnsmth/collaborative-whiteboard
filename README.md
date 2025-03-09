# Collaborative Whiteboard App

A fairly basic real-time collaborative whiteboard application. Users can draw, annotate, and chat with each other in real time. Each user is assigned a random goofy name upon joining, and all changes to the canvas are synchronized across all connected users.

---

## Features

### Core Features
- **Real-time Drawing Synchronization**: All users see updates to the canvas in real time.
- **Multiple Users Editing the Same Canvas**: Users can collaborate on the same canvas simultaneously.
- **Drawing Tools**:
  - Pen for freehand drawing
  - Line, Rectangle, and Circle tools for shapes
  - Eraser to remove parts of the drawing
  - Color picker to choose drawing colors
  - Adjustable brush size
  - Clear canvas button to reset the canvas
- **Chat Functionality**: Users can send messages to each other in real time.

---

## Technologies Used

### Backend
- **FastAPI**: For handling WebSocket connections and managing the server.
- **WebSockets**: For real-time communication between the server and clients.

### Frontend
- **HTML5 Canvas**: For drawing and rendering the whiteboard.
- **JavaScript**: For handling user interactions, drawing logic, and WebSocket communication.

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher

### Steps to Run the App

1. **Clone the Repository**
   ```bash
   git clone https://github.com/brndnsmth/collaborative-whiteboard.git
   cd collaborative-whiteboard
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Server**
   Start the FastAPI server:
   ```bash
   python main.py
   ```

5. **Access the App**
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

---

## How It Works

1. **User Connection**:
   - When a user connects, they are assigned a random goofy name (e.g., "BouncyPenguin").
   - The server sends the current canvas state and the list of online users to the new user.

2. **Real-Time Drawing**:
   - Users draw on the canvas using tools like Pen, Line, Rectangle, Circle, and Eraser.
   - Drawing actions are sent to the server via WebSockets and broadcast to all connected users.

3. **Canvas State Management**:
   - The server maintains a shared canvas state.
   - When a new user joins, they receive the current canvas state to ensure consistency.

4. **Chat**:
   - Users can send messages to each other in real time.
   - Messages are displayed in the chat panel with the sender's name.

---

## Usage Instructions

### Drawing Tools
- **Pen**: Freehand drawing.
- **Line**: Draw straight lines. Click and drag to define the start and end points.
- **Rectangle**: Draw rectangles. Click and drag to define the top-left and bottom-right corners.
- **Circle**: Draw circles or ellipses. Click and drag to define the bounding box.
- **Eraser**: Erase parts of the drawing.
- **Color Picker**: Choose a color for drawing.
- **Size Slider**: Adjust the size of the brush or shape outline.
- **Clear Canvas**: Reset the canvas for all users.

### Chat
- Type a message in the chat input box and press "Send" to communicate with other users.

---

## Known Issues and Limitations

- **Performance**: For very large numbers of users or complex drawings, performance may degrade. Optimizations like throttling WebSocket messages can help.
- **Persistence**: The canvas state is not saved permanently. If the server restarts, the canvas is cleared.

---

## Future Improvements

- **Save and Load Canvas**: Add functionality to save the canvas as an image or JSON file and reload it later.
- **Authentication**: Allow users to log in with custom usernames.
- **Undo/Redo**: Add undo and redo functionality for drawing actions.
- **Mobile Optimization**: Further improve touch support and responsiveness for mobile devices.
- **Add Images**: Add images to the canvas.