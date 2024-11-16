"""
This file will be used to create a subset of the data for testing purposes.
It takes the json files created by the WebScraper class and creates a subset of the data.
This is useful for testing but generally not relevant for production.
"""

import argparse
import json
import shutil
from pathlib import Path


def find_copy_jsons_with_phrase(input_dir, phrase, output_dir=None, encoding='utf-8-sig', case_insensitive=False):
    if case_insensitive:
        phrase = phrase.lower()

    matching_files = []
    
    for json_file in Path(input_dir).glob("*.json"):
        print(f"\rProcessing: {json_file.name.ljust(50)}", end='', flush=True)
        with open(json_file, 'r', encoding=encoding) as file:
            data = json.load(file)
            
            # Check if "title" field exists and contains the phrase
            title = data.get("title", "")
            if title:
                if case_insensitive:
                    title = title.lower()
                if phrase in title:
                    matching_files.append(json_file)
                    continue
            
            # Check if "paragraphs" field exists and contains the phrase
            paragraphs = data.get("paragraphs", [])
            if paragraphs:
                for paragraph in paragraphs:
                    if case_insensitive:
                        paragraph = paragraph.lower()
                    if phrase in paragraph:
                        matching_files.append(json_file)
                        break
    
    # If output_dir is specified, copy matching files to the output directory
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        for file in matching_files:
            shutil.copy2(file, output_dir)
    
    print("\nDone!")
    return matching_files



if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create a subset of the scraped data")
    parser.add_argument("--input_dir", type=str, default="/workspaces/guidescanner/src/output/ign", help="Directory containing the scraped data")
    parser.add_argument("--phrase", type=str, default=None, help="Phrase to search for in the JSON files")
    parser.add_argument("--output_dir", type=str, default="/workspaces/guidescanner/data/testing", help="Directory to save the subset")
    args = parser.parse_args()

    # take input dir from argparse
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    
    find_copy_jsons_with_phrase(input_dir, "Shadowheart", output_dir, case_insensitive=True)


