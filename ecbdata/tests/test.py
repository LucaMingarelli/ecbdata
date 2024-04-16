"""  Created on 15/04/2024::
------------- test.py -------------
 
**Authors**: L. Mingarelli
"""
from ecbdata import ecbdata
import pytest

_MANUAL = False
tickers = ['ICP.M.U2.Y.XEF000.3.INX',                        # Inflation
           'MNA.Q.Y.I8.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.LR.N',   # GDP
           'FM.M.U2.EUR.4F.MM.EONIA.HSTA',                   # EONIA
           'ENA.Q.Y.I8.W2.S1.S1._Z.EMP._Z._T._Z.HW._Z.N',    # Employment in hour worked
           ]

class TestECBDATA:
    def test_get_series(self):
        df = ecbdata.get_series(ticker=tickers[0])
        assert not df.empty
        df = ecbdata.get_series(ticker=tickers[0], start='2024-01', end='2024-03')
        assert df.TIME_PERIOD.min() == '2024-01'
        assert df.TIME_PERIOD.max() == '2024-03'
        print(df)

    def test_error(self):
        with pytest.raises(Exception):
            ecbdata.get_series(ticker="ABC.CBA", start='2024-01-01', end='2024-03-01')




if _MANUAL:

    from connectors.certificates import where
    from connectors.certificates.proxies import PROXIES

    ecbdata.connect(proxies=PROXIES, verify=where())

    ecbdata.get_series(ticker=tickers[0])

