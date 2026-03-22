from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

connections = []

html = """
<!DOCTYPE html>
<html>
<head>
<title>Chatterbox Real-Time</title>

<style>
body {
    font-family: Arial;
    background: linear-gradient(to right,#4facfe,#00f2fe);
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}

.container {
    width:400px;
    background:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0 5px 20px rgba(0,0,0,0.3);
}

h2 { text-align:center; }

#chat {
    height:300px;
    overflow-y:auto;
    border:1px solid #ccc;
    padding:10px;
    border-radius:8px;
    background:#f9f9f9;
}

.input-area {
    display:flex;
    margin-top:10px;
}

#msg {
    flex:1;
    padding:8px;
    border-radius:5px;
    border:1px solid #ccc;
}

button {
    padding:8px 12px;
    margin-left:5px;
    background:#007bff;
    color:white;
    border:none;
    border-radius:5px;
    cursor:pointer;
}

button:hover { background:#0056b3; }

</style>
</head>
<body>

<div class="container">

<h2>💬 Real-Time Chat</h2>

<div id="chat"></div>

<div class="input-area">
<input id="msg" placeholder="Type message...">
<button onclick="sendMessage()">Send</button>
</div>

</div>

<script>

let username = prompt("Enter your name:");

const socket = new WebSocket("ws://localhost:8000/ws");

const chat = document.getElementById("chat");

// receive messages
socket.onmessage = (event) => {
    const div = document.createElement("div");
    div.innerHTML = event.data;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
};

// send message
function sendMessage(){

    let msg = document.getElementById("msg").value;

    if(msg === "") return;

    socket.send("<b>" + username + ":</b> " + msg);

    document.getElementById("msg").value = "";
}

</script>

</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connections.append(ws)

    try:
        while True:
            data = await ws.receive_text()

            for conn in connections:
                await conn.send_text(data)

    except WebSocketDisconnect:
        connections.remove(ws)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)