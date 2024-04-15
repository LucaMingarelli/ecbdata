"""  Created on 15/04/2024::
------------- test.py -------------
 
**Authors**: L. Mingarelli
"""
from ecbdata.api import ECB_DataPortal

tickers = ['ICP.M.U2.Y.XEF000.3.INX',                        # Inflation
           'MNA.Q.Y.I8.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.LR.N',   # GDP
           'FM.M.U2.EUR.4F.MM.EONIA.HSTA',                   # EONIA
           'ENA.Q.Y.I8.W2.S1.S1._Z.EMP._Z._T._Z.HW._Z.N',    # Employment in hour worked
           ]

example = ECB_DataPortal(tickers)

# call the class to download the data
example()

# he data file can be retrieved with
example.data
