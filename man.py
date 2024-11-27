from DiagramToMeta import DiagramToMeta
from MetaToSql import MetaToSql

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Process metadata and generate SQL or models.")
    parser.add_argument("-i", "--input", required=True, help="Input file containing JSON metadata.")
    parser.add_argument("-m", "--mode", required=True, choices=["mysql", "migrate", "model"], help="Mode of operation.")
    
    args = parser.parse_args()

    # Read the input file
    try:
        f = open(args.input, "r")
        diagram_text = f.read()
        diagram_to_meta = DiagramToMeta(diagram_text)
        result = diagram_to_meta.get_all()
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    # Handle the specified mode
    if args.mode == "mysql":
        converter = MetaToSql(result)
        converter.process_and_save("output.sql")
    elif args.mode == "migrate":
        print("Migrate mode is under development.")
    elif args.mode == "model":
        print("Model mode is under development.")
    else:
        print("Invalid mode selected.")

if __name__ == "__main__":
    main()