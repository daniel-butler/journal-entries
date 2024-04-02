from attrs import define, field
from enum import StrEnum
import pandas as pd

INTERCOMPANY_GL_ASSET_ACCOUNT = '12300'
INTERCOMPANY_GL_LIABILITY_ACCOUNT = '22300'


class EntryType(StrEnum):
    """
    This class is used to determine what sub-ledger or ledger the journal entry is posted to.
    """
    general_ledger = "G/L Account"  # References the General Ledger
    customer = "Customer",  # References the Accounts Receivable sub-ledger


class DocumentType(StrEnum):
    """
    This class is used to determine the type of document the journal entry is.
    """
    invoice = "Invoice"
    credit_memo = "Credit Memo"
    payment = "Payment"
    journal_entry = "Journal Entry"
    other = "Other"


class Department(StrEnum):
    """
    This class is used to determine the department the journal entry is posted to.
    """
    corporate = "Corporate"
    retail = "Retail"
    sales = "Sales"
    marketing = "Marketing"
    operations = "Operations"
    finance = "Finance"
    human_resources = "Human Resources"
    it = "Information Technology"
    other = "Other"


class Division(StrEnum):
    one = '1'
    two = '2'
    three = '3'
    four = '4'
    five = '5'
    six = '6'


class Market(StrEnum):
    """
    This class is used to keep all the available markets in one place.

    This class also abstracts away the specific intricacies of the naming of the markets.
    The codes are normally hard to change but their meanings and classifications evolve over time.
    Using this pattern it is easy to change the name of the market without changing the code.
    """

    # Name = Code (used in the system)
    albuquerque = 'ALBUQ'
    atlanta = 'ATLANTA'
    baltimore = 'BALTI'
    billings = 'BILLI'
    boise = 'BOISE'
    boston = 'BOSTON'
    birmingham = 'BIRMING'
    charlotte = 'CHARL'
    chicago = 'CHICA'
    cincinnati = 'CINCI'
    cleveland = 'CLEVE'
    corporate = 'CORPO'
    dakota = 'DAKOT'
    dallas = 'DALLA'
    denver = 'DENVE'
    des_moines = 'DESMO'
    grand_rapids = 'GRAND'
    honolulu = 'HONOL'
    houston = 'HOUST'
    indiana = 'INDIA'
    jackson = 'JACKS'
    north_florida = 'JAXSV'
    kansas = 'KANSA'
    knoxville = 'KNOXV'
    las_vegas = 'LASVE'
    little_rock = 'LITTL'
    louisville = 'LOUIS'
    memphis = 'MEMPH'
    miami = 'MIAMI'
    milwaukee = 'MILWA'
    minnesota = 'MINNE'
    nashville = 'NASHV'
    new_orleans = 'NEWOR'
    north_california = 'NOCAL'
    ny_metro = 'NYMET'
    ny_upstate = 'NYUPST'
    oklahoma = 'OKLAH'
    omaha = 'OMAHA'
    orlando = 'ORLANDO'
    philadelphia = 'PHILA'
    phoenix = 'PHOEN'
    pittsburgh = 'PITTS'
    portland = 'PORTL'
    richmond = 'RICHM'
    salt_lake = 'SALTL'
    san_antonio = 'SANAN'
    seattle = 'SEATT'
    south_california = 'SOCAL'
    south_carolina = 'SOCAR'
    spokane = 'SPOKA'
    st_louis = 'STLOU'
    tampa = 'TAMPA'
    west_texas = 'WESTT'


@define
class Entity:
    business_unit: int
    name: str
    abbreviation: str
    major_market: Market
    major_state: str
    major_division: Division


