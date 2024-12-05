<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Models\Kasir; 
use Illuminate\Database\Eloquent\Factories\HasFactory; 
use Illuminate\Database\Eloquent\Model; 
use Illuminate\Database\Eloquent\Relations\HasOne; 
use Illuminate\Database\Eloquent\Relations\BelongsTo; 
use Illuminate\Database\Eloquent\Relations\HasMany; 

Class KTransaksi extends Model { 
    use HasFactory; 
    protected $table = 'k_transaksi'; 
    protected $fillable = [ 
        "id", 
        "id_customer", 
        "id_kasir", 
    ]; 

    //k_customer < k_transaksi 
    public function customer(): belongsTo { 
        return $this->belongsTo('App\Models\Kasir\KCustomer' ,'id_customer');
    }

    //users < k_transaksi 
    public function kasir(): belongsTo { 
        return $this->belongsTo('App\Models\User' ,'id_kasir');
    }

    //k_transaksi < k_transaksi_items 
    public function k_transaksi_items(): hasMany { 
        return $this->hasMany('App\Models\Kasir\KTransaksiItems' ,'id_transaksi');
    }

} 
