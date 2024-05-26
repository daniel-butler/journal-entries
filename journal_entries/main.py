from pathlib import Path
from typing import Union

from attrs import define, field, asdict

from datetime import date, datetime
from decimal import Decimal
import uuid

import pandas as pd

from .constants import INTERCOMPANY_GL_ASSET_ACCOUNT, EntryType, DocumentType, \
    INTERCOMPANY_GL_LIABILITY_ACCOUNT, Department, Market, ENTITIES, Entity
from .exceptions import JournalEntryInvalid

SAVE_LOCATION = Path(__file__).parent  # Same folder as the script


def main(
        import_file: Path,
        client_code: str,
        deposit_entity: Entity,
        posting_date: date,
        document_date: date,
        payment_number: str,
        applies_to_type: str,
        department: Department,
        market: Market,
        state: str,
        division: str,
        statement_identifier: str,
        save_location: Path = SAVE_LOCATION,

        # Only if versioning is required
        import_input_version: str = 'V1',
        import_output_version: str = 'V1',
):
    df = pd.read_excel(import_file)
    df.columns = df.columns.str.lower()  # Ensure all columns are lowercase to reduce mistakes
    lines = df.to_dict(orient='records')

    import_je = ImportEntries(
        lines=lines,
        posting_date=posting_date,
        statement_reference=statement_identifier,
        deposit_id=payment_number,
        deposit_document_type=applies_to_type,
        deposit_entity=deposit_entity,
        deposit_client_code=client_code,
        import_version=import_input_version,
        document_date=document_date,
        deposit_department=department,
        deposit_market=market,
        deposit_state=state,
        deposit_division=division,
    )
    import_je.create()
    save_import_jes(
        entries=import_je,
        save_location=save_location,
        version=import_output_version,
    )


@define
class JournalLine:
    """ Stores all the information for a single journal line in an entry.
    """

    account_type: EntryType
    account_number: str
    posting_date: date
    document_date: date
    document_no: str
    debit: Decimal
    description: str
    department: Department
    market: Market
    state: str
    division: str
    business_unit_code: int
    entry_entity: Entity
    salesperson_code: str | None = None
    client: str | None = None
    customer: str | None = None
    employee_ID: str | None = None
    expense_code: str | None = None
    vendor_dimension: str | None = None
    job_dimension: str | None = None
    document_type: DocumentType | None = None
    applies_to_document_number: str | None = None
    applies_to_document_type: DocumentType | None = None
    blank_field: str | None = None
    credit: Decimal = Decimal(0)
    reason_code: str = 'R10'


@define
class JournalEntry:
    """ Journal Entry comprises 2 or more journal lines that net to zero, and are in the same company
    with same document type and posting date.

    This designed, so it can be split out and used in other parts.
    """
    description: str
    posting_date: date
    identifier: Union[str, uuid.UUID]
    lines: list[JournalLine] = field(factory=list)

    @property
    def is_valid(self):
        return self.validate_lines_net_to_zero() \
            and self.validate_document_types_match() \
            and self.validate_lines_for_one_entity() \
            and self.validate_posting_date()

    def validate_posting_date(self):
        if self.lines[0].posting_date is None:
            raise JournalEntryInvalid('Missing Posting Date!')

        if self._check_equal([line.posting_date for line in self.lines]):
            return True
        else:
            raise JournalEntryInvalid(
                f'Journal Lines Posting Dates do not match!\n'
                f'Summary:\n{[(entry.account_number, entry.description, entry.posting_date) for entry in self.lines]}\n'
                f'Detail:\n{self.lines}')

    def validate_lines_net_to_zero(self):
        amount = 0
        for line in self.lines:
            amount += line.debit - line.credit
        if amount == 0:
            return True
        else:
            raise JournalEntryInvalid(
                f'Journal lines do not net to Zero. They Equal: {amount}\n'
                f'Summary:\n{[(entry.account_number, entry.description, entry.debit) for entry in self.lines]}\n'
                f'Details:\n{self.lines}'
            )

    def validate_document_types_match(self):
        """Validate Document Type is the same for all lines.
        Allowed Options:
            - None or ""
            - Payment
            - Invoice
            - Credit Memo
            - Finance Charge Memo
            - Reminder
            - Refund
        """
        if self._check_equal([line.document_type for line in self.lines]):
            return True
        else:
            raise JournalEntryInvalid('Journal Lines Document Types do not match!')

    def validate_lines_for_one_entity(self):
        if self.lines[0].entry_entity is None:
            raise JournalEntryInvalid('Missing Entry Entity!')

        if self._check_equal([line.entry_entity for line in self.lines]):
            return True
        else:
            raise JournalEntryInvalid(
                f'Journal Lines Entry Entity does not match!\n'
                f'Summary:\n{[(entry.account_number, entry.description, entry.entry_entity) for entry in self.lines]}\n'
                f'Detail:\n{self.lines}')

    @staticmethod
    def _check_equal(iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == rest for rest in iterator)


