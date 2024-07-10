def read_json(filename):
    '''
        read json
    '''
    try:
        with open(filename, 'r') as f:
            print("reading, ",filename)
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}
        print("Error reading ",filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    return data