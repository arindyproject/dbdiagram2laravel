<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Http\Resources\Kasir; 

use Illuminate\Http\Request; 
use Illuminate\Http\Resources\Json\JsonResource; 

Class KCustomerResource extends JsonResource { 
    /**
    * Transform the resource into an array.
    *
    * @return array<string, mixed>
    */
    public function toArray($request){
        return[
            "id"         => $this->id, 
            "name"       => $this->name, 
            "alamat"     => $this->alamat, 
            "no_tlp"     => $this->no_tlp, 
            "author"     => $this->id_author ? [ "id" => $this->author->id , "name" => $this->author->name ] : [], 
            "created_at" => $this->created_at ? $this->created_at->format("Y-m-d h:i") : "", 
            "updated_at" => $this->updated_at ? $this->updated_at->format("Y-m-d h:i") : "", 
        ]; 
    } 
} 
