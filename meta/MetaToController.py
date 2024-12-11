import json, os, shutil, re

class MetaToController:
    def __init__(self, json_data, dir="", exc=[]):
        """
        Inisialisasi MetaToRes dengan data JSON.
        :param json_data: Data JSON yang berisi definisi tabel.
        """
        if isinstance(json_data, str):
            self.json_data = json.loads(json_data)
        elif isinstance(json_data, dict):  # Sesuaikan jika data berupa list
            self.json_data = json_data
        else:
            raise ValueError("Input harus berupa string JSON atau list dictionary.")

        self.exc = exc
        self.dir = "/" + dir if dir else ""

    def ubah_nama(self,input_text):
        """
        Mengubah teks dengan format snake_case menjadi PascalCase.
        Contoh:
        - "jenis_barang" -> "JenisBarangController"
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
                return f"App\Http\Controllers{self.dir}\\" + ( i['dir'] + "\\" ) if i['dir'] else f"App\Http\Controllers{self.dir}\\"
        return f"App\Http\Controllers{self.dir}\\"
    
    def cek_name_tbl_out_type(self, table_name):
        table_data = self.json_data['tabels']
        tbl = []
        for tb in table_data:
            if(table_name == tb['table']):
                tbl = tb
                break
        
        if(tbl):
            for i in tbl['items']:
                if('name' in i['name']):
                    return i['name']
                elif('nama' in i['name']):
                    return i['name']
        return ""

    def convert_sql_roles(self,sql_type):
        """
        Convert SQL data type to Laravel Validator Rule.
        
        :param sql_type: The SQL data type as a string.
        :return: Laravel Validator Rule as a string.
        """
        sql_type = sql_type.lower()
        
        # Mapping SQL data types to Laravel Validator Rules
        type_mapping = {
            "varchar": lambda size: f"string|max:{size[0]}" if size else "string",
            "char": lambda size: f"string|max:{size[0]}" if size else "string",
            "text": lambda _: "string",
            "integer": lambda _: "integer",
            "int": lambda _: "integer",
            "smallint": lambda _: "integer",
            "bigint": lambda _: "integer",
            "decimal": lambda args: f"numeric:{args[0]},{args[1]}" if len(args) == 2 else "numeric",
            "numeric": lambda args: f"numeric:{args[0]},{args[1]}" if len(args) == 2 else "numeric",
            "float": lambda _: "numeric",
            "real": lambda _: "numeric",
            "double": lambda _: "numeric",
            "boolean": lambda _: "boolean",
            "tinyint": lambda size: "boolean" if size == "1" else "integer",
            "date": lambda _: "date|date_format:Y-m-d",
            "datetime": lambda _: "date|date_format:Y-m-d H:i:s",
            "timestamp": lambda _: "date|date_format:Y-m-d H:i:s",
            "time": lambda _: "date_format:H:i:s",
            "year": lambda _: "digits:4",
            "blob": lambda _: "file",
            "longblob": lambda _: "file",
            "json": lambda _: "json",
            "enum": lambda args: f"in:{','.join(args)}",
            "set": lambda _: "array",
            "uuid": lambda _: "uuid",
            "ip address": lambda _: "ip",
            "email": lambda size: f"email|max:{size}" if size else "email",
        }

        # Extract type and parameters
        match = re.match(r"(\w+)(?:\((.*?)\))?", sql_type)
        if not match:
            return "unknown"
        
        base_type = match.group(1)
        args = match.group(2)
        args_list = args.split(",") if args else []

        # Remove quotes and trim whitespace from args
        args_list = [arg.strip().strip("'").strip('"') for arg in args_list]

        # Determine the conversion rule
        converter = type_mapping.get(base_type)
        if converter:
            return converter(args_list)
        else:
            return "unknown"
    
    def cek_validation(self, i, table_name, max_length=10):
        #print(i)
        is_null = "nullable" if i["null"] else "required"
        typ     = self.convert_sql_roles( i["type"] )
        li= i["name"]

        uni= f'|unique:{table_name}'  if i['is_unique'] else ''
        upd= f".($id ? ',{i["name"]},' . $id . ',id'  : '')" if i['is_unique'] else ''

        ri= f'"{is_null}|{ typ }{uni}" {upd}'

        return f'            "{li}"{" " * (max_length - len(li))} => {ri}, \n'


    def json_to_model(self, table_data, refs_data):
        dir        = ( '\\' + table_data["dir"] ).replace('/','\\') if table_data["dir"] else ""
        table_name = table_data["table"]
        columns    = table_data["items"]
        model_name = self.ubah_nama(table_name)
 
        #-------------------------------------------------
        mod = '<?php \n'
        mod+= '//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel \n'
        mod+= 'namespace App\Http\Controllers'+self.dir.replace("/","\\")+dir+'; \n\n'
        mod+= 'use App\Http\Controllers\Controller; \n'
        mod+= 'use Illuminate\Http\Request; \n'
        mod+= 'use Illuminate\Support\Facades\Auth; \n'
        mod+= 'use Illuminate\Support\Facades\Validator; \n'
        mod+= ' \n'
        mod+= 'use App\Http\Resources\BaseResource; \n'
        mod+= 'use App\Http\Resources' + dir + '\\' + model_name + 'Resource; \n'
        mod+= 'use App\Models' + dir + '\\' + model_name + '; \n'
        mod+= ' \n'

        mod+= 'Class ' + model_name+ 'Controller' + ' extends Controller { \n'
        #construct
        #-------------------------------------------------
        mod+= '    //construct----------------------------------------------\n'
        mod+= '    public function __construct(){\n'
        mod+= f'        $this->title = "{model_name}";\n'
        mod+= f'        $this->model = new {model_name};\n'
        mod+= f'        $this->res   = new {model_name}Resource(null);\n'
        mod+= '    }\n'
        mod+= '    //end_construct------------------------------------------\n\n\n'
        #-------------------------------------------------


        #Validation roles
        #-------------------------------------------------
        mod+= '    //roles--------------------------------------------------\n'
        mod+= '    protected function getValidationRules($id = null){ \n'
        mod+= '        return[\n'
        #-------------------------------------------------
        max_length = max(len(i['name']) for i in columns)
        for i in columns:
            if(i['name'] != 'created_at' and i['name'] != 'updated_at' and i['name'] != 'id' ):
                mod+= self.cek_validation(i, table_name=table_name, max_length=max_length)
        #-------------------------------------------------
        mod+= '        ]; \n'
        mod+= '    }\n'
        mod+= '    //end_roles----------------------------------------------\n\n\n'
        #-------------------------------------------------

        #list
        #-------------------------------------------------
        mod+= '    //list---------------------------------------------------\n'
        mod+= '    public function list(){\n'

        mod+= '    }\n'
        mod+= '    //end_list-----------------------------------------------\n\n\n'
        #-------------------------------------------------

        #show
        #-------------------------------------------------
        mod+= '    //show---------------------------------------------------\n'
        mod += '    public function show($id){\n'
        mod += '        try {\n'
        mod += '            // Find the record by ID\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            $record = $this->model->find($id);\n'
        mod += '            if (!$record) {\n'
        mod += '                return response(\n'
        mod += '                    new BaseResource(false, "Data not found for ID: " . $id),\n'
        mod += '                    404\n'
        mod += '                );\n'
        mod += '            }\n'
        mod += '            //-----------------------------------------------\n\n'
        mod += '            // Return the record directly\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(true, "Data successfully retrieved.", $this->res->make($record) )\n'
        mod += '            , 200);\n'
        mod += '            //-----------------------------------------------\n'
        mod += '        } catch (Exception $e) {\n'
        mod += '            // Handle any errors during retrieval\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(false, "An error occurred while retrieving data: (" . $e->getMessage() . ")")\n'
        mod += '            , 442);\n'
        mod += '        }\n'
        mod += '    }\n'
        mod += '    //end_show-----------------------------------------------\n\n\n'
        #-------------------------------------------------

        #create
        #-------------------------------------------------
        mod+= '    //create-------------------------------------------------\n'
        mod+= '    public function create(Request $request){\n'
        mod += '        try {\n'
        mod += '            //validation input\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            $validator = Validator::make($request->all(), $this->getValidationRules() ); \n'
        mod += '            if ($validator->fails()) { \n'
        mod += '                return response( \n'
        mod += '                    new BaseResource(false, \n'
        mod += '                        $this->title . " => Input error occurred!!, while adding data", \n'
        mod += '                        [], $validator->errors()\n'
        mod += '                ), 442); \n'
        mod += '            } \n'
        mod += '            //-----------------------------------------------\n\n'
        mod += '            //add new data\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            $record = $this->model->create($request->all());\n'
        mod += '            if(!$record){\n'
        mod += '                return response(new BaseResource(false, "Failed to create data."), 442);\n'
        mod += '            }\n'
        mod += '            return response(new BaseResource(true, "Data created successfully.", $this->res->make($record) ), 200);\n'
        mod += '            //-----------------------------------------------\n'
        mod += '        } catch (Exception $e) {\n'
        mod += '            // Handle any errors during retrieval\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(false, "An error occurred while creating data: (" . $e->getMessage() . ")")\n'
        mod += '            , 442);\n'
        mod += '        }\n'
        mod+= '    }\n'
        mod+= '    //end_create---------------------------------------------\n\n\n'
        #-------------------------------------------------

        #update
        #-------------------------------------------------
        mod+= '    //update-------------------------------------------------\n'
        mod+= '    public function update(Request $request, $id){\n'
        mod += '        try {\n'
        mod += '            // Find the record by ID\n'
        mod += '            $record = $this->model->find($id);\n'
        mod += '            if (!$record) {\n'
        mod += '                return response(\n'
        mod += '                    new BaseResource(false, "Data not found for ID: " . $id),\n'
        mod += '                    404\n'
        mod += '                );\n'
        mod += '            }\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            \n'
        mod += '            //validation input\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            $validator = Validator::make($request->all(), $this->getValidationRules($id) ); \n'
        mod += '            if ($validator->fails()) { \n'
        mod += '                return response( \n'
        mod += '                    new BaseResource(false, \n'
        mod += '                        $this->title . " => Input error occurred!!, while adding data", \n'
        mod += '                        [], $validator->errors()\n'
        mod += '                ), 442); \n'
        mod += '            } \n'
        mod += '            //-----------------------------------------------\n'
        mod += '        } catch (Exception $e) {\n'
        mod += '            // Handle any errors during retrieval\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(false, "An error occurred while updating data: (" . $e->getMessage() . ")")\n'
        mod += '            , 442);\n'
        mod += '        }\n'
        mod+= '    }\n'
        mod+= '    //end_update---------------------------------------------\n\n\n'
        #-------------------------------------------------

        #delete
        #-------------------------------------------------
        mod += '    //delete-------------------------------------------------\n'
        mod += '    public function delete($id){\n'
        mod += '        try {\n'
        mod += '            // Find the record by ID\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            $record = $this->model->find($id);\n'
        mod += '            if (!$record) {\n'
        mod += '                return response(\n'
        mod += '                    new BaseResource(false, "Data not found for ID: " . $id),\n'
        mod += '                    404\n'
        mod += '                );\n'
        mod += '            }\n'
        mod += '            //-----------------------------------------------\n\n'
        mod += '            // Attempt to delete the record\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            if ($record->delete()) {\n'
        mod += '                // Return success response\n'
        mod += '                return response(\n'
        mod += '                    new BaseResource(true, "Data successfully deleted.")\n'
        mod += '                , 200);\n'
        mod += '            } else {\n'
        mod += '                // Return failure response if delete failed\n'
        mod += '                return response(\n'
        mod += '                    new BaseResource(false, "Failed to delete the data.")\n'
        mod += '                , 500);\n'
        mod += '            }\n'
        mod += '            //-----------------------------------------------\n'
        mod += '        } catch (Exception $e) {\n'
        mod += '            // Handle any errors during deletion\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(false, "An error occurred while deleting data: (" . $e->getMessage() . ")")\n'
        mod += '            , 442);\n'
        mod += '        }\n'
        mod += '    }\n'
        mod += '    //end_delete---------------------------------------------\n\n\n'

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
        models_dir = "out/app/Http/Controllers" 

        print('\n\n+=============================================+')
        print('|             Generating Controllers          |')
        print('+=============================================+')

        # Hapus direktori jika ada
        if os.path.exists(models_dir):
            shutil.rmtree(models_dir)
            print(f"Direktori {models_dir} berhasil dihapus.")

        table_data = self.json_data['tabels']
        refs_data = self.json_data['refs']

        models_dir = models_dir + self.dir
        
        total_file = 0
        for i in table_data:
            if i['table'].lower() not in [exc_item.lower() for exc_item in self.exc]:
                total_file += 1
                d = self.json_to_model(i, refs_data)
                output_dir = models_dir + d['path']
                
                # Membuat folder jika belum ada
                os.makedirs(output_dir, exist_ok=True)
                
                # Path untuk file model
                output_path = output_dir + "/" + d['model'] + 'Controller' + '.php'
                
                # Menulis file model
                with open(output_path, "w") as file:
                    file.write(d['class'])

                print(f"Controllers berhasil disimpan di {output_path}")
                #print(d['class'])
                #print(json.dumps(d, indent=4))
        print('+=============================================+')
        print(f"Total File                   : {total_file}")
        if(self.exc):
            print(f"Total pengecualian           : {len(self.exc)}")
            print(f"Memproses dengan pengecualian: {self.exc}")
        
        print('+=============================================+')