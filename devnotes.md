<p></p>

# **<p style="text-align: center;">Developer Notes</p>**
## This file mainly contains little bits of information that might be helpful or maybe just random thoughts I had while working on this :\)
### you may not have any of these issues, but in case you do:
1. [Central Registry](#Central-Registry)
2. [Chat Server](#Chat-Server)
3. [Chat Client](#Chat-Client)
4. [Security](#Security)
5. [Tests/Debug](#Testing-and-Debugging)
6. [Future Features](#Future-Features)
7. [Random Thoughts/Notes](#Random-Thoughts/Notes)
###  **Central Registry**
   - **Server Details**: The registry server is hardcoded to start on port `5556` because it isn't a reserved port and is rarely used by other processes
   - **Troubleshooting**:  stupid problems that happen way too much (for sure need to work on resolving these)
     - #### Certificates
        - If you are having errors that sound something like `Err02: no such file or directory`, theres a chance your certificates may have either expired or been corrupted and may need regenerated and authenticated. See the [***README***](README.md) file for more details on regeneration and correct directory setup.
     - #### Firewall issues
       - I don't know too much about firewalls or how they work, but from what I read on SO, you may need to configure your machine to allow inputs on the ports the servers are running on. It's similar to port forwarding AFAIK
   - **Logs**: No user information is logged or stored, as long as the server you were active in is closed there is no log retained after closing
   - **Performance**: Added support for using multiple threads for intake, output, decryption, etc

###  **Chat Server**
   - **Handling Connections**: 
     - When the server has a new client, it takes that client's information and adds it to a `client = []` list of the currently connected users.
     - When the server loses connection with a client, it will display a message stating that an error with the client occurred and it will try 3 more times to reconnect with the missing client, and after three failed attempts stops and deletes user logs and information, as well as removing the client from the list.
  - **Security**: Information on the security protocols used (e.g., TLS 1.3) and any additional steps you’ve taken to ensure data protection.
   - **Scalability**: Personally, I run the registry on a RaspberryPi at home, but that has a heavy restriction on bandwidth and processing power. It might be a good idea to get an old laptop motherboard from a ThinkPad or something like that for additional power if needed
   - **Host Control Features**: currently, the functionality is there for the server host to have special permissions, like kicking (just a forceful closing of the connection to an **`ip`** address), announcements (functionally no different from a normal chat message, except for the username being **`Server`**), there is just not an effective implementation yet

###  **Chat Client**
   - **UI/UX Details**: I absolutely ABHOR using  tkinter, but it's all I could find. The GUI for this was originally just basic B&W, but right now I'm really liking the Matrix vibes it gives off, even if it is pretty rough aroudn the edges
   - **TLS and Authentication**:

      - **TLS Encryption**: Communication between the client and server is encrypted using **TLS 1.3** to protect data in transit. The server presents a certificate, which the client validates to ensure secure connections.
  
      - **Fernet Encryption**: Messages are encrypted using **Fernet** for end-to-end security. Both the client and server share a secret key, which is used to encrypt and decrypt messages
  
     - **Secret Key Authentication**: The client, server, and the registry must have the correct ``secret.key`` file to connect to the server. The server checks the key before allowing access. If the keys don’t match, the connection is rejected.

     - **Dynamic Server Discovery**: This simply re-calls the function to fetch the active server list from the registry again 
    
     - **Client Behavior**: When users perform any action that would be sent to the server, it is encrypted using AES-128 adn HMAC-SHA256 on their machine before being sent to the server for decryption (using that same key of course)

###  **Security**
   - **Encryption Details**: 

     - **AES-128-CBC**: Used for encrypting messages. It’s a symmetric encryption algorithm that ensures data confidentiality. It’s used with **HMAC-SHA256** to ensure integrity, so even if someone intercepts the message, they can’t modify or read it without detection.

     - **HMAC-SHA256**: Used to generate a hash of the message and is attached along with a secret key. This ensures the message hasn’t been tampered with, adding an extra layer of protection.

- **Authentication**: 

  - The server uses **X.509 certificates** for identity checking. The client verifies the server’s certificate against its own before connecting to ensure it’s communicating with the right (and real)  server.

  - The **`secret.key`** file is used to authenticate the client to the server, and the server to the registry. If the key doesn’t match, the connection is denied, preventing  access by attackers.

 - **Vulnerabilities/Exploits**: 

   - **Man-in-the-middle attacks (MITMs)**: If someone manages to intercept the communication, they could possibly modify messages. This is lessened/eliminated by using **TLS encryption** to ensure secure connections and verify the server’s identity.

   - **Weak Keys**: If the `secret.key` is weak or compromised, an attacker could gain unauthorized access. It’s crucial to generate and store keys securely and rotate/distribute them periodically.
     - Personally for the sake of security, I recommend generating the secret key on your machine, storing it on a memory device of some kind, and distributing it to users you wish to chat with **IN PERSON**.
       - I ***cannot*** stress this enough. If you are foolish enough to text someone your key, OPSEC really must not be your goal. 

###  **Testing and Debugging**
   - **Debugging Tips**: Currently, there is no way to easily debug this absolute mess of a program, but see [Future Features](#Future-Features) for more details
   - **Manual Testing**: 

     - **Server-Client Connection**: Test if the client can successfully connect to the server by ensuring the server is running and accessible on the correct port. Verify that the client can send and receive messages.

     - **Certificate Validation**: Ensure the client is verifying the server’s certificate properly. If the certificate is expired, invalid, or not trusted, the client should reject the connection.

     - **Encryption**: Check that messages sent between the client and server are properly encrypted and decrypted. Manually inspect the encrypted messages to confirm they can’t be read in transit.

     - **Client Authentication**: Test the `secret.key` authentication by attempting to connect with incorrect or missing keys. The connection should fail if the key is invalid.

      - **Error Handling**: Simulate server shutdowns, network disruptions, and invalid inputs to make sure the system handles errors gracefully without crashes.

###  **Future Features**
   - **Roadmap**:My current goal for this is to add in a user-triggerable debug mode, with print statements for all functions called in all programs to ease debugging for those editing this code for their own uses, but that is a long way off, especially with the current issues and bug fixes in this early stage of development. 
     - I'm also trying to work on the functionality and implementation of server/host permissions/powers.
   - **Known Improvements**: I would love to add support for multiple languages, as well as file sharing. Maybe I will add a (pretty much just a vastly simplified of the full build of StealthComm without server hosting functionalities) P2P program that people who just want a simple messenger service without all the extra weight. 

###  **Miscellaneous**
   - **Coding Standards**: Generally all declarations will follow the python standards, like this:
   ```python3
   def functionName(x):
        x + 5 = b
        return b
   variable = functionName(x)
   ```
   - **Contributions**: If you have any issues/ideas, please open a pull request and let me know, I want to keep improving this!

### Random Thoughts/Notes
- 2/2/25 - I am DEFINITELY shelving this for a while, this has been HORRIBLE to debug. Definitely working on adding a debug mode when I work up the courage to work on this again

- 2/2/25 - this would be so much easier having access to  multiple machines

- 2/2/25 - Yeah no I still hate using tkinter. I have to watch like 3 youtube videos and ask ChatGPT like every 5 seconds.

- 1/16/25 - I think this project is sick, but I am shelving this for now.

- 1/15/25 - I have got to learn some languages so I do not have to use someone elses GUI library, this is awful :\( 


