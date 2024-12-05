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
            "transaksi"    => $this->id_transaksi ? [ "id" => $this->transaksi->id ,  ] : [], 
            "produk"       => $this->id_produk ? [ "id" => $this->produk->id , "name" => $this->produk->name ] : [], 
            "jumlah"       => $this->jumlah, 
            "harga"        => $this->harga, 
            "created_at"   => $this->created_at ? $this->created_at->format("Y-m-d h:i:s") : "", 
            "updated_at"   => $this->updated_at ? $this->updated_at->format("Y-m-d h:i:s") : "", 
        ]; 
    } 
} 
