<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Models\Kasir; 
use Illuminate\Database\Eloquent\Factories\HasFactory; 
use Illuminate\Database\Eloquent\Model; 
use Illuminate\Database\Eloquent\Relations\HasOne; 
use Illuminate\Database\Eloquent\Relations\BelongsTo; 
use Illuminate\Database\Eloquent\Relations\HasMany; 

Class KProduk extends Model { 
    use HasFactory; 
    protected $table = 'k_produk'; 
    protected $fillable = [ 
        "id", 
        "name", 
        "keterangan", 
        "harga", 
        "diskon", 
        "ppn", 
        "id_jenis", 
        "id_satuan", 
        "id_author", 
        "created_at", 
        "updated_at", 
    ]; 

    //users < k_produk 
    public function author(): belongsTo { 
        return $this->belongsTo('App\Models\User' ,'id_author');
    }

    //k_jenis < k_produk 
    public function jenis(): belongsTo { 
        return $this->belongsTo('App\Models\KJenis' ,'id_jenis');
    }

    //k_satuan < k_produk 
    public function satuan(): belongsTo { 
        return $this->belongsTo('App\Models\KSatuan' ,'id_satuan');
    }

    //k_produk < k_transaksi_items 
    public function k_transaksi_items(): hasMany { 
        return $this->hasMany('App\Models\Kasir\KTransaksiItems' ,'id_produk');
    }

} 
