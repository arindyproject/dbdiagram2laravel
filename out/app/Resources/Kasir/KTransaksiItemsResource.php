<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Http\Resources\Kasir; 
use Illuminate\Http\Request; 
use Illuminate\Http\Resources\Json\JsonResource; 

Class KTransaksiItemsResource extends JsonResource { 
    /**
    * Transform the resource into an array.
    *
    * @return array<string, mixed>
    */
    public function toArray($request){
        return[
            "id"           => $this->id, 
            "id_transaksi" => $this->id_transaksi, 
            "id_produk"    => $this->id_produk, 
            "jumlah"       => $this->jumlah, 
            "harga"        => $this->harga, 
            "created_at"   => $this->created_at, 
            "updated_at"   => $this->updated_at, 
        ]; 
    } 
} 
