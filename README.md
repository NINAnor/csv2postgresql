# Description

csv2postgresql imports data from a CSV file into PostgreSQL.

It differs from PostgreSQL `COPY FROM ... WITH (FORMAT CSV ...)` command as it
detects automatically the CSV columns available, so even CSV files with missing
columns or having columns arranged in a different order can be easily imported.

# Setup

The software can be installed using `pip` or `pipx`, which is preferred.

```
pipx install csv2postgresql
```

# Help

```
$ csv2postgresql --help
usage: csv2postgresql [-h] [--input-file INPUT_FILE] [--delimiter DELIMITER] [--quotechar QUOTECHAR]
                      [--escapechar ESCAPECHAR] [--encoding ENCODING]
                      dsn table

Load CSV with header into PostgreSQL

positional arguments:
  dsn
  table

optional arguments:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE, -i INPUT_FILE
                        Input file name containing a valid CSV.
  --delimiter DELIMITER, -d DELIMITER
  --quotechar QUOTECHAR
  --escapechar ESCAPECHAR
  --encoding ENCODING, -e ENCODING
```

# Example

```
csv2postgresql -i table.csv postgresql://user:password@localhost/db table
```