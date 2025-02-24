import json

def remove_id_field(data):
    """
    Recursively remove the "id" key from dictionaries.
    """
    if isinstance(data, dict):
        # Remove the key if it exists
        data.pop("id", None)
        # Recursively process the dictionary values
        for key, value in data.items():
            data[key] = remove_id_field(value)
    elif isinstance(data, list):
        # Process each item in the list
        data = [remove_id_field(item) for item in data]
    return data

def main():
    input_file = 'data.json'    # Path to your input JSON file
    output_file = 'cleaned_data.json'  # Path for the output JSON file

    # Open and load the JSON data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remove the "id" key from the data
    cleaned_data = remove_id_field(data)

    # Write the cleaned data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
