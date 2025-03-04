import json, os, shutil
class MetaToModel:
    def __init__(self, json_data, exc=[]):
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
        
        self.exc = exc
    

    def ubah_nama(self,input_text):
        """
        Mengubah teks dengan format snake_case menjadi PascalCase.
        Contoh:
        - "jenis_barang" -> "JenisBarang"
        """
        if not input_text:
            return ""
        # Pecah teks berdasarkan underscore (_), kapitalisasi setiap kata, lalu gabungkan
        if(input_text.lower() == 'users'):
            return "User"
        return ''.join(word.capitalize() for word in input_text.split('_'))
    
    def get_class_rel_dir(self, table_data, table_name):
        for i in table_data:
            if(i['table'] == table_name):
                return "App\Models\\" + ( i['dir'] + "\\" ) if i['dir'] else "App\Models\\"
        return "App\Models\\"
    

    def json_to_model(self, table_data, refs_data):
        dir        = ( '\\' + table_data["dir"] ).replace('/','\\') if table_data["dir"] else ""
        table_name = table_data["table"]
        columns    = table_data["items"]
        model_name = self.ubah_nama(table_name)
 
        #-------------------------------------------------
        mod = '<?php \n'
        mod+= f'//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel \n'
        mod+= f'namespace App\Models{dir}; \n\n'
        mod+= f'use Illuminate\Database\Eloquent\Factories\HasFactory; \n'
        mod+= f'use Illuminate\Database\Eloquent\Model; \n'
        mod+= f'use Illuminate\Database\Eloquent\Relations\HasOne; \n'
        mod+= f'use Illuminate\Database\Eloquent\Relations\BelongsTo; \n'
        mod+= f'use Illuminate\Database\Eloquent\Relations\HasMany; \n\n'
        mod+= 'Class ' + model_name+ ' extends Model { \n'
        mod+= '    use HasFactory; \n'
        mod+= f"    protected $table = '{table_name}'; \n"
        mod+=  '    protected $fillable = [ \n'
        #-------------------------------------------------
        for i in columns:
            if(i['name'] != 'created_at' and i['name'] != 'updated_at' ):
                mod +='        "' + i['name'] +'", \n'

        mod+= '    ]; \n\n'
        #-------------------------------------------------
        #relasi
        #-------------------------------------------------
        for i in refs_data:
            if(i["tb1"]["name"] == table_name or i["tb2"]["name"] == table_name): 
                #-----------------------------------------  
                seleted   = ""
                name_func = ""
                rela      = ""
                class_rel = ""
                class_ref = ""
                class_dir = ""
                if(i['mark'] == '-'): #one-to-one
                    if(i["tb1"]["name"] != table_name):
                        seleted = i["tb1"]
                    if(i["tb2"]["name"] != table_name):
                        seleted = i["tb2"]
                    name_func   = seleted['name']
                    rela        = "hasOne"
                    class_rel   = self.ubah_nama(name_func)
                    class_ref = seleted['ref']
                    class_dir   = self.get_class_rel_dir(self.json_data['tabels'], name_func)
                elif(i['mark'] == '<'): #< one-to-many
                    seleted = i["tb2"]
                    if seleted['name'] != table_name :
                        name_func = seleted['name']
                        rela      = "hasMany"
                        class_rel = self.ubah_nama(name_func)
                        class_ref = seleted['ref']
                        class_dir   = self.get_class_rel_dir(self.json_data['tabels'], name_func)
                    else:
                        name_func = seleted['ref'].replace('id_', '').replace('_id', '')
                        rela      = "belongsTo"
                        class_rel = self.ubah_nama(i["tb1"]['name'])
                        class_ref = seleted['ref']
                        class_dir   = self.get_class_rel_dir(self.json_data['tabels'], i["tb1"]['name'])
                elif(i['mark'] == '>'): #< many-to-one
                    seleted = i["tb1"]
                    if seleted['name'] != table_name :
                        name_func = seleted['name']
                        rela      = "hasMany"
                        class_rel = self.ubah_nama(name_func)
                        class_ref = seleted['ref']
                        class_dir   = self.get_class_rel_dir(self.json_data['tabels'], name_func)
                    else:
                        name_func = seleted['ref'].replace('id_', '').replace('_id', '')
                        rela      = "belongsTo"
                        class_rel = self.ubah_nama(i["tb2"]['name'])
                        class_ref = seleted['ref']
                        class_dir   = self.get_class_rel_dir(self.json_data['tabels'], i["tb2"]['name'])
                #-----------------------------------------       
                class_ref = "," + "'" +class_ref + "'" if  class_ref else ''    
                mod += f"    //{i['tb1']['name']} {i['mark']} {i['tb2']['name']} \n"
                mod += "    public function " + name_func + "(): "+rela+" { \n"
                mod += f"        return $this->{rela}('{ class_dir + class_rel}' {class_ref});\n"
                mod += "    }\n\n"
                
        #-------------------------------------------------
        #-------------------------------------------------
        mod+= '} \n'
        #-------------------------------------------------
        return {
            'table' : table_name,
            'model' : model_name,
            'path'  : '/' + table_data["dir"] if table_data["dir"] else '',
            'class' : mod
        }
    
    def process_and_save(self):
        # Path ke direktori yang akan dihapus
        models_dir = "out/app/Models"

        print('\n\n+=============================================+')
        print('|             Generating Models               |')
        print('+=============================================+')

        # Hapus direktori jika ada
        if os.path.exists(models_dir):
            shutil.rmtree(models_dir)
            print(f"Direktori {models_dir} berhasil dihapus.")

        table_data = self.json_data['tabels']
        refs_data = self.json_data['refs']
        
        total_file = 0
        for i in table_data:
            if i['table'].lower() not in [exc_item.lower() for exc_item in self.exc]:
                total_file += 1
                d = self.json_to_model(i, refs_data)
                output_dir = models_dir + d['path']
                
                # Membuat folder jika belum ada
                os.makedirs(output_dir, exist_ok=True)
                
                # Path untuk file model
                output_path = output_dir + "/" + d['model'] + '.php'
                
                # Menulis file model
                with open(output_path, "w") as file:
                    file.write(d['class'])

                print(f"Model berhasil disimpan di {output_path}")
                #print(d['class'])
                #print(json.dumps(d, indent=4))
        print('+=============================================+')
        print(f"Total File                   : {total_file}")
        if(self.exc):
            print(f"Total pengecualian           : {len(self.exc)}")
            print(f"Memproses dengan pengecualian: {self.exc}")
        
        print('+=============================================+')