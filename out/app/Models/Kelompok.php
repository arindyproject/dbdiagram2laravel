<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Models; 
use Illuminate\Database\Eloquent\Factories\HasFactory; 
use Illuminate\Database\Eloquent\Model; 
Class Kelompok extends Model { 
    use HasFactory; 
    protected $table = 'kelompok'; 
    protected $fillable = [ 
        "id", 
        "id_user", 
        "id_jenis", 
    ]; 
kelompok > users 
jenis < kelompok 
} 
