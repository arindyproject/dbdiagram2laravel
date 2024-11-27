import json, os
## > many-to-one; < one-to-many; - one-to-one; <> many-to-many
class MetaToSql:
    def __init__(self, json_data):
        """
        Inisialisasi MetaToSql dengan data JSON.
        :param json_data: Data JSON yang berisi definisi tabel.
        """
        if isinstance(json_data, str):
            self.json_data = json.loads(json_data)
        elif isinstance(json_data, dict):  # Sesuaikan jika data berupa list
            self.json_data = json_data
        else:
            raise ValueError("Input harus berupa string JSON atau list dictionary.")

    def json_to_mysql(self, table_data):
        """
        Mengonversi metadata JSON menjadi query SQL CREATE TABLE.
        :param table_data: Data JSON untuk satu tabel.
        """
        table_name = table_data["table"]
        columns = table_data["items"]

        # Mulai query CREATE TABLE
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"

        column_definitions = []
        for col in columns:
            column_def = f"  {col['name']} {col['type']}"

            # Tambahkan atribut jika ada
            if col.get("attributes"):
                column_def += f" {col['attributes']}"

            # Cek apakah kolom tidak boleh null
            if not col["null"]:
                column_def += " NOT NULL"
            else:
                column_def += " NULL"

            # Tambahkan default value jika ada
            if "default" in col:
                default_value = col["default"]
                if isinstance(default_value, str) and default_value.lower() == "null":
                    column_def += " DEFAULT NULL"
                elif isinstance(default_value, str):
                    column_def += f" DEFAULT '{default_value}'"
                else:
                    column_def += f" DEFAULT {default_value}"

            # Tambahkan AUTO_INCREMENT jika ada
            if col.get("increment"):
                column_def += " AUTO_INCREMENT"

            column_definitions.append(column_def)

        # Tambahkan kolom ke query
        sql += ",\n".join(column_definitions)

        # Tambahkan primary key jika ada
        primary_keys = [col["name"] for col in columns if col.get("primary")]
        if primary_keys:
            sql += f",\n  PRIMARY KEY ({', '.join(primary_keys)})"

        # Akhiri query CREATE TABLE
        sql += "\n);"

        return sql

    def json_to_alter(self, json_data):
        sql_statements = []

        for ref in json_data:
            tb1 = ref['tb1']
            tb2 = ref['tb2']
            mark = ref['mark']
            att = ref.get('att', {})

            # Menentukan aksi ON DELETE
            on_delete = f" ON DELETE {att['delete'].upper()}" if 'delete' in att else ""
            on_update = f" ON UPDATE {att['update'].upper()}" if 'update' in att else ""

            # Menentukan perintah ALTER TABLE berdasarkan arah referensi
            if mark in ["<", ">"]:  # Foreign key relationship
                table = tb2['name'] if mark == "<" else tb1['name']
                column = tb2['ref'] if mark == "<" else tb1['ref']
                ref_table = tb1['name'] if mark == "<" else tb2['name']
                ref_column = tb1['ref'] if mark == "<" else tb2['ref']

                sql = f"ALTER TABLE `{table}` ADD FOREIGN KEY (`{column}`) REFERENCES `{ref_table}` (`{ref_column}`){on_delete}{on_update};"
                sql_statements.append(sql)

            elif mark == "-":  # Bi-directional (assumed as a single direction for SQL FK)
                sql = f"ALTER TABLE `{tb2['name']}` ADD FOREIGN KEY (`{tb2['ref']}`) REFERENCES `{tb1['name']}` (`{tb1['ref']}`){on_delete}{on_update};"
                sql_statements.append(sql)

        return "\n".join(sql_statements)

    def process_and_save(self, file_name="output.sql"):
        """
        Memproses JSON untuk semua tabel dan menyimpannya ke folder 'out'.
        :param file_name: Nama file output.
        """
        # Buat folder 'out' jika belum ada
        output_dir = "out"
        os.makedirs(output_dir, exist_ok=True)
        
        # Path lengkap untuk file output
        output_path = os.path.join(output_dir, file_name)
        
        sql_queries = []

        # Proses CREATE TABLE
        for table_data in self.json_data['tabels']:
            sql_queries.append(self.json_to_mysql(table_data))
        
        # Proses ALTER TABLE
        alter_queries = self.json_to_alter(self.json_data['refs'])
        if alter_queries:
            sql_queries.append(alter_queries)
        
        # Gabungkan semua query menjadi satu string
        final_sql = "\n\n".join(sql_queries)

        # Simpan ke file
        with open(output_path, "w") as file:
            file.write(final_sql)
        
        print(f"SQL berhasil disimpan di {output_path}")