import re
from pathlib import Path

class LogCompiler:
    """
    Class for compiling raw keystroke logs into readable text
    Converts individual keystrokes into formatted text with proper line breaks and word wrapping
    """
    
    def __init__(self, config):
        self.config = config
        self.special_keys_map = {
            'enter': '\n',
            'space': ' ',
            'tab': '\t',
            'backspace': '[BACKSPACE]',
            'delete': '[DEL]',
            'esc': '[ESC]',
            'caps lock': '[CAPS]',
            'shift': '',
            'ctrl': '[CTRL]',
            'alt': '[ALT]',
            'windows': '[WIN]',
            'up': '[UP]',
            'down': '[DOWN]',
            'left': '[LEFT]',
            'right': '[RIGHT]',
            'page up': '[PGUP]',
            'page down': '[PGDN]',
            'home': '[HOME]',
            'end': '[END]',
            'insert': '[INS]',
        }
    
    def compile_log(self):
        """
        Main method to compile raw keystroke log into readable text
        """
        if not self.config.input_log_file:
            print("Error: Input log file not specified")
            return False
        
        input_path = Path(self.config.input_log_file)
        if not input_path.exists():
            print(f"Error: Input file '{self.config.input_log_file}' not found")
            return False
        
        try:
            # Read the raw log file
            with open(input_path, 'r', encoding='utf-8') as f:
                raw_lines = f.readlines()
            
            print(f"Processing {len(raw_lines)} keystrokes...")
            
            # Compile the keystrokes
            compiled_text = self._process_keystrokes(raw_lines)
            
            # Save compiled text
            if self.config.output_compiled_file:
                output_path = Path(self.config.output_compiled_file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(compiled_text)
                print(f"Compiled log saved to: {output_path}")
            else:
                print("\n" + "="*50)
                print("COMPILED TEXT:")
                print("="*50)
                print(compiled_text)
            
            return True
            
        except Exception as e:
            print(f"Error compiling log: {e}")
            return False
    
    def _process_keystrokes(self, raw_lines):
        """
        Process raw keystrokes and convert to readable text
        """
        compiled_text = ""
        current_line = ""
        
        for line in raw_lines:
            line = line.strip()
            if not line:
                continue
            
            # Extract the key name (handle different log formats)
            key_name = self._extract_key_name(line)
            
            # Process the key
            processed_key = self._process_single_key(key_name)
            
            # Handle backspace specially
            if processed_key == '[BACKSPACE]':
                if current_line:
                    current_line = current_line[:-1]
                continue
            
            # Add to current line
            current_line += processed_key
            
            # Check if we need to break the line
            if '\n' in current_line or len(current_line) >= 80:
                lines = current_line.split('\n', 1)
                compiled_text += lines[0] + '\n'
                current_line = lines[1] if len(lines) > 1 else ""
        
        # Add any remaining text
        if current_line:
            compiled_text += current_line
        
        return compiled_text
    
    def _extract_key_name(self, line):
        """
        Extract the key name from log line (handles different formats)
        """
        # Remove timestamps if present [2024-01-01 12:00:00] key
        timestamp_match = re.match(r'\[.*?\]\s*(.+)', line)
        if timestamp_match:
            return timestamp_match.group(1).strip().lower()
        
        # Remove any other prefixes and get the last word (the key)
        return line.strip().lower()
    
    def _process_single_key(self, key_name):
        """
        Process a single key name and return its text representation
        """
        # Check if it's a special key
        if key_name in self.special_keys_map:
            return self.special_keys_map[key_name]
        
        # Handle function keys
        if key_name.startswith('f') and key_name[1:].isdigit():
            return f'[F{key_name[1:]}]'
        
        # Handle number keys with modifiers (like shift+1 = !)
        number_symbols = {
            '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
            '6': '^', '7': '&', '8': '*', '9': '(', '0': ')'
        }
        
        # If it's a single character, return it as is
        if len(key_name) == 1:
            return key_name
        
        # For other keys, return in brackets
        return f'[{key_name.upper()}]'
    
    def get_statistics(self, raw_lines):
        """
        Generate statistics about the keystroke log
        """
        total_keys = len(raw_lines)
        special_keys = 0
        regular_keys = 0
        
        for line in raw_lines:
            key_name = self._extract_key_name(line.strip())
            if key_name in self.special_keys_map or len(key_name) > 1:
                special_keys += 1
            else:
                regular_keys += 1
        
        return {
            'total_keystrokes': total_keys,
            'regular_keys': regular_keys,
            'special_keys': special_keys,
            'average_line_length': total_keys / max(1, len(self._process_keystrokes(raw_lines).split('\n')))
        }