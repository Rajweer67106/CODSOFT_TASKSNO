# Task 5 – Chat Application

This project is part of my **OASIS INFOBYTE Python Programming Internship**.
I built a simple client-server chat application to understand how computers communicate over a network in real time. The project uses Python sockets and threads so that multiple clients can connect to one server and exchange messages.

## Features
- Client-server architecture
- TCP socket communication
- Multiple clients supported
- Simple username system
- Real-time message broadcasting
- Join and leave notifications
- Graphical client interface using Tkinter
- Background thread for receiving messages
- Graceful disconnect using `/quit`
- Basic connection and input error handling

## Technologies Used
- Python
- Socket programming
- TCP/IP
- Threading
- Tkinter

## Project Structure

```text
Python-L2-Task5-ChatApplication/
├── server.py
├── client.py
└── README.md
```

## How to Run
### 1. Start the Server

Open a terminal in this folder and run:

```bash
python server.py
```

The server will listen on port `5000`.

### 2. Start a Client

Open another terminal and run:

```bash
python client.py
```

Enter:
- Server: `127.0.0.1`
- Port: `5000`
- Username: any name you choose

Click **Connect**.

### 3. Connect Multiple Users

Open `client.py` in two or more terminals/windows. Give each client a different username and connect them to the same server. Messages sent by one client will be displayed to the other connected clients.

### Commands

Use:
```text
/quit
```

to leave the chat.

## Running on Another Computer

For computers on the same network, the server computer can be used as the server address instead of `127.0.0.1`. Make sure the server port is allowed through the firewall and that both computers are connected to the same network. This project helped me understand client-server architecture, TCP sockets, multi-client communication, threading, GUI programming, and handling network connections in Python.
