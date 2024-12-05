<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Models\Kasir; 

use Illuminate\Database\Eloquent\Factories\HasFactory; 
use Illuminate\Database\Eloquent\Model; 
use Illuminate\Database\Eloquent\Relations\HasOne; 
use Illuminate\Database\Eloquent\Relations\BelongsTo; 
use Illuminate\Database\Eloquent\Relations\HasMany; 

Class KTransaksiItems extends Model { 
    use HasFactory; 
    protected $table = 'k_transaksi_items'; 
    protected $fillable = [ 
        "id", 
        "id_transaksi", 
        "id_produk", 
        "jumlah", 
        "harga", 
    ]; 

    //k_produk < k_transaksi_items 
    public function produk(): belongsTo { 
        return $this->belongsTo('App\Models\Kasir\KProduk' ,'id_produk');
    }

    //k_transaksi < k_transaksi_items 
    public function transaksi(): belongsTo { 
        return $this->belongsTo('App\Models\Kasir\KTransaksi' ,'id_transaksi');
    }

} 
