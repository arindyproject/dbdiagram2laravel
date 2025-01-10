# ArindyProject  
**dbdiagram.io TO Laravel**  

This application converts **dbdiagram.io** formats into Laravel-compatible files such as:  
- **Controllers**  
- **Models**  
- **Resources**  
- **Routes**  
- **SQL**  

## Detailed Options  
| Option          | Description                                      |
|-----------------|--------------------------------------------------|
| **-i / --input**| Input file from dbdiagram .txt.                  |
| **-m / --mode** | Mode of operation.                               |
|                 | **Modes:**                                       |
|                 | - `mysql/sql`  -> Generate SQL file              |
|                 | - `migrate`    -> Generate Laravel migration     |
|                 | - `controller` -> Generate Laravel Controller    |
|                 | - `model`      -> Generate Laravel Model         |
|                 | - `res`        -> Generate Laravel Resources     |
|                 | - `route`      -> Generate Laravel Route         |
|                 | - `all`        -> Generate ALL Modes             |
| **-e / --exc**  | Exclude columns from generation.                 |
| **-d / --dir**  | Optional, to place files in additional folders specifically for Routes and Controllers |

## How to Use this Generator
- **Please design your database first at dbdiagram.io**
- **Copy the code from dbdiagram, then save it to a new file, for example: input.txt**

## Example Input File from dbdiagram.io
***Here is an example of writing a table from dbdiagram.io***

[An Example Dbdiagram](https://dbdocs.io/datakitaya/ArindyProject-Kasir-Test)
```bash
Table users{
  id bigint [pk, increment]
  name varchar
  alamat text [null]
  id_kelamin bigint [null]
}

Table k_produk{
  //dir: Kasir
  id bigint [pk, increment]
  name varchar  [not null]
  keterangan text
  harga decimal(10,2) 
  diskon decimal(5,2)
  ppn decimal(5,2) [default: 11.0]
  id_jenis bigint
  id_satuan bigint
  id_author bigint 
  created_at timestamp [null, default: null]
  updated_at timestamp [null, default: null]
}
```
**The following is the description**

- ***//dir: Kasir*** is an additional folder that will later be used to store controller files, models, and resources. "Kasir" is the folder name, you can replace it with what you want.

- ***created_at timestamp [null, default: null]*** is a customized code addition for Laravel
- ***updated_at timestamp [null, default: null]*** is a customized code addition for Laravel
- ***id_author, id_jenis, and id_satuan*** is a way of writing for relations between tables or writing foreign keys. The writing must be "id_namefiled" or "namefiled_id".

**This is Writing to Connect Between Tables**

supporting writing marks
- ***>*** : many-to-one
- ***<*** : one-to-many
- ***-*** : one-to-one

***How ​​to write correctly:***
```bash
Ref: "users"."id" < "k_jenis"."id_author" [delete: set null]
Ref: "users"."id" < "k_produk"."id_author" [delete: set null]
Ref: "k_customer"."id" - "k_kartu"."id_user" [delete: cascade]
```

***Incorrect Spelling:***
```bash
Ref: users.id < k_jenis.id_author [delete: set null]
Ref: users.id < k_produk.id_author [delete: set null]
Ref: k_customer.id - k_kartu.id_user [delete: cascade]
```

## Example Commands  
How to Use It:
- ***input.txt*** is the code from dbdiagram.io
- ***-m / --mode*** is the choice of what code file we will create. for example "model" to create a Model or "all" to create all existing modes.
```bash
python main.py -i input.txt -m model
python main.py -i input.txt -m all
```

for example if you don't want to generate from a table, you can use ***-e / --exc*** for example ***-e user*** then the user table will not be generated.
```bash
python main.py -i input.txt -m all -e user
```

Suppose you want to add an additional folder to store your files you can use ***-d / --dir*** example ***-d v2***. this function only applies to controllers and routes only. and in routes then your link also has an addition for example: "*/v2/*".
```bash
python main.py -i input.txt -m all -e user -d v2
```

## Results From Generate
The output results are in the **out** folder