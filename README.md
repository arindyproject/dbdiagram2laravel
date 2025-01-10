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
| **-e / --exc**  | Exclude columns from generation.  Applies to Models and Resources.|
| **-d / --dir**  | Optional, to place files in additional folders specifically for Routes and Controllers |

## How to Use this Generator
- **Please design your database first at dbdiagram.io**
- **Copy the code from dbdiagram, then save it to a new file, for example: input.txt**

## Example Input File from dbdiagram.io
Here is an example of writing a table from dbdiagram.io
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
- ***id_author, id_jenis, and id_satuan***

## Example Commands  
Using the input file `dbdiagram.txt` and `model` mode:  
```bash
python main.py -i dbdiagram.txt -m model