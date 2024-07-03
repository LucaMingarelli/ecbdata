"""  Created on 15/04/2024::
------------- test.py -------------
 
**Authors**: L. Mingarelli
"""
from ecbdata import ecbdata
import pytest

_MANUAL = False
series_keys = ['ICP.M.U2.Y.XEF000.3.INX',                        # Inflation
               'MNA.Q.Y.I8.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.LR.N',   # GDP
               'FM.M.U2.EUR.4F.MM.EONIA.HSTA',                   # EONIA
               'ENA.Q.Y.I8.W2.S1.S1._Z.EMP._Z._T._Z.HW._Z.N',    # Employment in hour worked
               'EXR.M..EUR.SP00.A',                              # All exchange rates
               'EXR.M.USD+GBP+JPY.EUR.SP00.A',                   # USD, GBP, JPY exchange rates
               ]

class TestECBDATA:
    def test_get_series(self):
        df = ecbdata.get_series(series_key=series_keys[0])
        assert not df.empty
        df = ecbdata.get_series(series_key=series_keys[0], start='2024-01', end='2024-03')
        assert df.TIME_PERIOD.min() == '2024-01'
        assert df.TIME_PERIOD.max() == '2024-03'
        print(df)
        df_all = ecbdata.get_series(series_key=series_keys[4], start='2024-01', end='2024-03')
        assert len(set(df_all.CURRENCY)) >= 30
        df_usd_gbp_jpy = ecbdata.get_series(series_key=series_keys[5], start='2024-01', end='2024-03')
        assert set(df_usd_gbp_jpy.CURRENCY) == {'GBP', 'JPY', 'USD'}

    def test_error(self):
        with pytest.raises(Exception):
            ecbdata.get_series(series_key="ABC.CBA", start='2024-01-01', end='2024-03-01')

    def test_params(self):
        df_first = ecbdata.get_series(series_key=series_keys[0], firstnobservations=5)
        assert (df_first.TIME_PERIOD.nunique() == 5) and (df_first.TIME_PERIOD.min() == '1997-01')
        df_last = ecbdata.get_series(series_key=series_keys[0], lastnobservations=5)
        assert (df_last.TIME_PERIOD.nunique() == 5) and (df_last.TIME_PERIOD.min() != '1997-01')



if _MANUAL:

    from connectors.certificates import where
    from connectors.certificates.proxies import PROXIES

    ecbdata.connect(proxies=PROXIES, verify=where())

    df = ecbdata.get_series(series_key=series_keys[0])

    import pandas as pd, pylab as plt
    from ecbtools import set_ecb_style
    set_ecb_style(font_size=12)

    df = ecbdata.get_series('ICP.M.U2.N.000000.4.ANR', start='2010-01')

    df.TIME_PERIOD = pd.to_datetime(df.TIME_PERIOD)
    df = df.set_index('TIME_PERIOD')

    df.OBS_VALUE.plot()
    plt.xlabel('')
    plt.ylabel('HICP Inflation [%]')
    plt.tight_layout()
    plt.savefig('HICP.png', dpi=400)
    plt.show()




