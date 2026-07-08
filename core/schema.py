"""
Schema discovery classes.

Reads the SQLite schema once when the application starts.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from typing import Dict, List, Optional

from core.database import DatabaseManager


# -------------------------------------------------------
# Column
# -------------------------------------------------------

@dataclass
class ColumnInfo:

    cid: int

    name: str

    datatype: str

    notnull: bool

    default: object

    primary_key: bool


# -------------------------------------------------------
# Foreign Key
# -------------------------------------------------------

@dataclass
class ForeignKeyInfo:

    table: str

    from_column: str

    to_column: str


# -------------------------------------------------------
# Table
# -------------------------------------------------------

@dataclass
class TableInfo:

    name: str

    columns: List[ColumnInfo] = field(default_factory=list)

    foreign_keys: List[ForeignKeyInfo] = field(default_factory=list)

    primary_key: Optional[str] = None

    row_count: int = 0


# -------------------------------------------------------
# Schema Manager
# -------------------------------------------------------

class SchemaManager:

    """
    Discovers the complete SQLite schema.

    This class should be instantiated once when the
    application starts.
    """

    def __init__(self, db: DatabaseManager):

        self.db = db

        self.tables: Dict[str, TableInfo] = {}

    # ----------------------------------------------

    def load(self):

        """
        Read every table.
        """

        self.tables.clear()

        for table_name in self.db.tables():

            table = TableInfo(table_name)

            # -----------------------
            # Columns
            # -----------------------

            for column in self.db.columns(table_name):

                info = ColumnInfo(

                    cid=column["cid"],

                    name=column["name"],

                    datatype=column["type"],

                    notnull=bool(column["notnull"]),

                    default=column["dflt_value"],

                    primary_key=bool(column["pk"])

                )

                table.columns.append(info)

                if info.primary_key:

                    table.primary_key = info.name

            # -----------------------
            # Foreign Keys
            # -----------------------

            for fk in self.db.foreign_keys(table_name):

                table.foreign_keys.append(

                    ForeignKeyInfo(

                        table=fk["table"],

                        from_column=fk["from"],

                        to_column=fk["to"]

                    )

                )

            table.row_count = self.db.count(table_name)

            self.tables[table_name] = table

    # ----------------------------------------------

    def get_table(self, name):

        return self.tables[name]

    # ----------------------------------------------

    def get_tables(self):

        return list(self.tables.values())

    # ----------------------------------------------

    def column(self, table, column):

        for c in self.tables[table].columns:

            if c.name == column:

                return c

        return None

    # ----------------------------------------------

    def primary_key(self, table):

        return self.tables[table].primary_key

    # ----------------------------------------------

    def relationships(self, table):

        return self.tables[table].foreign_keys

    # ----------------------------------------------

    def dump(self):

        """
        Print schema to console.
        """

        for table in self.tables.values():

            print()

            print(table.name)

            print("-" * len(table.name))

            print()

            for column in table.columns:

                pk = " PK" if column.primary_key else ""

                print(

                    f"{column.name:<20}"

                    f"{column.datatype:<12}"

                    f"{pk}"

                )

            if table.foreign_keys:

                print()

                print("Foreign Keys")

                print()

                for fk in table.foreign_keys:

                    print(

                        f"{fk.from_column}"

                        f" -> "

                        f"{fk.table}.{fk.to_column}"

                    )

            print()

            print(

                f"Rows : {table.row_count}"

            )