# States do not have a class because they are universal and do not change.
e1 = Entity(
    business_unit=1007, name='NebulaSolutions', abbreviation='NS', major_market=Market.phoenix,
    major_state='AZ', major_division=Division.one
)
e2 = Entity(
    business_unit=1023, name='StellarGlobe', abbreviation='SG', major_market=Market.pittsburgh,
    major_state='PA', major_division=Division.two
)
e3 = Entity(
    business_unit=1016, name='DynamicHorizon', abbreviation='HF', major_market=Market.des_moines,
    major_state='IA', major_division=Division.three
)
e4 = Entity(
    business_unit=1015, name='InfiniteVista', abbreviation='IV', major_market=Market.tampa,
    major_state='FL', major_division=Division.four
)
e5 = Entity(
    business_unit=1011, name='FusionPulse', abbreviation='FP', major_market=Market.denver,
    major_state='CO', major_division=Division.three
)
e6 = Entity(
    business_unit=1001, name='SynergyPeak', abbreviation='SP', major_market=Market.south_california,
    major_state='CA', major_division=Division.one
)
e7 = Entity(
    business_unit=1003, name='ZenithWave', abbreviation='ZW', major_market=Market.las_vegas,
    major_state='NV', major_division=Division.one
)
e8 = Entity(
    business_unit=1002, name='PinnacleCrest', abbreviation='PC', major_market=Market.north_california,
    major_state='CA', major_division=Division.one
)
e9 = Entity(
    business_unit=1008, name='NexusStrive', abbreviation='NS', major_market=Market.boise,
    major_state='ID', major_division=Division.one
)
e10 = Entity(
    business_unit=1021, name='VisionaryVista', abbreviation='VV', major_market=Market.boston,
    major_state='MA', major_division=Division.two
)
e11 = Entity(
    business_unit=1022, name='CatalystCore', abbreviation='CC', major_market=Market.corporate,
    major_state='ALL', major_division=Division.six
)
e12 = Entity(
    business_unit=1020, name='ZenithQuotient', abbreviation='ZQ', major_market=Market.ny_upstate,
    major_state='NY', major_division=Division.two
)
e13 = Entity(
    business_unit=1019, name='ApexWave', abbreviation='AW', major_market=Market.philadelphia,
    major_state='PA', major_division=Division.two
)
e14 = Entity(
    business_unit=1018, name='EclipticEdge', abbreviation='EE', major_market=Market.indiana,
    major_state='IN', major_division=Division.five
)
e15 = Entity(
    business_unit=1017, name='MomentumStride', abbreviation='MS', major_market=Market.dallas,
    major_state='TX', major_division=Division.three
)
e16 = Entity(
    business_unit=1004, name='FusionFlare', abbreviation='FF', major_market=Market.salt_lake,
    major_state='UT', major_division=Division.one
)
e17 = Entity(
    business_unit=1009, name='EclipsePulse', abbreviation='EP', major_market=Market.corporate,
    major_state='ALL', major_division=Division.six
)
e18 = Entity(
    business_unit=1005, name='NovaSphere', abbreviation='NS', major_market=Market.seattle,
    major_state='WA', major_division=Division.one
)

ENTITIES: dict[str, Entity] = {
    'E1': e1, 'E2': e2, 'E3': e3, 'E4': e4, 'E5': e5, 'E6': e6, 'E7': e7, 'E8': e8, 'E9': e9, 'E10': e10, 'E11': e11,
    'E12': e12, 'E13': e13, 'E14': e14, 'E15': e15, 'E16': e16, 'E17': e17, 'E18': e18,
}


INPUT_CONVERSION_MAP = {
    'V20200224': {
        'column_conversion': {
            'account no.': 'account_number', 'posting date': 'posting_date', 'document date': 'document_date',
            'amount': 'amount', 'description': 'description', 'department': 'department', 'market': 'market',
            'state': 'state', 'customer': 'customer', 'division': 'division', 'client': 'client',
            'employee id': 'employee_id', 'job dimension': 'job_dimension', 'entity': 'entity'
        },
        'column_function_conversions': {
            'posting_date': lambda pd_timestamp: pd_timestamp.to_pydatetime().date() if type(
                pd_timestamp) == pd.Timestamp else pd_timestamp,
            'document_date': lambda pd_timestamp: pd_timestamp.to_pydatetime().date() if type(
                pd_timestamp) == pd.Timestamp else pd_timestamp,
        },
        'required_columns': [
            'account_number', 'posting_date', 'document_date', 'amount', 'description', 'department', 'market', 'state',
            'division', 'client', 'entity'
        ],
        'reverse_column_conversion': {
            'account_number': 'Account No.', 'posting_date': 'Posting Date', 'document_date': 'Document Date',
            'amount': 'Amount', 'description': 'Description', 'department': 'Department', 'market': 'Market',
            'state': 'State', 'customer': 'Customer', 'division': 'Division', 'client': 'Client',
            'employee_id': 'Employee Id', 'job_dimension': 'Job Dimension', 'entity': 'Entity'
        }
    }
}