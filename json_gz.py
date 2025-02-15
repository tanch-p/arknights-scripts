import json
import gzip
import sys
from pathlib import Path

def json_to_gz(input_file, output_file=None):
    """
    Convert a JSON file to a compressed GZ file with explicit UTF-8 handling.
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str, optional): Path to the output GZ file. If not provided,
                                   will use input filename with .gz extension
    
    Returns:
        str: Path to the created GZ file
    """
    try:
        # Convert input path to Path object
        input_path = Path(input_file)
        
        # If output file not specified, use input filename with .gz extension
        if not output_file:
            output_file = str(input_path.with_suffix('.gz'))
            
        # Read JSON file with explicit UTF-8 encoding
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Convert to JSON string with non-ASCII characters preserved
        json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        json_bytes = json_str.encode('utf-8')
        
        # Write to GZ file
        with gzip.open(output_file, 'wb') as f:
            f.write(json_bytes)
            
        return output_file
        
    except json.JSONDecodeError:
        print(f"Error: {input_file} is not a valid JSON file")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Encoding error: {str(e)}")
        print("Make sure your input file is properly UTF-8 encoded")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
