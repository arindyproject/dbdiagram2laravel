<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
namespace App\Models; 
use Illuminate\Database\Eloquent\Factories\HasFactory; 
use Illuminate\Database\Eloquent\Model; 
use Illuminate\Database\Eloquent\Relations\HasOne; 
use Illuminate\Database\Eloquent\Relations\BelongsTo; 
use Illuminate\Database\Eloquent\Relations\HasMany; 

Class Kelamin extends Model { 
    use HasFactory; 
    protected $table = 'kelamin'; 
    protected $fillable = [ 
        "id", 
        "name", 
    ]; 

    //kelamin < users 
    public function users(): hasMany { 
        return $this->hasMany(Users::class );
    }

} 
