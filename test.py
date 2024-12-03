from meta.DiagramToMeta import DiagramToMeta
from meta.MetaToSql import MetaToSql
from meta.MetaToModel import MetaToModel
from meta.MetaToRes import MetaToRes
import json

f = open('input.txt', "r")
diagram_text = f.read()
diagram_to_meta = DiagramToMeta(diagram_text)
result = diagram_to_meta.get_all()

mtm = MetaToRes(result)
mtm.process_and_save()

#print(json.dumps(result, indent=4) )