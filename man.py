import json
import re

from DiagramToMeta import DiagramToMeta
from MetaToSql import MetaToSql

f = open("input.txt", "r")
diagram_text = f.read()

diagram_to_meta = DiagramToMeta(diagram_text)
result = diagram_to_meta.get_tabels()
print(result)

toSql = MetaToSql(result)
toSql.process_and_save()