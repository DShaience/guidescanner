from pathlib import Path
import json
import argparse

def parse_json_to_text(input_dir: Path, output_dir: Path, encoding: str = 'utf-8-sig'):
    # Ensure the input directory exists
    if not input_dir.is_dir():
        raise ValueError(f"The directory {input_dir} does not exist.")
    
    # Ensure the output directory exists or create it
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Iterate over each JSON file in the input directory
    for json_file in input_dir.glob('*.json'):
        text_file = output_dir / json_file.with_suffix('.txt').name
        
        # Read the JSON file
        with open(json_file, 'r', encoding=encoding) as file:
            data = json.load(file)
        
        # Extract title and paragraphs
        title = data.get('title', '')
        paragraphs = data.get('paragraphs', [])
        
        # Clean paragraphs
        cleaned_paragraphs = [para.strip() for para in paragraphs if para.strip()]
        combined_paragraphs = '\n'.join(cleaned_paragraphs)
        
        # Write to the text file
        with open(text_file, 'w', encoding=encoding) as file:
            file.write(f"Title: {title}\n\n{combined_paragraphs}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse JSON files to text files.")
    parser.add_argument('--input_dir', type=Path, default="/workspaces/guidescanner/src/output/ign", help="Directory containing JSON files.")
    parser.add_argument('--output_dir', type=Path, default="/workspaces/guidescanner/dev/full_bg3/input", help="Directory to save the output text files.")
    args = parser.parse_args()
    
    parse_json_to_text(args.input_dir, args.output_dir)






