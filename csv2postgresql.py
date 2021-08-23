#!/usr/bin/env python3

import argparse
import csv
import locale
import sys

from psycopg2 import connect, sql


def main(input_file, dsn, table, delimiter, quotechar, escapechar, encoding):
    with connect(dsn) as conn:
        with conn.cursor() as cur:
            reader = csv.reader(input_file, delimiter=delimiter)
            header = next(reader)
            options = [
                sql.SQL(k + " ") + sql.Identifier(v)
                for k, v in {
                    "delimiter": reader.dialect.delimiter,
                    "quote": reader.dialect.quotechar,
                    "escape": reader.dialect.escapechar,
                    "encoding": input_file.encoding,
                }.items()
                if v
            ]
            query = sql.SQL(
                """
                copy {table} ({columns})
                from stdin
                with (format csv,
                     {options})
            """
            ).format(
                table=sql.Identifier(table),
                columns=sql.SQL(", ").join(
                    [sql.Identifier(c) for c in header]
                ),
                options=sql.SQL(", ").join(options),
            )
            cur.copy_expert(query, sys.stdin)


def cli():
    parser = argparse.ArgumentParser(
        description="Load CSV with header into PostgreSQL"
    )
    parser.add_argument("dsn")
    parser.add_argument("table")
    parser.add_argument(
        "--input-file",
        "-i",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Input file name containing a valid CSV.",
    )
    parser.add_argument("--delimiter", "-d", default=",")
    parser.add_argument("--quotechar", default='"')
    parser.add_argument("--escapechar", default=None)
    parser.add_argument(
        "--encoding", "-e", default=locale.getpreferredencoding()
    )
    args = parser.parse_args()
    args.input_file.reconfigure(encoding=args.input_file.encoding)
    main(**vars(args))


if __name__ == "__main__":
    cli()
