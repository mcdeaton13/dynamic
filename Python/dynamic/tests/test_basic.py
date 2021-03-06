import os
import sys
CUR_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(CUR_PATH, "../../"))
import pytest
import tempfile
import pickle
import numpy as np
from dynamic.utils import comp_array
from dynamic.utils import comp_scalar
from dynamic.utils import dict_compare

TOL = 1e-5

@pytest.yield_fixture
def picklefile1():
    x = {'a': 1}
    pfile = tempfile.NamedTemporaryFile(mode="a", delete=False)
    pickle.dump(x, pfile)
    pfile.close()
    # must close and then yield for Windows platform
    yield pfile
    os.remove(pfile.name)

@pytest.yield_fixture
def picklefile2():
    y = {'a': 1, 'b':2}

    pfile = tempfile.NamedTemporaryFile(mode="a", delete=False)
    pickle.dump(y, pfile)
    pfile.close()
    # must close and then yield for Windows platform
    yield pfile
    os.remove(pfile.name)

@pytest.yield_fixture
def picklefile3():
    x = {'a':np.array([100.,200.,300.]), 'b':2}
    pfile = tempfile.NamedTemporaryFile(mode="a", delete=False)
    pickle.dump(x, pfile)
    pfile.close()
    # must close and then yield for Windows platform
    yield pfile
    os.remove(pfile.name)

@pytest.yield_fixture
def picklefile4():
    x = {'a':np.array([100.,200.,300.1]), 'b':2}
    pfile = tempfile.NamedTemporaryFile(mode="a", delete=False)
    pickle.dump(x, pfile)
    pfile.close()
    # must close and then yield for Windows platform
    yield pfile
    os.remove(pfile.name)


def test_import_ok():
    import dynamic

def test_run_small():
    from run_small import runner
    runner()


def test_compare_pickle_file_bad(picklefile1, picklefile2):
    from dynamic.utils import pickle_file_compare
    assert not pickle_file_compare(picklefile1.name, picklefile2.name)


def test_compare_pickle_file_bad2(picklefile3, picklefile4):
    from dynamic.utils import pickle_file_compare
    assert not pickle_file_compare(picklefile3.name, picklefile4.name)


def test_compare_pickle_file_relative(picklefile3, picklefile4):
    from dynamic.utils import pickle_file_compare
    assert pickle_file_compare(picklefile3.name, picklefile4.name, relative=True)


def test_compare_pickle_file_basic(picklefile1):
    from dynamic.utils import pickle_file_compare
    assert pickle_file_compare(picklefile1.name, picklefile1.name)

def test_compare_dict_basic():
    from dynamic.utils import dict_compare
    lhs = {'a':1, 'b':2}
    rhs = {'c':4, 'b':2}
    assert not dict_compare("lhs.pkle", lhs, "rhs.pkle", rhs, tol=TOL)

def test_compare_dict_more_lhs():
    from dynamic.utils import dict_compare
    lhs = {'a':1, 'b':2, 'c':3}
    rhs = {'c':4, 'b':2}
    assert not dict_compare("lhs.pkle", lhs, "rhs.pkle", rhs, tol=TOL)

def test_compare_dict_diff_ndarrays():
    from dynamic.utils import dict_compare
    lhs = {'a':np.array([1,2,3]), 'b':2}
    rhs = {'a':np.array([1,3]), 'b':2}
    assert not dict_compare("lhs.pkle", lhs, "rhs.pkle", rhs, tol=TOL)

def test_compare_dict_diff_ndarrays2():
    from dynamic.utils import dict_compare
    lhs = {'a':np.array([1.,2.,3.]), 'b':2}
    rhs = {'a':np.array([1.,2.,3.1]), 'b':2}
    assert not dict_compare("lhs.pkle", lhs, "rhs.pkle", rhs, tol=TOL)

def test_comp_array_relative():
    x = np.array([100., 200., 300.])
    y = np.array([100.01, 200.02, 300.03])
    unequal = []
    assert not comp_array("test", y, x, 1e-3, unequal)
    assert comp_array("test", y, x, 1e-3, unequal, relative=True)

def test_comp_scalar_relative():
    x = 100
    y = 100.01
    unequal = []
    assert not comp_scalar("test", y, x, 1e-3, unequal)
    assert comp_scalar("test", y, x, 1e-3, unequal, relative=True)

def test_compare_dict_diff_ndarrays_relative():
    lhs = {'a':np.array([100.,200.,300.]), 'b':2}
    rhs = {'a':np.array([100.,200.,300.1]), 'b':2}
    assert dict_compare("lhs.pkle", lhs, "rhs.pkle", rhs, tol=1e-3, relative=True )


