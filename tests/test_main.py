import zipfile
from datetime import date
from decimal import Decimal
from pathlib import Path

import pandas as pd

from constants import Market, Division, e16, Department
from main import main

test_data_directory = Path(__file__).parent / "data"


def test_creating_import_happy_case(tmp_path):
    # GIVEN the expected test file
    test_file = test_data_directory / 'example-statement.xlsx'

    # GIVEN the expected inputs
    statement_amount = Decimal('5896.07')
    client_code = 'P005'
    deposit_date = pd.Timestamp(date(2024, 9, 17))
    document_date = pd.Timestamp(date(2024, 1, 31))
    deposit_payment_id = '191705'
    deposit_department = Department.retail
    deposit_market = Market.corporate
    deposit_state = 'ALL'
    deposit_division = Division.six
    deposit_entity = e16

    # Download directory
    download_directory = tmp_path / 'downloads'
    download_directory.mkdir()

    # WHEN calling the function to generate the imports
    main(
        import_file=test_file,
        client_code=client_code,
        deposit_entity=deposit_entity,
        posting_date=deposit_date,
        document_date=document_date,
        payment_number='191705',
        applies_to_type='Payment',
        department=deposit_department,
        market=deposit_market,
        state=deposit_state,
        division=deposit_division,
        statement_identifier='8495543',
        save_location=download_directory,
    )

    # THEN imports per company are in the single directory
    assert len(list(download_directory.iterdir())) == 1

    # THEN all the expected files are in the directory
    files = list(next(download_directory.iterdir()).iterdir())
    assert sorted([file_.name for file_ in files]) == sorted([
        "09.17.24 01.24 CK 191705 IMPORT_V1_AW.txt", "09.17.24 01.24 CK 191705 IMPORT_V1_HF.txt",
        "09.17.24 01.24 CK 191705 IMPORT_V1_SP.txt", "09.17.24 01.24 CK 191705 IMPORT_V1_CC.txt",
        "09.17.24 01.24 CK 191705 IMPORT_V1_IV.txt", "09.17.24 01.24 CK 191705 IMPORT_V1_VV.txt",
        "09.17.24 01.24 CK 191705 IMPORT_V1_EE.txt", "09.17.24 01.24 CK 191705 IMPORT_V1_MS.txt",
        "09.17.24 01.24 CK 191705 IMPORT_V1_ZQ.txt", "09.17.24 01.24 CK 191705 IMPORT_V1_EP.txt",
        "09.17.24 01.24 CK 191705 IMPORT_V1_NS.txt", "09.17.24 01.24 CK 191705 IMPORT_V1_ZW.txt",
        "09.17.24 01.24 CK 191705 IMPORT_V1_FF.txt", "09.17.24 01.24 CK 191705 IMPORT_V1_PC.txt",
        "09.17.24 01.24 CK 191705 IMPORT_V1_FP.txt", "09.17.24 01.24 CK 191705 IMPORT_V1_SG.txt"
    ])

    # THEN the contents of a files is as expected
    deposit_entity_file: Path = next((file_ for file_ in files if 'FF' in file_.name), None)
    assert deposit_entity_file.read_text() == """\
Customer\tP005\t091724\t013124\t\tSJ20240507P005\t58936.08\t0\tQuasar Innovations Ltd. - JULY 2024\tRetail\tCORPO\t\tALL\t\t6\tP005\t\t1004\tR10\t\t\t\tInvoice\tPayment\t191705
G/L Account\t41000\t091724\t073124\t\tSJ20240507P005\t-1102.93\t0\tQuasar Innovations Ltd. - JULY 2024\tRETAIL\tHONOL\t\tHI\t\t1\tP008\t\t1004\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-13010.94\t0\tIV - Quasar Innovations Ltd. - JULY 2024\tCorporate\tTAMPA\t\tFL\t\t4\tP005\t\t1015\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-483.78\t0\tNS - Quasar Innovations Ltd. - JULY 2024\tCorporate\tPHOEN\t\tAZ\t\t1\tP005\t\t1007\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-3303.02\t0\tSP - Quasar Innovations Ltd. - JULY 2024\tCorporate\tSOCAL\t\tCA\t\t1\tP005\t\t1001\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-3862.23\t0\tPC - Quasar Innovations Ltd. - JULY 2024\tCorporate\tNOCAL\t\tCA\t\t1\tP005\t\t1002\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-1596.91\t0\tFP - Quasar Innovations Ltd. - JULY 2024\tCorporate\tDENVE\t\tCO\t\t3\tP005\t\t1011\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-2308.04\t0\tHF - Quasar Innovations Ltd. - JULY 2024\tCorporate\tDESMO\t\tIA\t\t3\tP005\t\t1016\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-230.78\t0\tNS - Quasar Innovations Ltd. - JULY 2024\tCorporate\tBOISE\t\tID\t\t1\tP005\t\t1008\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-9912.62\t0\tAW - Quasar Innovations Ltd. - JULY 2024\tCorporate\tPHILA\t\tPA\t\t2\tP005\t\t1019\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-2680.94\t0\tVV - Quasar Innovations Ltd. - JULY 2024\tCorporate\tBOSTON\t\tMA\t\t2\tP005\t\t1021\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-6151.14\t0\tZQ - Quasar Innovations Ltd. - JULY 2024\tCorporate\tNYUPST\t\tNY\t\t2\tP005\t\t1020\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-375.73\t0\tNS - Quasar Innovations Ltd. - JULY 2024\tCorporate\tSEATT\t\tWA\t\t1\tP005\t\t1005\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-7240.37\t0\tEE - Quasar Innovations Ltd. - JULY 2024\tCorporate\tINDIA\t\tIN\t\t5\tP005\t\t1018\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-559.57\t0\tZW - Quasar Innovations Ltd. - JULY 2024\tCorporate\tLASVE\t\tNV\t\t1\tP005\t\t1003\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-883.23\t0\tCC - Quasar Innovations Ltd. - JULY 2024\tCorporate\tCORPO\t\tALL\t\t6\tP005\t\t1022\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-4041.33\t0\tEP - Quasar Innovations Ltd. - JULY 2024\tCorporate\tCORPO\t\tALL\t\t6\tP005\t\t1009\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-583.64\t0\tSG - Quasar Innovations Ltd. - JULY 2024\tCorporate\tPITTS\t\tPA\t\t2\tP005\t\t1023\tR10\t\t\t\tInvoice\t\t
G/L Account\t22300\t091724\t013124\t\tSJ20240507P005\t-608.88\t0\tMS - Quasar Innovations Ltd. - JULY 2024\tCorporate\tDALLA\t\tTX\t\t3\tP005\t\t1017\tR10\t\t\t\tInvoice\t\t
""" # noqa


