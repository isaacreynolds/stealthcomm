# StealthComm

**StealthComm** is a peer-to-peer (P2P) secure messaging application designed for privacy enthusiasts who value encrypted communication. Leveraging AES encryption (via the `cryptography` library) and a central server registry for managing active chat servers, StealthComm ensures secure, lightweight, and efficient communication.

## Features

- **End-to-End Encryption:** Messages are encrypted using SHA256 (Fernet cipher) for confidentiality.
- **Central Server Registry:** A  system to register and retrieve active chat servers.
- **Peer-to-Peer Communication:** Clients connect directly to chat servers for real-time communication.
- **User-Friendly Interface:** Simple GUI built using Tkinter for ease of use.
- **Cross-Platform Compatibility:** Runs on Windows, macOS, and Linux.

## Architecture

StealthComm consists of three main components:

1. **Central Registry Server:** Maintains a list of active chat servers and provides server information to clients.
2. **Chat Server:** Handles client connections, message broadcasting, and encryption.
3. **Chat Client:** Connects to the chat server for secure messaging.

## Installation

### Prerequisites

- [Python 3.x](https://www.python.org/) installed
- Required Python packages listed in `requirements.txt`

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/isaacreynolds/StealthComm.git
   cd StealthComm
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the central registry server (in a terminal):

   ```bash
   python stealthcomm_central_registry.py
   ```

5. Start a chat server (in another terminal):

   ```bash
   python stealthcomm_chat_server.py
   ```

6. Launch the chat client (in a separate terminal):

   ```bash
   python stealthcomm_chat_client.py
   ```

## Usage

### Client Mode

1. Run the client application.
2. Connect to an available chat server from the central registry.
3. Begin secure communication.

### Server Mode

1. Run the server application.
2. Accept client connections and monitor chat activity via the GUI.
3. Broadcast messages and manage client connections.

## Technical Details

- **Encryption:** Messages are encrypted using the AES-based Fernet cipher for secure communication.
- **Central Registry:** Manages active server registrations and provides server details to clients.
- **GUI:** Built using Tkinter for both server and client applications.

## Security Considerations

- Ensure that the `secret.key` file used for encryption is securely stored and not shared.
- Regularly rotate encryption keys for enhanced security.
- Use secure network configurations to protect against unauthorized access.

## Contributing

We eagerly welcome contributions from the community! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature:

   ```bash
   git checkout -b feature-name
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add new feature"
   ```

4. Push your branch:

   ```bash
   git push origin feature-name
   ```

5. Open a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [cryptography](https://cryptography.io/) library for encryption utilities.
- Community contributors for code improvements and feature suggestions.

## Contact

For issues, suggestions, or feedback, please open an issue on the [GitHub Issues](https://github.com/username/StealthComm/issues) page.

---

Enjoy secure and private communication with **StealthComm**!

