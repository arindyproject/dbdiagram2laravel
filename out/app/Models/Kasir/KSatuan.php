<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Models\Kasir; 

use Illuminate\Database\Eloquent\Factories\HasFactory; 
use Illuminate\Database\Eloquent\Model; 
use Illuminate\Database\Eloquent\Relations\HasOne; 
use Illuminate\Database\Eloquent\Relations\BelongsTo; 
use Illuminate\Database\Eloquent\Relations\HasMany; 

Class KSatuan extends Model { 
    use HasFactory; 
    protected $table = 'k_satuan'; 
    protected $fillable = [ 
        "id", 
        "name", 
        "id_author", 
    ]; 

    //users < k_satuan 
    public function author(): belongsTo { 
        return $this->belongsTo('App\Models\User' ,'id_author');
    }

    //k_satuan < k_produk 
    public function k_produk(): hasMany { 
        return $this->hasMany('App\Models\Kasir\KProduk' ,'id_satuan');
    }

} 
