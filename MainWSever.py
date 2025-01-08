import socket
import threading
import json
import select


# Web Server Host/Port
HOST = ''
PORT = 8000

# Chat Server Host/Port
Chat_HOST = ''  
Chat_PORT = 8756
page = b'''<html>

<body>

<h1>Discordn't Application</h1>
<div id = "login_page">
     <input type="text" id = "username" placeholder="Enter your username">
<div id = "button_class">
    <button onclick="enter()">Login</button>
</div>
</div>

<div id = "chat_page">
    <input type="text" id = "messageInput" placeholder = "Enter your message">

<div id = "button_class">
    <button onclick="sendRequest()">Send</button>
    <button onclick="logout()">Logout</button>
</div>
</div> 

<div id="messages"></div> 

<script>
let interval = null;

function enter(){

    const loginPage = document.getElementById('login_page');
    const chatPage = document.getElementById('chat_page');

    loginPage.style.display = 'none';
    chatPage.style.display = 'block';
    
    // setting new messages after 1 second using getRequest.
   interval = setInterval(getRequest, 1000);


}


function logout(){

    if(interval != null){
        clearInterval(interval);
    }

    const xhr = new XMLHttpRequest();

    xhr.onload = () => {

        if(xhr.status === 200){
            const loginPage = document.getElementById('login_page');
            const chatPage = document.getElementById('chat_page');
           
            loginPage.style.display = 'block';
            chatPage.style.display = 'none';
        
            document.getElementById('messageInput').value = ''
            document.getElementById('messages').innerHTML = ''
            document.getElementById('username').value =''
        }
    };
    xhr.open('DELETE', '/api/logout', true);
    xhr.send();
     
}

function sendRequest(){
    // Getting input from user
    const message = document.getElementById('messageInput').value;
    const username = document.getElementById('username').value;

    // Create new XHR request
    const xhr = new XMLHttpRequest(); 

    xhr.onload = () => {
        if (xhr.status === 200){
            // clear the placeholder once message successfully send
            document.getElementById('messageInput').value = '';
            getRequest();
        }
    };

    // HTTP Post method - 
    xhr.open('POST','/api/messages', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Sending data in JSON format

    const data = JSON.stringify({username: username, message: message});
    xhr.send(data)
  
}


function getRequest() {
    const xhr = new XMLHttpRequest();

    xhr.onload = () => {
        if (xhr.status === 200) {
            const messages = JSON.parse(xhr.responseText);
            const messageID = document.getElementById('messages');
            messageID.innerHTML = ''; 

           
                for (let i = 0; i < messages.length; i++) {
                    const msg = messages[i];
                    messageID.innerHTML += `<div>${msg.username}: ${msg.body}</div>`;
                }
            } 
        
    };
    
    xhr.open('GET', '/api/messages', true);
    xhr.send();

}

</script>

<style>

h1{
    padding-top: 50px;
    padding-left: 40px;
}

#login_page{
   
    padding-top: 10px;
    padding-left: 40px;
}


#button_class{
    margin-top: 5px;
}

#chat_page{
    display:none;
    padding-top: 10px;
    padding-left: 40px;

}

button{
    font-size: 18px;
}


#username, #messageInput {
    padding: 10px;
    width: 40%;
    border-radius: 5px;
    font-size: 20px;

}

</style>

</body>
</html>
'''




header = """HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {}

"""
jsonHeader = """HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: {}

"""

errorHeader = """HTTP/1.1 401 Not Found
Content-Type: text/plain
Content-Length: {}
"""
# Send Error response
def send_error(conn):
    body = "401 Not Found"
    error = errorHeader.format(len(body))
    conn.sendall(error.encode('utf-8'))
    conn.sendall(body.encode('utf-8'))
    conn.close()


# Send HTML page response
def send_html(conn):
    replyHeader = header.format(len(page))
    conn.sendall(replyHeader.encode())
    conn.sendall(page)
    conn.close()

# Send JSON responses
def send_json(conn, content):
    response_header = jsonHeader.format(len(content))
    conn.sendall(response_header.encode('utf-8'))
    conn.sendall(content.encode('utf-8'))
    conn.close()

# Main HTTP request handler
def http_request(conn):
    recv_request = conn.recv(1024).decode('utf-8')

       # Parsing if both headers and body are present in the request
    if "\r\n\r\n" in recv_request:
        headers, body = recv_request.split("\r\n\r\n", 1)
    else:
        headers = recv_request
        body = " " 

    try:
        http_request = headers.split("\r\n")[0]
        method, path, _ = http_request.split(" ", 2)
    except Exception as e:
        print("Invalid request format")
        send_error(conn)
        conn.close()
        return

    print(f"Received {method} request for {path}")

    if path == '/' or not path:
        send_html(conn)
    elif method == 'POST' and path == '/api/messages':
        post_request(conn, body)
    elif method == 'GET' and path.startswith('/api/messages'):
        get_request(conn)
    elif method == 'DELETE' and path == '/api/logout':
        delete_request(conn)
    else:
        send_error(conn)
        conn.close()

# delete request:
def delete_request(conn):
    try:
        send_json(conn, json.dumps({"status": "Logged out"}))
    except Exception as e:
        print(f"Error in DELETE request: {e}")
        send_error(conn)



# POST request: send message to chat server
def post_request(conn, body):
    try:
        # Parse JSON from the request body
        data = json.loads(body)
        username = data.get("username")
        user_message = data.get("message")
    

        message = f"{username}: {user_message}"

        message_recv = send_message_chatServer(message)
        # Send the message to the chat server
        if message_recv:
            response_json = json.dumps(message_recv)
            send_json(conn, response_json)
            sendMessage_to_clients()
        else:
            send_json(conn, json.dumps({"status": "Failed to send message"}))

    except Exception as e:
        print(f"Error in POST request: {e}")
        send_error(conn)


#GET request: retrieve messages from chat server
def get_request(conn):
    try:
        # Retrieve all messages from the chat server
        messages = retrieve_messages_chatServer()
        # Format messages as JSON for the client
        if messages:
            messages_list = []
            for msg in messages.splitlines():
                # Split and check if the message has a valid username and body
                parts = msg.split(": ", 1)
                if len(parts) == 2:  
                    username, body = parts
                    messages_list.append({"username": username, "body": body})

           
            messages_json = json.dumps(messages_list)
            send_json(conn, messages_json)
           

        else:
            send_json(conn, json.dumps([])) 

    except Exception as e:
        print(f"Error in GET request: {e}")
        send_error(conn)




#Retrieve messages from chat server
def retrieve_messages_chatServer():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((Chat_HOST, Chat_PORT)) 
            messages = sock.recv(1024).decode('utf-8')
            return messages 
    except Exception as e:
        print(f"Error retrieving messages from chat server: {e}")
        return ""


# Send message to chat server
def send_message_chatServer(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((Chat_HOST, Chat_PORT))
            sock.sendall(message.encode('utf-8'))
            messages = sock.recv(1024).decode('utf-8')
            return messages 
    except Exception as e:
        print(f"Error sending message to chat server: {e}")
        return False


# List of all connections clients connected 
clients = []

def sendMessage_to_clients():
    for client in clients:
        try:
            message = retrieve_messages_chatServer()
            client.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to all client: {e}")
            clients.remove(client)


# Main server loop
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Listening on port {PORT}')
    while True:
        conn, addr = s.accept()
        # adding all connections in list
        clients.append(conn) 
        myThread = threading.Thread(target=http_request, args=(conn,))
        myThread.start()
 
