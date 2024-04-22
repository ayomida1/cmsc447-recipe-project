import datetime
import io
import json
from typing import Any, List

from rich import box
from rich.console import Console
from rich.table import Table

from .models import Grade


def render(result: Any, output_format: str = "text") -> str:
    """Render the result in the specified format."""
    if output_format == "text":
        return str(result)
    elif output_format == "json":
        return result.json()
    elif output_format == "ndjson":
        return result.ndjson()
    else:
        raise ValueError("Unknown format: " + output_format)


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder for object containing datetime values."""

    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class GradesListResult:
    def __init__(self, grades: List[Grade]) -> None:
        self.grades = grades

    def __str__(self) -> str:
        table = Table(title="Grades", box=box.SIMPLE)
        table.add_column("Data")
        table.add_column("Materia")
        table.add_column("Tipo")
        table.add_column("Voto")
        table.add_column("Commento")
        table.add_column("Docente")

        for g in self.grades:
            table.add_row(
                str(g.date.strftime("%Y-%m-%d")),
                str(g.subject),
                str(g.kind),
                str(g.value),
                str(g.comment),
                str(g.teacher),
            )

        # we capture the output into this variable
        output = io.StringIO()

        # turn table into a string using the Console
        console = Console(file=output)
        console.print(table)

        return output.getvalue()

    def json(self) -> str:
        return json.dumps(
            [g.__dict__ for g in self.grades], cls=DateTimeEncoder
        )

    def ndjson(self) -> str:
        return "\n".join(
            [json.dumps(g.__dict__, cls=DateTimeEncoder) for g in self.grades],
        )
