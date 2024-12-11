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


    //list---------------------------------------------------
    public function list(){
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
        } catch (Exception $e) {
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
        } catch (Exception $e) {
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
        } catch (Exception $e) {
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
        } catch (Exception $e) {
            // Handle any errors during deletion
            return response(
                new BaseResource(false, "An error occurred while deleting data: (" . $e->getMessage() . ")")
            , 442);
        }
    }
    //end_delete---------------------------------------------


} 