@define
class ImportEntries:
    """Interface for revenue and the interchangeable journal entry portion.

    This class handles making the specific journal entries for revenue statements and generates the specific reports
    required.
    """
    lines: list[dict]
    posting_date: date
    statement_reference: str
    deposit_id: str
    deposit_document_type: str
    deposit_entity: Entity
    deposit_client_code: str
    import_version: str
    document_date: date
    deposit_department: Department
    deposit_market: Market
    deposit_state: str
    deposit_division: str

    entries: list[JournalEntry] = field(factory=list)
    _statement_amount: Decimal | None = None
    entry_id: str | None = None
    _entity_and_amount: dict | None = None

    def __attrs_post_init__(self):
        """This function is ran after the object is created.
        It first validates the lines are for known entities.
        Then creates the entry_id and an entity_and_amount metadata dictionary we will use later.

        :return: None
        """
        self.entry_id = self.create_entry_id()
        self._entity_and_amount = dict()
        for line in self.lines:
            if entity := ENTITIES.get(line.get('entity')):
                line['entity'] = entity
            else:
                raise ValueError(f"Unknown Entity: {line.get('entity')}")

    def to_dataframe(self):
        """Turns the entries into a DataFrame that matches the general journal import V7 specification"""
        lines = list()
        for entry in self.entries:
            for line in entry.lines:
                d = asdict(line)
                d['entry_entity'] = line.entry_entity.abbreviation
                lines.append(d)
        df = pd.DataFrame(lines)
        df['posting_date'] = pd.to_datetime(df['posting_date'])
        df['document_date'] = pd.to_datetime(df['document_date'])
        return df[[
            'account_type', 'account_number', 'posting_date', 'document_date', 'blank_field', 'document_no', 'debit',
            'credit', 'description', 'department', 'market', 'salesperson_code', 'state', 'customer', 'division',
            'client', 'employee_ID', 'business_unit_code', 'reason_code', 'expense_code', 'vendor_dimension',
            'job_dimension', 'document_type', 'applies_to_document_type', 'applies_to_document_number', 'entry_entity',
        ]]

    @property
    def statement_amount(self) -> Decimal:
        """Calculate the total amount for the import. This can be thought of the total cash required to pay the batch.
        """
        if self._statement_amount is None:
            self._statement_amount = Decimal(0)
            for line in self.lines:
                self._statement_amount += Decimal(line['amount']).quantize(Decimal('1.00'))
        return Decimal(self._statement_amount)

    def create(self) -> None:
        """
        Create the journal entry for each of the specified entries below. The entries are then saved to the entries
        attribute as a list of entries.

        | Description | Debit | Credit |
        |-------------|-------|--------|
        | Make Intercompany Entries in other Entities | _Entry Entity_ : 12300 - Due to Related Entity | _Entry Entity_: 41000 - Commission |
        | Make Deposit Entry, Intercompany Entries to other Entities, and revenue entries | _Deposit Entity_ : P# - Client Card | _Deposit Entity_ : 22300 - Due from Related Entity  + _Entry Entity_ : 41000 - Commission |
        """
        self._intercompany_entries_to_deposit_entity_jes()
        self._deposit_entity_card_intercompany_and_revenue_je()

    def _intercompany_entries_to_deposit_entity_jes(self) -> None:
        """Loops through the entities and creates the intercompany entries for each entity to the main entity"""
        entities_and_amount = self.entities_and_amount
        for entity in entities_and_amount.keys():
            if entity != self.deposit_entity:
                entity_total_amount = entities_and_amount[entity].quantize(Decimal('1.00'))
                self._intercompany_to_deposit_entity_je(entity=entity, entity_total_amount=entity_total_amount)

    def _intercompany_to_deposit_entity_je(self, entity: Entity, entity_total_amount: Decimal) -> None:
        """
        | Description | Debit | Credit |
        |-------------|-------|--------|
        | Make Intercompany Entries in other Entities | _Entry Entity_ : 12300 - Due to Related Entity | _Entry Entity_: 41000 - Commission |

        """
        description = f'Revenue entry in entities other than deposit entity intercompanying back to deposit entity: ' \
                      f'{self.deposit_entity.abbreviation}'
        lines = [
            self._revenue_line(line=line, entry_entity=entity)
            for line in self.lines
            if line['entity'] == entity
        ]

        lines.append(self._intercompany_line_to_deposit_entity(entity=entity, total_amount=entity_total_amount))

        if lines:
            entry = JournalEntry(
                lines=lines,
                description=description,
                posting_date=self.posting_date,
                identifier=self.deposit_id
            )
            if entry.is_valid:
                self.entries.append(entry)

    def _deposit_entity_card_intercompany_and_revenue_je(self) -> None:
        """
        | Description | Debit | Credit |
        |-------------|-------|--------|
        | Make Deposit Entry, Intercompany Entries to other Entities, and revenue entries | _Deposit Entity_ : P# - Client Card | _Deposit Entity_ : 22300 - Due from Related Entity  + _Entry Entity_ : 41000 - Commission |
        """
        entities = self.entities_and_amount
        # create intercompany lines
        intercompany_lines = [
            JournalLine(
                account_type=EntryType.general_ledger,
                account_number=INTERCOMPANY_GL_LIABILITY_ACCOUNT,
                posting_date=self.posting_date,
                document_date=self.document_date,
                document_no=self.entry_id,
                # The below entry the balancing entry to the deposit entity.
                # This is required so that each entity's journal entry nets to zero.
                debit=Decimal(entities[entity]).quantize(Decimal('1.00')) * -1,
                description=f"{entity.abbreviation} - {self.lines[0]['description']}",
                department=Department.corporate,
                market=entity.major_market,
                state=entity.major_state,
                division=entity.major_division,
                business_unit_code=entity.business_unit,
                document_type=DocumentType.invoice,
                client=self.deposit_client_code,
                entry_entity=self.deposit_entity,
            )
            for entity in entities.keys()
            if entity != self.deposit_entity
        ]
        # Create deposit line in customer
        deposit_line = [JournalLine(
            account_type=EntryType.customer,
            account_number=self.deposit_client_code,
            posting_date=self.posting_date,
            document_date=self.document_date,
            document_no=self.entry_id,
            debit=Decimal(self.statement_amount).quantize(Decimal('1.00')),
            description=f"{self.lines[0]['description']}",
            department=self.deposit_department,
            market=self.deposit_market,
            state=self.deposit_state,
            division=self.deposit_division,
            business_unit_code=self.deposit_entity.business_unit,
            client=self.deposit_client_code,
            applies_to_document_type=DocumentType.payment,
            applies_to_document_number=self.deposit_id,
            document_type=DocumentType.invoice,
            entry_entity=self.deposit_entity,
        )]

        # Create revenue lines in the company
        revenue_lines = [
            self._revenue_line(line=line, entry_entity=self.deposit_entity)
            for line in self.lines
            if line['entity'] == self.deposit_entity
        ]

        # create description
        description = f'Created deposit line in {self.deposit_entity.abbreviation}'

        if revenue_lines:
            description += ' with revenue lines'

        if intercompany_lines:
            description += ' and intercompany lines'

        lines = deposit_line + revenue_lines + intercompany_lines
        entry = JournalEntry(
            lines=lines,
            description=description,
            posting_date=self.posting_date,
            identifier=self.deposit_id,
        )

        if entry.is_valid:
            self.entries.append(entry)

    def _revenue_line(self, line: dict, entry_entity: Entity) -> JournalLine:
        """Creates revenue lines"""
        description = line['description']
        if entry_entity != self.deposit_entity:
            description = f"{self.deposit_entity.abbreviation} - {description}"

        return JournalLine(
            account_type=EntryType.general_ledger,
            account_number=line['account number'],
            posting_date=line['posting date'],
            document_date=line['document date'],
            document_no=self.entry_id,
            client=line['client'],
            debit=Decimal(line['amount']).quantize(Decimal('1.00')) * -1,
            description=description,
            department=line['department'],
            market=line['market'],
            state=line['state'],
            division=line['division'],
            document_type=DocumentType.invoice,
            business_unit_code=line['entity'].business_unit,
            entry_entity=entry_entity
        )

    def _intercompany_line_to_deposit_entity(self, entity: Entity, total_amount: Decimal) -> JournalLine:
        """Creates intercompany line to the deposit entity"""
        return JournalLine(
            account_type=EntryType.general_ledger,
            account_number=INTERCOMPANY_GL_ASSET_ACCOUNT,
            posting_date=self.posting_date,
            document_date=self.document_date,
            document_no=self.entry_id,
            debit=total_amount,
            # Using the first lines description, line[0], is an imperfect workaround.
            description=f"{entity.abbreviation} - {self.lines[0]['description']}",
            client=self.deposit_client_code,
            document_type=DocumentType.invoice,
            department=Department.corporate,
            market=self.deposit_entity.major_market,
            state=self.deposit_entity.major_state,
            division=self.deposit_entity.major_division,
            business_unit_code=self.deposit_entity.business_unit,
            entry_entity=entity,
        )

    def create_entry_id(self) -> str:
        return f"SJ{datetime.now().strftime('%Y%m%d')}{self.deposit_client_code}"

    @property
    def entities_and_amount(self) -> dict:
        """
        Looks through the lines to pick out the entities because each journal entry is done in an entity.
        """
        if not self._entity_and_amount:
            for line in self.lines:
                if entity := line.get('entity'):
                    self._entity_and_amount[entity] = Decimal(
                        self._entity_and_amount.get(entity, 0) + Decimal(line['amount'])
                    ).quantize(Decimal('1.00'))

        return self._entity_and_amount


def save_import_jes(
        entries: ImportEntries,
        save_location: Path,
        version: str,
) -> Path:
    """
    Using the list of entries from the entries attribute. A dataframe of the entries are created. Looking at each
    entities set of entries they are saved off as a .txt file to the specified location.
    """
    # TODO: Implement support for Quickbooks
    # TODO: Implement support for SAP
    # TODO: Implement support for Oracle Fusion

    df = entries.to_dataframe()
    statement_save_location = save_location / f'{entries.statement_reference}'
    statement_save_location.mkdir()
    for entity in df['entry_entity'].unique():
        destination = statement_save_location / f"{entries.posting_date.strftime('%m.%d.%y')} " \
                                                f"{entries.document_date.strftime('%m.%y')} " \
                                                f"CK {entries.deposit_id} " \
                                                f"IMPORT_{entries.import_version}_{entity}.txt"
        df[df['entry_entity'] == entity].drop('entry_entity', axis=1) \
            .to_csv(destination, sep='\t', index=False, header=False, date_format='%m%d%y', )

    # TODO: zip the files
    return statement_save_location

