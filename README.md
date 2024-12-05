# ArindyProject  
**dbdiagram.io TO Laravel**  

This application converts **dbdiagram.io** formats into Laravel-compatible files such as:  
- **Models**  
- **Resources**  
- **SQL**  

## Detailed Options  
| Option         | Description                                      |
|-----------------|--------------------------------------------------|
| **-i / --input** | Input file from dbdiagram .txt.                 |
| **-m / --mode**  | Mode of operation.                              |
|                 | **Modes:**                                       |
|                 | - `mysql/sql`  -> Generate SQL file              |
|                 | - `migrate`    -> Generate Laravel migration     |
|                 | - `model`      -> Generate Laravel Model         |
|                 | - `res`        -> Generate Laravel Resources     |
|                 | - `all`        -> Generate ALL Modes             |
| **-e / --exc**   | Exclude columns from generation.                |
|                 | Applies to Models and Resources.                |

## Example Commands  
Using the input file `dbdiagram.txt` and `model` mode:  
```bash
python main.py -i dbdiagram.txt -m model