<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Http\Resources\Kasir; 
use Illuminate\Http\Request; 
use Illuminate\Http\Resources\Json\JsonResource; 

Class KProdukResource extends JsonResource { 
    /**
    * Transform the resource into an array.
    *
    * @return array<string, mixed>
    */
    public function toArray($request){
        return[
            "id"         => $this->id, 
            "name"       => $this->name, 
            "keterangan" => $this->keterangan, 
            "harga"      => $this->harga, 
            "diskon"     => $this->diskon, 
            "ppn"        => $this->ppn, 
            "id_jenis"   => $this->id_jenis, 
            "id_satuan"  => $this->id_satuan, 
            "id_author"  => $this->id_author, 
            "created_at" => $this->created_at, 
            "updated_at" => $this->updated_at, 
        ]; 
    } 
} 
