from pydantic import BaseModel


class Column(BaseModel):
    name: str
    type: str = ""
    is_primary_key: bool = False
    references: str | None = None  # "table.column"


class Table(BaseModel):
    name: str
    columns: list[Column]


class DatabaseSchema(BaseModel):
    tables: list[Table]

    def table_names(self) -> set[str]:
        return {t.name.lower() for t in self.tables}

    def columns_of(self, table: str) -> set[str]:
        for t in self.tables:
            if t.name.lower() == table.lower():
                return {c.name.lower() for c in t.columns}
        return set()

    def to_prompt(self) -> str:
        lines: list[str] = []
        for t in self.tables:
            lines.append(f"TABLE {t.name}")
            for c in t.columns:
                tags = []
                if c.is_primary_key:
                    tags.append("PK")
                if c.references:
                    tags.append(f"FK -> {c.references}")
                lines.append(f"  - {c.name} {c.type} {' '.join(tags)}".rstrip())
        return "\n".join(lines)
