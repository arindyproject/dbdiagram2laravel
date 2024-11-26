import json

class MetaToSql:
    def __init__(self, json_data):
        """
        Inisialisasi MetaToSql dengan data JSON.
        :param json_data: Data JSON yang berisi definisi tabel.
        """
        if isinstance(json_data, str):
            self.json_data = json.loads(json_data)
        elif isinstance(json_data, list):  # Sesuaikan jika data berupa list
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
        sql = f"CREATE TABLE {table_name} (\n"

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

    def process_and_save(self, file_name="output.sql"):
        """
        Memproses JSON untuk semua tabel dan menyimpannya ke file.
        :param file_name: Nama file output.
        """
        sql_queries = []
        for table_data in self.json_data:
            sql_queries.append(self.json_to_mysql(table_data))
        
        # Gabungkan semua query menjadi satu string
        final_sql = "\n\n".join(sql_queries)

        # Simpan ke file
        with open(file_name, "w") as file:
            file.write(final_sql)
        print(f"SQL berhasil disimpan di {file_name}")