import json
import re

class DiagramToMeta:
    def __init__(self, text_input):
        """
        Inisialisasi DiagramToMeta dengan teks input diagram.
        :param text_input: String teks diagram tabel.
        """
        if not isinstance(text_input, str):
            raise ValueError("Input harus berupa string teks.")
        self.text_input = text_input

    @staticmethod
    def split_tabel_ref(text):
        """
        Memisahkan tabel dan referensi dari teks diagram.
        """
        lines = text.strip().splitlines()
        tables = []
        refs = []
        current_table = []

        for line in lines:
            if line:
                line = line.strip()
                if line.startswith("Table"):
                    if current_table:
                        cleaned_table = DiagramToMeta.clean_table("\n".join(current_table))
                        tables.append(cleaned_table)
                        current_table = []
                    current_table.append(line)
                elif line.startswith("Ref:"):
                    refs.append(line)
                elif current_table:
                    current_table.append(line)

        if current_table:
            cleaned_table = DiagramToMeta.clean_table("\n".join(current_table))
            tables.append(cleaned_table)

        return tables, refs

    @staticmethod
    def clean_table(table):
        """
        Membersihkan tabel dari komentar dan teks tambahan setelah '}'
        """
        cleaned_lines = []
        inside_table = False

        for line in table.splitlines():
            if line.startswith("Table"):
                inside_table = True
            if line.startswith("//") and inside_table:
                continue
            cleaned_lines.append(line)

        cleaned_table = "\n".join(cleaned_lines)
        cleaned_table = re.sub(r"}.*$", "}", cleaned_table)
        return cleaned_table

    @staticmethod
    def ck_is_null(ls):
        """
        Mengecek apakah atribut null didefinisikan.
        """
        if 'null' in ls:
            return True
        elif 'not null' in ls:
            return False
        else:
            return True

    @staticmethod
    def ck_is_primary(ls):
        """
        Mengecek apakah atribut primary key didefinisikan.
        """
        return 'pk' in ls

    @staticmethod
    def ck_is_increment(ls):
        """
        Mengecek apakah atribut auto increment didefinisikan.
        """
        return 'increment' in ls

    @staticmethod
    def ck_default(ls):
        """
        Mengecek dan mengekstrak nilai default.
        """
        for i in ls:
            parts = [part.strip() for part in i.split(':', 1)]
            if parts[0].lower() == 'default':
                if len(parts) > 1:
                    value = parts[1]
                    if value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    elif value.lower() in ['true', 'false']:
                        value = value.lower() == 'true'
                    elif value == 'null':
                        pass
                    elif '.' in value and value.replace('.', '', 1).isdigit():
                        value = float(value)
                    elif value.isdigit():
                        value = int(value)
                    return True, value
        return False, None

    @staticmethod
    def extract_table(table):
        """
        Mengekstrak metadata tabel dari teks diagram.
        """
        lines = [line for line in table.split('\n') if line.strip()]
        if not lines:
            return {}

        table_name = lines[0].split()[-1].replace('{', '')
        items_field = []

        for line in lines[1:-1]:
            items = [item for item in line.split() if item]
            tmp = {
                'name': items[0],
                'type': items[1],
                'null': len(items) < 3,
                'increment': False,
                'attributes': ''
            }

            if 'id_' in items[0] or '_id' in items[0]:
                tmp['attributes'] = 'UNSIGNED'

            match = re.search(r"\[(.*?)\]", line)
            if match:
                result = re.split(r",\s*", match.group(1))
                tmp['increment'] = DiagramToMeta.ck_is_increment(result)
                tmp['primary'] = DiagramToMeta.ck_is_primary(result)
                tmp['null'] = DiagramToMeta.ck_is_null(result)
                if tmp['primary']:
                    tmp['attributes'] = "UNSIGNED"
                    tmp['null'] = False

                d_sts, d_val = DiagramToMeta.ck_default(result)
                if d_sts:
                    tmp['default'] = d_val

            items_field.append(tmp)

        result = {
            'table': table_name,
            'items': items_field
        }

        return result

    def get_tabels(self):
        """
        Memproses teks diagram Tabel menjadi metadata JSON.
        """
        tables, refs = self.split_tabel_ref(self.text_input)
        metadata = [self.extract_table(table) for table in tables]
        return json.dumps(metadata, indent=4)