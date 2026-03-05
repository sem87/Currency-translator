from contextlib import nullcontext as does_not_raise

import pytest

from pysev.sev import Cal


class TestCal:
    @pytest.mark.parametrize("x,y,res,expectation",
                             [(4, -2, -2, does_not_raise()),
                              (4, 0, 0, pytest.raises(ZeroDivisionError)),
                              (4, "asd", 0, pytest.raises(TypeError))])
    def test_delenie(self, x, y, res, expectation):
        with expectation:
            assert Cal(x, y).delenie() == res

    @pytest.mark.parametrize("x,y,res,expectation",
                             [(5, 2, 7, does_not_raise()),
                              (4, -2, 2, does_not_raise()),
                              (4, 0, 4, does_not_raise()),
                              (4, "asd", 0, pytest.raises(TypeError)),  # ← Исправлено
                              (-8, -2, -10, does_not_raise()),
                              (-8, -0.2, -8.2, does_not_raise())])
    def test_add(self, x, y, res, expectation):
        with expectation:  # ← Добавлен контекстный менеджер
            assert Cal(x, y).add() == res
