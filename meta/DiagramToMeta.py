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

    def split_tabel_ref(self):
        """
        Memisahkan tabel dan referensi dari teks diagram.
        """
        lines = self.text_input.strip().splitlines()
        tables = []
        refs = []
        current_table = []

        for line in lines:
            if line:
                line = line.strip()
                if line.startswith("Table"):
                    if current_table:
                        cleaned_table = self.clean_table("\n".join(current_table))
                        tables.append(cleaned_table)
                        current_table = []
                    current_table.append(line)
                elif line.startswith("Ref:"):
                    refs.append(line)
                elif current_table:
                    current_table.append(line)

        if current_table:
            cleaned_table = self.clean_table("\n".join(current_table))
            tables.append(cleaned_table)

        return tables, refs

    def clean_table(self, table):
        """
        Membersihkan tabel dari komentar dan teks tambahan setelah '}'.
        Menjaga komentar yang dimulai dengan '//dir:'.
        """
        cleaned_lines = []
        inside_table = False

        for line in table.splitlines():
            if line.startswith("Table"):
                inside_table = True
            # Lewati semua komentar kecuali yang dimulai dengan '//dir:'
            if line.startswith("//") and not line.startswith("//dir:") and inside_table:
                continue
            cleaned_lines.append(line)

        cleaned_table = "\n".join(cleaned_lines)
        cleaned_table = re.sub(r"}.*$", "}", cleaned_table)
        return cleaned_table

    def ck_is_null(self, ls):
        """
        Mengecek apakah atribut null didefinisikan.
        """
        if 'null' in ls:
            return True
        elif 'not null' in ls:
            return False
        else:
            return True

    def ck_is_primary(self, ls):
        """
        Mengecek apakah atribut primary key didefinisikan.
        """
        return 'pk' in ls

    def ck_is_increment(self, ls):
        """
        Mengecek apakah atribut auto increment didefinisikan.
        """
        return 'increment' in ls

    def ck_type(self, ty):
        """
        Mengecek Type
        """
        if ty.lower() == 'varchar':
            return ty + "(255)"
        return ty

    def ck_default(self, ls):
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

    def extract_table(self, table):
        """
        Mengekstrak metadata tabel dari teks diagram.
        """
        lines = [line for line in table.split('\n') if line.strip()]
        if not lines:
            return {}

        table_name = lines[0].split()[-1].replace('{', '')
        items_field = []
        dir = ""
        for line in lines[1:-1]:
            
            items = [item for item in line.split() if item]
            if(items[0] == '//dir:'):
                dir = items[1]
            else:
                tmp = {
                    'name': items[0],
                    'type': self.ck_type(items[1]),
                    'null': len(items) < 3,
                    'increment': False,
                    'attributes': ''
                }

                if 'id_' in items[0] or '_id' in items[0]:
                    tmp['attributes'] = 'UNSIGNED'

                match = re.search(r"\[(.*?)\]", line)
                if match:
                    result = re.split(r",\s*", match.group(1))
                    tmp['increment'] = self.ck_is_increment(result)
                    tmp['primary'] = self.ck_is_primary(result)
                    tmp['null'] = self.ck_is_null(result)
                    if tmp['primary']:
                        tmp['attributes'] = "UNSIGNED"
                        tmp['null'] = False

                    d_sts, d_val = self.ck_default(result)
                    if d_sts:
                        tmp['default'] = d_val

                items_field.append(tmp)

        result = {
            'dir'  : dir,
            'table': table_name,
            'items': items_field
        }

        return result

    def get_tabels(self):
        """
        Memproses teks diagram Tabel menjadi metadata JSON.
        """
        tables, _ = self.split_tabel_ref()
        metadata = [self.extract_table(table) for table in tables]
        return metadata
    
    def get_refs(self):
        """
        Memproses teks diagram Refs menjadi metadata JSON.
        """
        refs = []
        _, lines = self.split_tabel_ref()
        
        for line in lines:
            # Menghapus komentar yang diawali dengan `//`
            line = re.sub(r"//.*$", "", line).strip()
            
            # Regex untuk menangkap elemen-elemen referensi dengan operator tambahan seperti `<>`
            match = re.match(
                r'Ref:\s*"([^"]+)"\."([^"]+)"\s*(<|>|-|<>)\s*"([^"]+)"\."([^"]+)"\s*(?:\[(.*?)\])?',
                line
            )
            if match:
                tb1_name, tb1_ref, operator, tb2_name, tb2_ref, attributes = match.groups()
                attributes_dict = {}

                # Memproses atribut seperti `delete` dan `update` jika ada
                if attributes:
                    for attr in attributes.split(','):
                        key_value = attr.strip().split(':')
                        if len(key_value) == 2:
                            key, value = key_value
                            attributes_dict[key.strip()] = value.strip()

                # Menambahkan hasil dalam format JSON
                refs.append({
                    "tb1": {"name": tb1_name, "ref": tb1_ref},
                    "tb2": {"name": tb2_name, "ref": tb2_ref},
                    "mark": operator,
                    "att": attributes_dict
                })
        return refs
    
    def get_all(self):
        """
        Menggabungkan hasil tabel dan referensi menjadi metadata JSON.
        """
        return {
            'tabels': self.get_tabels(),
            'refs'  : self.get_refs()
        }
