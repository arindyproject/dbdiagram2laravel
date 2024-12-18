<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Http\Controllers\Kasir; 

use App\Http\Controllers\Controller; 
use Illuminate\Http\Request; 
use Illuminate\Support\Facades\Auth; 
use Illuminate\Support\Facades\Validator; 
 
use App\Http\Resources\BaseResource; 
use App\Http\Resources\Kasir\KTransaksiItemsResource; 
use App\Models\Kasir\KTransaksiItems; 
 
Class KTransaksiItemsController extends Controller { 
    //construct----------------------------------------------
    public function __construct(){
        $this->title = "KTransaksiItems";
        $this->model = new KTransaksiItems;
        $this->res   = new KTransaksiItemsResource(null);
    }
    //end_construct------------------------------------------


    //roles--------------------------------------------------
    protected function getValidationRules($id = null){ 
        return[
            "id_transaksi" => "required|integer" , 
            "id_produk"    => "required|integer" , 
            "jumlah"       => "required|integer" , 
            "harga"        => "required|numeric:10,2" , 
        ]; 
    }
    //end_roles----------------------------------------------


    //table-----------------------------------------------------------
    public function table(Request $request){
        try {
            //-----------------------------------------------
            //row : represents the number of records displayed per page, default: 20 
            //Sorting data 
            //sort     : column_name 
            //direction: asc / desc 
            // Search  
            /**  
             * $search = [ 
             *      [ 
             *          "query"   : "column_name", 
             *          "mark"    : "LIKE",  // "=",">","<"  
             *          "request" : "search request / input name in HTML"  
             *          "type"    : "text", 
             *      ],  
             * ] 
             * **/ 
            //-----------------------------------------------
            /** Postman example body 
            *{ 
            *    "page"      : 1, 
            *    "row"       : 30, 
            *    "sort"      : "id_transaksi", 
            *    "direction" : "desc", 
            *    "search_id_transaksi" : "na" 
            *} 
            * **/ 
            //-----------------------------------------------
            $search = [ 
                [ 
                    "query"   => "id_transaksi", 
                    "mark"    => "LIKE",  // "=",">","<"  
                    "request" => "search_id_transaksi",  
                    "type"    => "text",  
                ],  
            ]; 
            $row    = $request->input("row") ? $request->input("row") : 20; 
            $query  = $this->model->query(); //table data 
            //-----------------------------------------------
            if ($request->has("sort")) { 
                $sortField = $request->input("sort"); 
                $sortDirection = $request->input("direction", "asc"); 
                $query->orderBy($sortField, $sortDirection); 
            } 
            //-----------------------------------------------
            if(count($search) > 0){ 
                foreach ($search as $d) { 
                    if($request->has($d['request']) && $request->input($d['request'])){ 
                        $val =  $request->input($d['request']); 
                        if($d['type'] == 'date'){ 
                            $query->whereDate($d['query'], $d['mark'], $val)->get(); 
                        } 
                        else{ 
                            if($d['mark'] == 'LIKE'){ 
                                $query->where($d['query'], $d['mark'], '%'. $val . '%'); 
                            }else{ 
                                $query->where($d['query'], $d['mark'], $val); 
                            } 
                        } 
                    } 
                } 
            } 
            //-----------------------------------------------
            $data = $query->paginate($row); 
            //-----------------------------------------------
            if($data){ 
                $datas = [ 
                    'data'       => $this->res->collection($data), 
                    'search'     => $search, 
                    'pagination' => [ 
                        'row'           => $row, 
                        'current_page'  => $data->currentPage(), 
                        'per_page'      => $data->perPage(), 
                        'max_page'      => ceil($data->total() / $data->perPage()), 
                        'total'         => $data->total(), 
                    ], 
                ]; 
                // Check if the data contains any records
                if($data->total()){ 
                    // Success: Data is available and returned to the user
                    return response( 
                        new BaseResource( 
                            true, 
                            $this->title . ' - Data successfully found.', 
                            $datas 
                        ), 200); 
                } 
                // No records found: Return a clean 'not found' response
                return response( 
                    new BaseResource( 
                        false, 
                        $this->title . ' - No data found.', 
                        $datas 
                    ), 404); 
            }else{ 
                // Edge case: Data is null or an invalid request was made
                return response( 
                    new BaseResource(false, $this->title . ' - No data available. Please verify your query.', [] 
                ), 404); 
            } 
            //-----------------------------------------------
        } catch (\Exception $e) {
            // Handle any errors during retrieval
            return response(
                new BaseResource(false, "An error occurred while retrieving data: (" . $e->getMessage() . ")")
            , 442);
        }
    } 
    //end_table-------------------------------------------------------


    //list with search functionality-----------------------------------
    public function search(Request $request){
        // Retrieve a list of all data with "id" as value and "name" as label.
        // Allows filtering with a search query using the LIKE operator.
        // If the "name" field is unavailable, it will use the second column after "id".
        try {
            // Get search parameter from the request
            //-----------------------------------------------
            if($request->filled("q")){ 
                //-----------------------------------------------
                $search = $request->get("q");
                $record = $this->model->select("id", "id_transaksi")
                    ->when($search, function ($query) use ($search) {
                        $query->where("id_transaksi", "LIKE", "%" . $search . "%");
                    })->get();
                //-----------------------------------------------
                if ($record->count() < 1) {
                    return response(
                        new BaseResource(false, "No matching data found"),
                        404
                    );
                }
                //-----------------------------------------------

                // Map the data to a key-value structure (value = id, name = name)
                //-----------------------------------------------
                $data = $record->map(function ($item) {
                    return [
                        "value" => $item->id,
                        "name"  => $item->id_transaksi ?? "Unnamed"
                    ];
                });
                //-----------------------------------------------

                // Return the mapped data as a successful response
                //-----------------------------------------------
                return response(
                    new BaseResource(true, "Data retrieved successfully", $data),
                    200
                );
            }
            //-----------------------------------------------
            return response(
                new BaseResource(false, "Please provide the query first!!!"),
                442
            );
            //-----------------------------------------------
        } catch (\Exception $e) {
            // Handle any exceptions that occur during the process
            //-----------------------------------------------
            return response(
                new BaseResource(false, "An error occurred while retrieving data: (" . $e->getMessage() . ")"),
                442
            );
        }
    }
    //end_list with search functionality-------------------------------


    //list---------------------------------------------------
    public function list(){
        // Retrieve a list of all data with "id" as value and "name" as label.
        // If the "name" or "nama" field is unavailable, it will use the second column after "id".
        try {
            // Query the database to select "id" and the appropriate name field
            //-----------------------------------------------
            $record = $this->model->select("id", "id_transaksi")->get();
            //-----------------------------------------------
            // Check if any records are found
            if ($record->count() < 1) {
                return response(
                    new BaseResource(false, "Data not found"),
                    404
                );
            }
            //-----------------------------------------------

            // Map the data to a key-value structure (value = id, name = name)
            //-----------------------------------------------
            $data = $record->map(function ($item) {
                return [
                    "value" => $item->id,
                    "name"  => $item->id_transaksi ?? "Unnamed"
                ];
            });
            //-----------------------------------------------
            // Return the mapped data as a successful response
            return response(
                new BaseResource(true, "Data retrieved successfully", $data),
                200
            );
        } catch (\Exception $e) {
            // Handle any exceptions that occur during the process
            //-----------------------------------------------
            return response(
                new BaseResource(false, "An error occurred while retrieving data: (" . $e->getMessage() . ")"),
                442
            );
        }
    }
    //end_list-----------------------------------------------


    //show---------------------------------------------------
    public function show($id){
        try {
            // Find the record by ID
            //-----------------------------------------------
            $record = $this->model->find($id);
            if (!$record) {
                return response(
                    new BaseResource(false, "Data not found for ID: " . $id),
                    404
                );
            }
            //-----------------------------------------------

            // Return the record directly
            //-----------------------------------------------
            return response(
                new BaseResource(true, "Data successfully retrieved.", $this->res->make($record) )
            , 200);
            //-----------------------------------------------
        } catch (\Exception $e) {
            // Handle any errors during retrieval
            return response(
                new BaseResource(false, "An error occurred while retrieving data: (" . $e->getMessage() . ")")
            , 442);
        }
    }
    //end_show-----------------------------------------------


    //create-------------------------------------------------
    public function create(Request $request){
        try {
            //validation input
            //-----------------------------------------------
            $validator = Validator::make($request->all(), $this->getValidationRules() ); 
            if ($validator->fails()) { 
                return response( 
                    new BaseResource(false, 
                        $this->title . " => Input error occurred!!, while adding data", 
                        [], $validator->errors()
                ), 442); 
            } 
            //-----------------------------------------------

            //add new data
            //-----------------------------------------------
            $record = $this->model->create($request->all());
            if(!$record){
                return response(new BaseResource(false, "Failed to create data."), 442);
            }
            return response(new BaseResource(true, "Data created successfully.", $this->res->make($record) ), 200);
            //-----------------------------------------------
        } catch (\Exception $e) {
            // Handle any errors during retrieval
            return response(
                new BaseResource(false, "An error occurred while creating data: (" . $e->getMessage() . ")")
            , 442);
        }
    }
    //end_create---------------------------------------------


    //update-------------------------------------------------
    public function update(Request $request, $id){
        try {
            // Find the record by ID
            $record = $this->model->find($id);
            if (!$record) {
                return response(
                    new BaseResource(false, "Data not found for ID: " . $id),
                    404
                );
            }
            //-----------------------------------------------
            
            //validation input
            //-----------------------------------------------
            $validator = Validator::make($request->all(), $this->getValidationRules($id) ); 
            if ($validator->fails()) { 
                return response( 
                    new BaseResource(false, 
                        $this->title . " => Input error occurred!!, while adding data", 
                        [], $validator->errors()
                ), 442); 
            } 
            //-----------------------------------------------

            //update data
            //-----------------------------------------------
            if(!$record->update($request->all()) ){
                return response(new BaseResource(false, "Failed to update data."), 442);
            }
            return response(new BaseResource(true, "Data updated successfully.", $this->res->make($record) ), 200);
            //-----------------------------------------------
        } catch (\Exception $e) {
            // Handle any errors during retrieval
            return response(
                new BaseResource(false, "An error occurred while updating data: (" . $e->getMessage() . ")")
            , 442);
        }
    }
    //end_update---------------------------------------------


    //delete-------------------------------------------------
    public function delete($id){
        try {
            // Find the record by ID
            //-----------------------------------------------
            $record = $this->model->find($id);
            if (!$record) {
                return response(
                    new BaseResource(false, "Data not found for ID: " . $id),
                    404
                );
            }
            //-----------------------------------------------

            // Attempt to delete the record
            //-----------------------------------------------
            if ($record->delete()) {
                // Return success response
                return response(
                    new BaseResource(true, "Data successfully deleted.")
                , 200);
            } else {
                // Return failure response if delete failed
                return response(
                    new BaseResource(false, "Failed to delete the data.")
                , 500);
            }
            //-----------------------------------------------
        } catch (\Exception $e) {
            // Handle any errors during deletion
            return response(
                new BaseResource(false, "An error occurred while deleting data: (" . $e->getMessage() . ")")
            , 442);
        }
    }
    //end_delete---------------------------------------------


} 
