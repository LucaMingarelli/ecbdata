# ecbdata <img src="https://raw.githubusercontent.com/LucaMingarelli/ecbdata/master/ecbdata/res/Logo_European_Central_Bank.svg"  width="80">

[![CircleCI](https://circleci.com/gh/LucaMingarelli/ecbdata.svg?style=svg&circle-token=cd9c300380d25c24c66cd6637693cc50a7e00248)](https://app.circleci.com/pipelines/github/LucaMingarelli/ecbdata)
[![version](https://img.shields.io/badge/version-0.1.1-success.svg)](#)
[![PyPI Latest Release](https://img.shields.io/pypi/v/ecbdata.svg)](https://pypi.org/project/ecbdata/)
[![License](https://img.shields.io/pypi/l/ecbdata.svg)](https://github.com/LucaMingarelli/ecbdata/blob/master/LICENSE.txt)
[![Downloads](https://static.pepy.tech/badge/ecbdata)](https://pepy.tech/project/ecbdata)
<a href="https://www.buymeacoffee.com/lucamingarelli" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 109px !important;" ></a>

## About

The **ecbdata** API allows for easy querying of data 
from the European Central Bank's [Data Portal](https://data.ecb.europa.eu/help/data/overview).

## Installation
You can install with pip as:

`pip install ecbdata`

### Example

```python
from ecbdata import ecbdata

df = ecbdata.get_series('ICP.M.U2.Y.XEF000.3.INX', start='2024-01', end='2024-03')

```

When behind a proxy server, one can establish a connection as

```python
from ecbdata import ecbdata

ecbdata.connect(proxies={'https': '<https-proxy>',
                         'http': '<http-proxy>'})

df = ecbdata.get_series('ICP.M.U2.Y.XEF000.3.INX', start='2024-01', end='2024-03')

```

For details on available series and filters, 
please consult the [ECB Data Portal](https://data.ecb.europa.eu/help/data/overview) page.


## Author

Luca Mingarelli, 2024

**You find this work useful?** <a href="https://www.buymeacoffee.com/lucamingarelli" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 109px !important;" ></a>

[![Python](https://img.shields.io/static/v1?label=made%20with&message=Python&color=blue&style=for-the-badge&logo=Python&logoColor=white)](#)
