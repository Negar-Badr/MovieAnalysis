import json

def merge_json_files(input_files, output_file):
    merged_data = []  # List to store all merged data

    try:
        for file in input_files:
            with open(file, 'r') as infile:
                data = json.load(infile)
                if isinstance(data, list):
                    merged_data.extend(data)  # Append lists directly
                else:
                    print(f"Warning: File '{file}' does not contain a list. Skipping.")
        
        print(f"Total records after merging: {len(merged_data)}")

        # Save the merged data to the output file
        with open(output_file, 'w') as outfile:
            json.dump(merged_data, outfile, indent=4)
        print(f"Merged data saved to: {output_file}")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
    except json.JSONDecodeError as e:
        print(f"Error: File contains invalid JSON - {e.msg}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    input_files = [
        "11-08_to_11-14.json",  # Replace with your file names
        "11-01_to_11-07.json",
        "10-25_to_10-31.json",
        "10-17_to_10-24.json"
    ]
    output_file = "movie_articles.json"  # Replace with your desired output file name

    merge_json_files(input_files, output_file)
