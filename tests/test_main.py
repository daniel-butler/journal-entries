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

    # THEN imports per company are downloaded to the user
    assert len(list(download_directory.iterdir())) == 1

    # THEN all  the expected zip files are in the directory
    zf = zipfile.ZipFile(list(download_directory.iterdir())[0])
    assert zf.namelist() == [
        '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_AZ.txt', '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_CFS.txt',
        '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_HF.txt', '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_HOPCO.txt',
        '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_HW.txt', '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_JGA.txt',
        '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_LV.txt', '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_MSI.txt',
        '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_MSM.txt', '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_NETCG.txt',
        '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_SFA.txt', '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_SFM.txt',
        '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_SGL.txt', '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_SI.txt',
        '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_SW.txt', '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_TCG.txt',
        '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_WFM.txt', '02.17.20 01.20 CK 191705 $56539.96 IMPORT_V7_WM.txt'
    ]
