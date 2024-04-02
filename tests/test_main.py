import zipfile
from decimal import Decimal
from pathlib import Path

from constants import Market, Division, e16, Department
from main import main

test_directory = Path(__file__).parent / "data"


def test_creating_import_happy_case(tmp_path):
    # GIVEN the expected test file
    test_file = test_directory / 'Test Files' / '02.17.20 01.20 CK 191705 $56539.96 BRKDWN.xlsx'

    # GIVEN the expected inputs
    statement_amount = Decimal('5896.07')
    client_code = 'P005'
    deposit_date = '2020-02-17'
    document_date = '2020-01-31'
    deposit_payment_id = '191705'
    deposit_department = Department.retail
    deposit_market = Market.corporate
    deposit_state = 'ALL'
    deposit_division = Division.six
    deposit_entity = e16

    # Download directory
    download_directory = tmp_path / 'downloads'

    # WHEN calling the function to generate the imports
    main(

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
