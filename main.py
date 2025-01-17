from meta.DiagramToMeta import DiagramToMeta
from meta.MetaToSql     import MetaToSql
from meta.MetaToModel   import MetaToModel
from meta.MetaToRes     import MetaToRes
from meta.MetaToController     import MetaToController
from meta.MetaToRoute   import MetaToRoute
from meta.MetaToMigrate import MetaToMigrate

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Process metadata and generate SQL or models.")
    parser.add_argument("-i", "--input", required=True, help="Input file containing JSON metadata.")
    parser.add_argument("-m", "--mode",  required=True, choices=["all", "mysql", "sql", "migrate", "model", "res", "controller", "route", "migrate"], help="Mode of operation.")
    parser.add_argument("-e", "--exc",   nargs="*",     default=[], help="List of columns to exception (optional).")
    parser.add_argument("-d", "--dir",   nargs="*",     help="Directory (optional).")
    
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
    #-------------------------------------------------
    if args.mode == "all":
        converter = MetaToSql(result)
        converter.process_and_save("output.sql")

        converter = MetaToModel(result, exc=args.exc)
        converter.process_and_save()

        converter = MetaToRes(result, exc=args.exc)
        converter.process_and_save()

        converter = MetaToController(result, exc=args.exc, dir=args.dir)
        converter.process_and_save()

        converter = MetaToRoute(result, exc=args.exc, dir=args.dir)
        converter.process_and_save()

        converter = MetaToMigrate(result, exc=args.exc)
        converter.process_and_save()

    #-------------------------------------------------
    elif args.mode == "mysql" or args.mode == "sql":
        converter = MetaToSql(result)
        converter.process_and_save("output.sql")
    elif args.mode == "migrate":
        print("Migrate mode is under development.")
    elif args.mode == "model":
        converter = MetaToModel(result, exc=args.exc)
        converter.process_and_save()
    elif args.mode == "res":
        converter = MetaToRes(result, exc=args.exc)
        converter.process_and_save()
    elif args.mode == "controller":
        converter = MetaToController(result, exc=args.exc, dir=args.dir)
        converter.process_and_save()
    elif args.mode == "route":
        converter = MetaToRoute(result, exc=args.exc, dir=args.dir)
        converter.process_and_save()
    elif args.mode == "migrate":
        converter = MetaToMigrate(result, exc=args.exc)
        converter.process_and_save()
    else:
        print("Invalid mode selected.")
    #-------------------------------------------------


print('+=======================================================+')
print('|                      ArindyProject                    |')
print('|                 dbdiagram.io TO Laravel               |')
print('|-------------------------------------------------------|')
print('| -i / --input : Input file from dbdiagram .txt.        |')
print('| -m / --mode  : Mode of operation.                     |')
print('|     Modes:                                            |')
print('|       mysql/sql  -> Generate SQL file                 |')
print('|       migrate    -> Generate Laravel migration        |')
print('|       controller -> Generate Laravel controller       |')
print('|       route      -> Generate Laravel route            |')
print('|       model      -> Generate Laravel Model            |')
print('|       res        -> Generate Laravel Resources        |')
print('|       all        -> Generate ALL Modes                |')
print('| -e / --exc   : To exclude columns from generation.    |')
print('|              : To Models, Resources                   |')
print('+=======================================================+')



if __name__ == "__main__":
    main()