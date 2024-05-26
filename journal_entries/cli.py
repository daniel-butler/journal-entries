"""
The entrypoint for the CLI application.
It handles converting the CLI inputs into the main function's parameters.
"""
from pathlib import Path
from datetime import datetime
from typing import Annotated

import typer
from typer import Typer

from .main import main, SAVE_LOCATION
from .constants import (
    Department, Market, ENTITIES, ALLOWED_INPUT_VERSIONS, ALLOWED_OUTPUT_VERSIONS
)
app = Typer()


def is_valid_entity(value: str) -> str:
    if value not in ENTITIES:
        raise ValueError(f"Invalid entity {value}.")
    return value


def is_valid_department(value: str) -> str:
    if value not in Department.__members__:
        raise ValueError(f"Invalid department {value}.")
    return Department[value]


def is_valid_market(value: str) -> str:
    if value not in Market.__members__:
        raise ValueError(f"Invalid market {value}.")
    return Market[value]


def is_valid_input_version(value: str) -> str:
    if value not in ALLOWED_INPUT_VERSIONS.keys():
        raise ValueError(f"Invalid input version {value}.")
    return value


def is_valid_output_version(value: str) -> str:
    if value not in ALLOWED_OUTPUT_VERSIONS.keys():
        raise ValueError(f"Invalid output version {value}.")
    return value


@app.command()
def journal_entry(
        import_file: Annotated[Path, typer.Option(help="The path to the statement file", prompt=True)],
        client_code: Annotated[str, typer.Option(help="The client/customer code", prompt=True)],
        deposit_entity: Annotated[str, typer.Option(callback=is_valid_entity, prompt=True)],
        posting_date: Annotated[datetime, typer.Option(help="The journal entry posting date", prompt=True)],
        document_date: Annotated[datetime, typer.Option(help="The statement's date", prompt=True)],
        payment_number: Annotated[
            str, typer.Option(
                help="The Payment's reference number. Normally the check number or EFT date.",
                prompt=True
            )
        ],
        applies_to_type: Annotated[str, typer.Option(help="The type of payment", prompt=True)],
        department: Annotated[str, typer.Option(callback=is_valid_department, prompt=True)],
        market: Annotated[str, typer.Option(callback=is_valid_market, prompt=True)],
        state: Annotated[str, typer.Option(help="The state the statement is for", prompt=True)],
        division: Annotated[str, typer.Option(help="The division the statement is for", prompt=True)],
        statement_identifier: Annotated[str, typer.Option(help="The statement identifier", prompt=True)],
        save_location: Path = SAVE_LOCATION,

        # Only if versioning is required
        import_input_version: Annotated[str, typer.Option(callback=is_valid_input_version, prompt=True)] = 'V1',
        import_output_version: Annotated[str, typer.Option(callback=is_valid_output_version, prompt=True)] = 'V1',
):
    """
    Generate the journal entries for a statement.
    """

    main(
        import_file=import_file,
        client_code=client_code,
        deposit_entity=ENTITIES.get(deposit_entity),
        posting_date=posting_date.date(),
        document_date=document_date.date(),
        payment_number=payment_number,
        applies_to_type=applies_to_type,
        department=Department[department],
        market=Market[market],
        state=state,
        division=division,
        statement_identifier=statement_identifier,
        save_location=save_location,
        import_input_version=import_input_version,
        import_output_version=import_output_version,
    )
