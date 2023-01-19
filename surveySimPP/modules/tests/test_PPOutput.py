import pandas as pd
import sqlite3
import os
import numpy as np
from numpy.testing import assert_equal

from surveySimPP.tests.data import get_test_filepath


def test_PPOutWriteCSV():

    from surveySimPP.modules.PPOutput import PPOutWriteCSV

    observations = pd.read_csv(get_test_filepath('test_input_fullobs.csv'), nrows=1)
    tmp_path = os.path.dirname(get_test_filepath('test_input_fullobs.csv'))

    PPOutWriteCSV(observations, os.path.join(tmp_path, 'test_csv_out.csv'))

    test_in = pd.read_csv(os.path.join(tmp_path, 'test_csv_out.csv'))

    pd.testing.assert_frame_equal(observations, test_in)

    os.remove(os.path.join(tmp_path, 'test_csv_out.csv'))

    return


def test_PPOutWriteSqlite3():

    from surveySimPP.modules.PPOutput import PPOutWriteSqlite3

    observations = pd.read_csv(get_test_filepath('test_input_fullobs.csv'), nrows=1)
    tmp_path = os.path.dirname(get_test_filepath('test_input_fullobs.csv'))

    PPOutWriteSqlite3(observations, os.path.join(tmp_path, 'test_sql_out.db'))

    cnx = sqlite3.connect(os.path.join(tmp_path, 'test_sql_out.db'))
    cur = cnx.cursor()
    cur.execute('select * from pp_results')
    col_names = list(map(lambda x: x[0], cur.description))

    test_in = pd.DataFrame(cur.fetchall(), columns=col_names)

    pd.testing.assert_frame_equal(observations, test_in)

    os.remove(os.path.join(tmp_path, 'test_sql_out.db'))

    return


# def test_PPOutWriteHDF5():
#
#     from surveySimPP.modules.PPOutput import PPOutWriteHDF5
#     import warnings
#     warnings.filterwarnings("ignore", message="numpy.dtype size changed")
#     warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
#     warnings.filterwarnings("ignore", message="`np.typeDict` is a deprecated alias")
#     warnings.filterwarnings("ignore", message="distutils Version classes are deprecated")
#
#     observations = pd.read_csv(get_test_filepath('test_input_fullobs.csv'), nrows=1)
#     tmp_path = os.path.dirname(get_test_filepath('test_input_fullobs.csv'))
#
#     PPOutWriteHDF5(observations, os.path.join(tmp_path, 'test_hdf5_out.h5'), 'testchunk')
#
#     test_in = pd.read_hdf(os.path.join(tmp_path, 'test_hdf5_out.h5'), key='testchunk')
#
#     pd.testing.assert_frame_equal(observations, test_in)
#
#     os.remove(os.path.join(tmp_path, 'test_hdf5_out.h5'))
#
#     return


def test_PPWriteOutput():

    from surveySimPP.modules.PPOutput import PPWriteOutput

    observations = pd.read_csv(get_test_filepath('test_input_fullobs.csv'), nrows=1)
    tmp_path = os.path.dirname(get_test_filepath('test_input_fullobs.csv'))

    cmd_args = {'outpath': tmp_path,
                'outfilestem': 'PPOutput_test_out'}

    configs = {'outputsize': 'default',
               'position_decimals': 7,
               'magnitude_decimals': 3,
               'outputformat': 'csv'}

    PPWriteOutput(cmd_args, configs, observations, 10)
    csv_test_in = pd.read_csv(os.path.join(tmp_path, 'PPOutput_test_out.csv'))

    configs['outputformat'] = 'separatelycsv'
    PPWriteOutput(cmd_args, configs, observations, 10)
    sep_test_in = pd.read_csv(os.path.join(tmp_path, 'S1000000a_PPOutput_test_out.csv'))

    configs['outputformat'] = 'sqlite3'
    PPWriteOutput(cmd_args, configs, observations, 10)
    cnx = sqlite3.connect(os.path.join(tmp_path, 'PPOutput_test_out.db'))
    cur = cnx.cursor()
    cur.execute('select * from pp_results')
    col_names = list(map(lambda x: x[0], cur.description))
    sql_test_in = pd.DataFrame(cur.fetchall(), columns=col_names)

    expected = np.array(['S1000000a', 61769.32062, 163.8754209, -18.8432714, 164.037713,
                         -17.582575, 3e-06, 'r', 19.647, 19.648, 0.007, 0.007, 23.864,
                         23.839], dtype=object)

    assert_equal(csv_test_in.loc[0, :].values, expected)
    assert_equal(sep_test_in.loc[0, :].values, expected)
    assert_equal(sql_test_in.loc[0, :].values, expected)
    
    os.remove(os.path.join(tmp_path, 'PPOutput_test_out.csv'))
    os.remove(os.path.join(tmp_path, 'S1000000a_PPOutput_test_out.csv'))
    os.remove(os.path.join(tmp_path, 'PPOutput_test_out.db'))

    return
