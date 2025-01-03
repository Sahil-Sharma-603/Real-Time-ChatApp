# Website-Based Real-Time Chat Application

## **Features**
- **Real-Time Conversations**:
  - Group chat functionality allowing multiple users to communicate in real time.
  - Messages delivered instantly using WebSocket technology.

- **User Identification**:
  - Remember users on returning visits using cookies.
  - Retrieve chat history between users and group members for continuity.

---

## **Technical Features and Technologies Used**

### **Backend**
- **Python**:
  - Core programming language for the backend logic.
  - RESTFUL APIs -  implementing REST APIs.

- **Websockets**:
  - Enables real-time, two-way communication between clients and the server (TCP SOCKETS for reliablity, security, ordering).
  - Used for instant message delivery and updates (Completed by concept of polling).

### **Frontend**
- **Single Page Application (SPA)**:
  - Built using **AJAX (Asynchronous JavaScript and XML)** to provide a seamless user experience.
  - Avoids page reloads by dynamically fetching and updating content.

### **Session Management**
- **Cookies**:
  - Utilized to identify and remember returning users.
  - Stores minimal data for maintaining user sessions.

### **Data Synchronization**
- **Polling**:
  - Periodically checks the server for updates as a backup mechanism.
  - Ensures message delivery during WebSocket disruptions.

---

## **How It Works**

1. **User Authentication**:
   - Users are identified by cookies when visiting the application.
   - New users can set a username through a login interface.

2. **Real-Time Group Chat**:
   - WebSockets handle instant delivery of messages between users in the same chat room.

3. **Chat History**:
   - User messages are stored on the server.
   - When users rejoin the application, their previous chat history is retrieved.

4. **Fallback to Polling**:
   - If WebSocket communication is unavailable, polling ensures data synchronization by periodically requesting updates.

---

## **Advantages of the Approach**

- **Real-Time Communication**:
  - Provides instant updates for a smooth user experience.

- **Session Persistence**:
  - Cookies ensure users are remembered, maintaining personalization and continuity.

- **Dynamic and Responsive**:
  - SPA and AJAX ensure seamless navigation without full-page reloads.

- **Reliable Delivery**:
  - Polling acts as a fallback to ensure messages are synchronized even during network disruptions.

---

## **Technologies Used**
- **Backend**:
  - Python
  - RESTFUL APIs
  - WebSocket Protocol

- **Frontend**:
  - HTML5, CSS3, JavaScript (AJAX)

- **Session Management**:
  - Cookies

- **Database**:
  - Simple file to store chats

---

