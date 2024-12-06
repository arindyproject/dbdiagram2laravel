<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Http\Controllers\API\Kasir; 

use App\Http\Controllers\Controller; 
use Illuminate\Http\Request; 
use Illuminate\Support\Facades\Auth; 
use Illuminate\Support\Facades\Validator; 
 
use App\Http\Resources\BaseResource; 
use App\Http\Resources\Kasir\KJenisResources; 
use App\Models\Kasir\KJenis; 
 
Class KJenisController extends Controller { 
    //construct----------------------------------------------
    public function __construct(){
        $this->model = new KJenis;
        $this->res   = new KJenisResources(null);
    }
    //end_construct------------------------------------------


    //list---------------------------------------------------
    public function list(){
    }
    //end_list-----------------------------------------------


    //show---------------------------------------------------
    public function show($id){
    }
    //end_show-----------------------------------------------


    //create-------------------------------------------------
    public function create(Request $request){
    }
    //end_create---------------------------------------------


    //update-------------------------------------------------
    public function update(Request $request, $id){
    }
    //end_update---------------------------------------------


    //delete-------------------------------------------------
    public function delete($id){
    }
    //end_delete---------------------------------------------


} 
