
# StealthComm (v2.1) - 2/2/2025

**StealthComm** is a secure, Matrix-inspired messaging system with end-to-end encryption and certificate-based authentication. Designed for privacy-conscious users, it combines TLS-secured connections with Fernet encryption for layered security.
**Secure Matrix-Style Chat System with Cross-Network Support**
## Currently working on:
- granting users use of a 'dev' or 'debug' mode in case of issues
- minor bug fixes, mainly on linux and OSX OSs
## New in v2.1
-  **LAN Communication**: Host/join servers across devices on the same network
-  **Repetitive Server Discovery**: Automatic server list updates, as well as a button to refresh them
-  **Network Security**: SSL-encrypted registry-server communication
-  **IP Configuration**: Specify registry server IP at client launch
-  **New Matrix-themed UI**: Changed colors, as well as font

## Key Features
- **Wireless/Wired Support**: Connect via WiFi or Ethernet cables
- **Central Registry**: Manage servers across the network
- **Firewall-Friendly**: Works behind most home/office firewalls
- **Certificate-Based Trust**: Prevent unauthorized servers

## Network Setup
1. **Registry Server**  
   Run on a machine visible to all users (static IP recommended, has issues connecting without.)
   ```bash
   python registry_server.py
## Features

- **Military-Grade Encryption**: 
  - Transport Layer: TLS 1.3 with ECDHE key exchange
  - Message Layer: Fernet (AES-128-CBC + HMAC-SHA256) 
- **Certificate Authentication**: X.509 certificates prevent MITM attacks
- **Matrix-Style UI**: Green-on-black terminal aesthetic with modern font
- **Server Browser**: Real-time server list with user counts and connection health
- **Secure File Transfer**: Encrypted plaintext file sharing capability
- **Temporary Sessions**: `//leavechat` command wipes session data
- **User Management**: Server-side kick ability for server hosts & moderators
## What's New in v2.0:
- 🔒 **TLS 1.3 Encryption**: All traffic now SSL-encrypted
- 🖥️ **Matrix-esqe UI**: Terminal-style chat interface
- 📊 **Live Server Metrics**: See active users before joining
- 🗝️ **Key-Based Access**: Servers require matching secret.key to be visible to users
- 🪲 **Minor bug fixes**: when joining servers with users with a different key, client & server would crash and oftentimes self delete from users machines.
## WARNINGS
All users of legacy code are recommended to upgrade as soon as possible, as previous versions were highly vulnerable to MITMs and had the possibility of code injection remotely
## Architecture
```.
├── registry/
│   ├── registry_server.py
│   ├── secret.key  # Generated once
│   ├── registry.crt
│   └── registry.key
├── server/
│   ├── chat_server.py
│   ├── secret.key  # Same as registry
│   ├── server.crt
│   ├── server.key
│   └── registry.crt
└── client/
    ├── client.py
    ├── secret.key  # Same as others
    ├── server.crt
    └── registry.crt
```
Three core components:

1. **Registry Server (Authority)**  
   - TLS-secured server directory  
   - Validates server/client keys  
   - Tracks active users per server  
   *Required/Default Port: 5556*

2. **Chat Server (Host)**  
   - TLS 1.3 + Fernet encrypted  
   - Broadcasts messages P2P-style  
   - User count reporting to registry  
   *Default Port: 5555*

3. **Matrix Client (End User)**  
   - Certificate-pinned connections  
   - Message history encryption  
   - Server health monitoring  
   *Port: Dynamic*

## Installation

### Prerequisites

- Python 3.10+
- OpenSSL 3.0+
- Required packages:
  ```bash
  cryptography >= 41.0.0
  pyOpenSSL >= 23.2.0
  requests >= 2.31.0
  ```

  ## Setup
  ### Install Pre-Reqs
  ```bash
   pip install -r requirements.txt
  ```
  1. **Clone Repository**
   ```git clone https://github.com/isaacreynolds/StealthComm.git```

  2. **Generate Certificates**
   
        Registry Certificate

        ```bash
        openssl req -x509 -newkey rsa:4096 -keyout registry.key -out registry.crt -days 365 -nodes
        ```
        Server Certificate
        ```bash
        openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
        ```
   3.Distribute files and run components:


### Start registry (terminal/machine 1)
```bash
cd registry && python registry_server.py

```

### Start chat server (terminal/machine 2)
```bash
cd server && python chat_server.py

```

### Launch client & connect to servers (terminal/machine 3)
```bash
cd client && python client.py
```

# Usage
Client flow:
1. Launch client - see server browser

2. Select server with updating user count

3. Enter username (not for registration, just a nickname in joined servers)

4. Chat

5. Type ```//leavechat``` to return to server list (or simply close out of the client to close and disconnect)

# Host Controls
| Commands | Description | 
|---|---|
| ```//kick <user>``` | Remove user from server |
| ```//users``` | List connected users with IPs |
| ```//broadcast``` | Send server-wide announcement | 

# Additional considerations
- Ensure the registry server that will be connected to is whitelisted
- all user  information including chat logs, user data, etc is wiped upon user leaving the server
- The security key will only allow connections or viewing of servers that share the same key as the client.
- If you want access to a server you must have the proper .key to do so
- **DO NOT SHARE KEY TO USER(S) YOU DO NOT TRUST WITH YOUR COMPUTER AND ANY INFORMATION IT CONTAINS**


# LICENSE 
This program is under an MIT free-use license. You are free to modify and edit it as you see fit.
