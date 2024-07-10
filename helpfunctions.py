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


def write_json(filename, data):
    '''
        write json
    '''
    try:
        with open(filename,'w') as f:
            print("writing, ",filename)
            json.dump(data, f, indent=4)

    except json.JSONDecodeError:
        print("Error writing ",filename)

write_json('results.json',results)
