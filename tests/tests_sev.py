import pytest
from contextlib import nullcontext as does_not_raise
from My_site.pysev.sev import *


# def test_fff():
#     assert A.x == 22
#
#
# @pytest.mark.parametrize("x,y,res", [(1, 2, 3), (2, 3, 5), (-8, -9, -17), (int(0), 0, 0)])
# def test_add(x, y, res):
#     assert Cal().add(x, y) == res
class TestCal:
    @pytest.mark.parametrize("x,y,res,expectation",
                             [(4, -2, -2, does_not_raise()),
                              (4, 0, 0, pytest.raises(ZeroDivisionError)),
                              (4, "asd", 0, pytest.raises(TypeError))])
    def test_delenie(self, x, y, res, expectation):
        with expectation:
            assert Cal(x, y).delenie() == res

    @pytest.mark.parametrize("x,y,res",
                             [(5, 2, 7), (4, -2, 2), (4, 0, 4), (4, "asd", 0), (-8, -2, -10), (-8, -0.2, -8.2)])
    def test_add(self, x, y, res):
        assert Cal(x, y).add() == res
