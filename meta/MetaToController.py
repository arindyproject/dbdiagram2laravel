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
        return str(tbl['items'][1]['name'])

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


    def json_to_model(self, table_data):
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

        #table
        #-------------------------------------------------
        mod += '    //table-----------------------------------------------------------\n'
        mod += '    public function table(Request $request){\n'
        mod += '        try {\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            //row : represents the number of records displayed per page, default: 20 \n'
        mod += '            //Sorting data \n'
        mod += '            //sort     : column_name \n'
        mod += '            //direction: asc / desc \n'
        mod += '            // Search  \n'
        mod += '            /**  \n'
        mod += '             * $search = [ \n'
        mod += '             *      [ \n'
        mod += '             *          "query"   : "column_name", \n'
        mod += '             *          "mark"    : "LIKE",  // "=",">","<"  \n'
        mod += '             *          "request" : "search request / input name in HTML"  \n'
        mod += '             *          "type"    : "text", \n'
        mod += '             *      ],  \n'
        mod += '             * ] \n'
        mod += '             * **/ \n'
        mod += '            //-----------------------------------------------\n'
        mod += '            /** Postman example body \n'
        mod += '            *{ \n'
        mod += '            *    "page"      : 1, \n'
        mod += '            *    "row"       : 30, \n'
        mod +=f'            *    "sort"      : "{self.cek_name_tbl_out_type(table_name)}", \n'
        mod += '            *    "direction" : "desc", \n'
        mod +=f'            *    "search_{self.cek_name_tbl_out_type(table_name)}" : "na" \n'
        mod += '            *} \n'
        mod += '            * **/ \n'
        mod += '            //-----------------------------------------------\n'
        mod += '            $search = [ \n'
        mod += '                [ \n'
        mod +=f'                    "query"   => "{self.cek_name_tbl_out_type(table_name)}", \n'
        mod += '                    "mark"    => "LIKE",  // "=",">","<"  \n'
        mod +=f'                    "request" => "search_{self.cek_name_tbl_out_type(table_name)}",  \n'
        mod += '                    "type"    => "text",  \n'
        mod += '                ],  \n'
        mod += '            ]; \n'
        mod += '            $row    = $request->input("row") ? $request->input("row") : 20; \n'
        mod += '            $query  = $this->model->query(); //table data \n'
        mod += '            //-----------------------------------------------\n'
        mod += '            if ($request->has("sort")) { \n'
        mod += '                $sortField = $request->input("sort"); \n'
        mod += '                $sortDirection = $request->input("direction", "asc"); \n'
        mod += '                $query->orderBy($sortField, $sortDirection); \n'
        mod += '            } \n'
        mod += '            //-----------------------------------------------\n'
        mod += "            if(count($search) > 0){ \n"
        mod += "                foreach ($search as $d) { \n"
        mod += "                    if($request->has($d['request']) && $request->input($d['request'])){ \n"
        mod += "                        $val =  $request->input($d['request']); \n"
        mod += "                        if($d['type'] == 'date'){ \n"
        mod += "                            $query->whereDate($d['query'], $d['mark'], $val)->get(); \n"
        mod += "                        } \n"
        mod += "                        else{ \n"
        mod += "                            if($d['mark'] == 'LIKE'){ \n"
        mod += "                                $query->where($d['query'], $d['mark'], '%'. $val . '%'); \n"
        mod += "                            }else{ \n"
        mod += "                                $query->where($d['query'], $d['mark'], $val); \n"
        mod += "                            } \n"
        mod += "                        } \n"                
        mod += "                    } \n"
        mod += "                } \n"
        mod += "            } \n"
        mod += '            //-----------------------------------------------\n'
        mod += '            $data = $query->paginate($row); \n'
        mod += '            //-----------------------------------------------\n'
        mod += "            if($data){ \n"
        mod += "                $datas = [ \n"
        mod += "                    'data'       => $this->res->collection($data), \n"
        mod += "                    'search'     => $search, \n"
        mod += "                    'pagination' => [ \n"
        mod += "                        'row'           => $row, \n"
        mod += "                        'current_page'  => $data->currentPage(), \n"
        mod += "                        'per_page'      => $data->perPage(), \n"
        mod += "                        'max_page'      => ceil($data->total() / $data->perPage()), \n"
        mod += "                        'total'         => $data->total(), \n"
        mod += "                    ], \n"
        mod += "                ]; \n"
        mod += "                // Check if the data contains any records\n"
        mod += "                if($data->total()){ \n"
        mod += "                    // Success: Data is available and returned to the user\n"
        mod += "                    return response( \n"
        mod += "                        new BaseResource( \n"
        mod += "                            true, \n"
        mod += "                            $this->title . ' - Data successfully found.', \n"
        mod += "                            $datas \n"
        mod += "                        ), 200); \n"
        mod += "                } \n"
        mod += "                // No records found: Return a clean 'not found' response\n"
        mod += "                return response( \n"
        mod += "                    new BaseResource( \n"
        mod += "                        false, \n"
        mod += "                        $this->title . ' - No data found.', \n"
        mod += "                        $datas \n"
        mod += "                    ), 404); \n"
        mod += "            }else{ \n"
        mod += "                // Edge case: Data is null or an invalid request was made\n"
        mod += "                return response( \n"
        mod += "                    new BaseResource(false, $this->title . ' - No data available. Please verify your query.', [] \n"
        mod += "                ), 404); \n"
        mod += "            } \n"
        mod += '            //-----------------------------------------------\n'
        mod += '        } catch (\Exception $e) {\n'
        mod += '            // Handle any errors during retrieval\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(false, "An error occurred while retrieving data: (" . $e->getMessage() . ")")\n'
        mod += '            , 442);\n'
        mod += '        }\n'
        mod += '    } \n'
        mod += '    //end_table-------------------------------------------------------\n\n\n'
        #-------------------------------------------------

        #list with search functionality
        #-------------------------------------------------
        mod += '    //list with search functionality-----------------------------------\n'
        mod += '    public function search(Request $request){\n'
        mod += '        // Retrieve a list of all data with "id" as value and "name" as label.\n'
        mod += '        // Allows filtering with a search query using the LIKE operator.\n'
        mod += '        // If the "name" field is unavailable, it will use the second column after "id".\n'
        mod += '        try {\n'
        mod += '            // Get search parameter from the request\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            if($request->filled("q")){ \n'
        mod += '                //-----------------------------------------------\n'
        mod += '                $search = $request->get("q");\n'
        mod += f'                $record = $this->model->select("id", "{self.cek_name_tbl_out_type(table_name)}")\n'
        mod += '                    ->when($search, function ($query) use ($search) {\n'
        mod += f'                        $query->where("{self.cek_name_tbl_out_type(table_name)}", "LIKE", "%" . $search . "%");\n'
        mod += '                    })->get();\n'
        mod += '                //-----------------------------------------------\n'
        mod += '                if ($record->count() < 1) {\n'
        mod += '                    return response(\n'
        mod += '                        new BaseResource(false, "No matching data found"),\n'
        mod += '                        404\n'
        mod += '                    );\n'
        mod += '                }\n'
        mod += '                //-----------------------------------------------\n\n'
        mod += '                // Map the data to a key-value structure (value = id, name = name)\n'
        mod += '                //-----------------------------------------------\n'
        mod += '                $data = $record->map(function ($item) {\n'
        mod += '                    return [\n'
        mod += '                        "value" => $item->id,\n'
        mod += f'                        "name"  => $item->{self.cek_name_tbl_out_type(table_name)} ?? "Unnamed"\n'
        mod += '                    ];\n'
        mod += '                });\n'
        mod += '                //-----------------------------------------------\n\n'   
        mod += '                // Return the mapped data as a successful response\n'
        mod += '                //-----------------------------------------------\n'
        mod += '                return response(\n'
        mod += '                    new BaseResource(true, "Data retrieved successfully", $data),\n'
        mod += '                    200\n'
        mod += '                );\n'
        mod += '            }\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(false, "Please provide the query first!!!"),\n'
        mod += '                442\n'
        mod += '            );\n'
        mod += '            //-----------------------------------------------\n'
        mod += '        } catch (\Exception $e) {\n'
        mod += '            // Handle any exceptions that occur during the process\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(false, "An error occurred while retrieving data: (" . $e->getMessage() . ")"),\n'
        mod += '                442\n'
        mod += '            );\n'
        mod += '        }\n'
        mod += '    }\n'
        mod += '    //end_list with search functionality-------------------------------\n\n\n'
        #-------------------------------------------------


       #list
        #-------------------------------------------------
        mod += '    //list---------------------------------------------------\n'
        mod += '    public function list(){\n'
        mod += '        // Retrieve a list of all data with "id" as value and "name" as label.\n'
        mod += '        // If the "name" or "nama" field is unavailable, it will use the second column after "id".\n'
        mod += '        try {\n'
        mod += '            // Query the database to select "id" and the appropriate name field\n'
        mod += '            //-----------------------------------------------\n'
        mod += f'            $record = $this->model->select("id", "{self.cek_name_tbl_out_type(table_name)}")->get();\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            // Check if any records are found\n'
        mod += '            if ($record->count() < 1) {\n'
        mod += '                return response(\n'
        mod += '                    new BaseResource(false, "Data not found"),\n'
        mod += '                    404\n'
        mod += '                );\n'
        mod += '            }\n'
        mod += '            //-----------------------------------------------\n\n'
        mod += '            // Map the data to a key-value structure (value = id, name = name)\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            $data = $record->map(function ($item) {\n'
        mod += '                return [\n'
        mod += '                    "value" => $item->id,\n'
        mod += f'                    "name"  => $item->{self.cek_name_tbl_out_type(table_name)} ?? "Unnamed"\n'
        mod += '                ];\n'
        mod += '            });\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            // Return the mapped data as a successful response\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(true, "Data retrieved successfully", $data),\n'
        mod += '                200\n'
        mod += '            );\n'
        mod += '        } catch (\Exception $e) {\n'
        mod += '            // Handle any exceptions that occur during the process\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            return response(\n'
        mod += '                new BaseResource(false, "An error occurred while retrieving data: (" . $e->getMessage() . ")"),\n'
        mod += '                442\n'
        mod += '            );\n'
        mod += '        }\n'
        mod += '    }\n'
        mod += '    //end_list-----------------------------------------------\n\n\n'
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
        mod += '        } catch (\Exception $e) {\n'
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
        mod += '        } catch (\Exception $e) {\n'
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
        mod += '            //-----------------------------------------------\n\n'
        mod += '            //update data\n'
        mod += '            //-----------------------------------------------\n'
        mod += '            if(!$record->update($request->all()) ){\n'
        mod += '                return response(new BaseResource(false, "Failed to update data."), 442);\n'
        mod += '            }\n'
        mod += '            return response(new BaseResource(true, "Data updated successfully.", $this->res->make($record) ), 200);\n'
        mod += '            //-----------------------------------------------\n'
        mod += '        } catch (\Exception $e) {\n'
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
        mod += '        } catch (\Exception $e) {\n'
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
                d = self.json_to_model(i)
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