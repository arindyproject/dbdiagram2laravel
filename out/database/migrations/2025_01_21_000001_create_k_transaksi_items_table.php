<?php 
//Generated by ArindyProject -> https://github.com/arindyproject/dbdiagram2laravel 
use Illuminate\Database\Migrations\Migration; 
use Illuminate\Database\Schema\Blueprint; 
use Illuminate\Support\Facades\Schema; 
return new class extends Migration{ 
    /** 
    * Run the migrations. 
    */ 
    public function up(): void { 
        Schema::create('k_transaksi_items', function (Blueprint $table) { 
            $table->id(); 
            //-------------------------------------------------------
            $table->unsignedBigInteger('id_transaksi'); 
            $table->unsignedBigInteger('id_produk'); 
            $table->integer('jumlah'); 
            $table->decimal('harga' ,10,2); 
            //-------------------------------------------------------
            $table->foreign('id_produk')->references('id')->on('k_produk')->onDelete('cascade');
            $table->foreign('id_transaksi')->references('id')->on('k_transaksi')->onDelete('cascade');
            //-------------------------------------------------------
            $table->timestamps(); 
        });
    } 

    /** 
    * Reverse the migrations. 
    */ 
    public function down(): void { 
        Schema::dropIfExists('k_transaksi_items'); 
    } 
};
