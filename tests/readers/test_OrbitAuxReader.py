import numpy as np
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from surveySimPP.readers.OrbitAuxReader import OrbitAuxReader
from surveySimPP.utilities.dataUtilitiesForTests import get_test_filepath


def test_OrbitAuxReader():
    txt_reader = OrbitAuxReader(get_test_filepath("testorb.des"), "whitespace")
    orbit_txt = txt_reader.read_rows()
    assert_equal(len(orbit_txt), 5)

    csv_reader = OrbitAuxReader(get_test_filepath("testorb.csv"), "csv")
    orbit_csv = csv_reader.read_rows()
    assert_equal(len(orbit_csv), 5)

    # Check we get the same results from both formats.
    assert_frame_equal(orbit_csv, orbit_txt)

    # Check that we modify the columns (i -> incl, etc.)
    expected_columns = np.array(["ObjID", "q", "e", "incl", "node", "argperi", "t_p", "t_0"], dtype=object)
    assert_equal(expected_columns, orbit_txt.columns.values)

    # Check that we read the correct valude, including dropped columns.
    expected_first_row = np.array(
        [
            "S00000t",
            0.952105479028,
            0.504888475701,
            4.899098347472,
            148.881068605772,
            39.949789586436,
            54486.32292808,
            54466.0,
        ],
        dtype=object,
    )
    assert_equal(expected_first_row, orbit_txt.iloc[0].values)

    # Unexpected H column.
    with pytest.raises(SystemExit) as e1:
        reader = OrbitAuxReader(get_test_filepath("PPReadOrbitFile_bad.txt"), "whitespace")
        _ = reader.read_rows(0, 14)
    assert e1.type == SystemExit
    assert (
        e1.value.code
        == "ERROR: PPReadOrbitFile: H column present in orbits data file. H must be included in physical parameters file only."
    )

    # Incorrect format.
    with pytest.raises(SystemExit) as e2:
        reader = OrbitAuxReader(get_test_filepath("testorb.csv"), "whitespace")
        _ = reader.read_rows(0, 14)
    assert e2.type == SystemExit
