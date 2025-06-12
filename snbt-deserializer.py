import json
import re

def parse_snbt(snbt_string):
    # Preserve newlines in description arrays
    snbt_string = re.sub(r'description: \[((?:[^[\]]|\[(?:[^[\]]|\[[^[\]]*\])*\])*)\]', 
                         lambda m: 'description: ' + json.dumps(m.group(1).strip().split('\n')), 
                         snbt_string, flags=re.DOTALL)
    
    # Handle empty arrays
    snbt_string = re.sub(r'\[ *\]', '[]', snbt_string)
    
    # Handle boolean values
    snbt_string = re.sub(r': *(true|false)', r': \1', snbt_string)
    
    # Handle numeric values
    snbt_string = re.sub(r': *(-?\d+\.?\d*[dDfF]?)', r': \1', snbt_string)
    
    # Handle string values
    def handle_string(match):
        value = match.group(1).replace('\n', '\\n')
        return f': "{value}"'
    snbt_string = re.sub(r': *([^{\[\d"\'][^,\n\]}]*)', handle_string, snbt_string)
    
    # Add quotes to keys
    snbt_string = re.sub(r'(\w+):', r'"\1":', snbt_string)
    
    # Parse the resulting JSON
    try:
        return json.loads('{' + snbt_string + '}')
    except json.JSONDecodeError as e:
        print(f"Error parsing SNBT: {e}")
        print(f"Problematic SNBT string: {snbt_string}")
        return None

def read_snbt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    file_path = input("Enter the path to your SNBT file: ")
    snbt_content = read_snbt_file(file_path)
    parsed_data = parse_snbt(snbt_content)
    
    if parsed_data:
        print(json.dumps(parsed_data, indent=2))
    else:
        print("Failed to parse SNBT file.")

if __name__ == "__main__":
    main()
