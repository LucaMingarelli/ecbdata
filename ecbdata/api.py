"""  Created on 15/04/2024::
------------- api.py -------------
 
**Authors**: L. Mingarelli
"""

import requests
import re, io
import pandas as pd

WSENTRYPOINT = 'https://data-api.ecb.europa.eu'


class ECB_DataPortal:

    def __init__(self, proxies=None, verify=None):
        """
        ECB_DataPortal class for retrieving data from the ECB Data Portal: https://data.ecb.europa.eu/.
        This class is a wrapper around the associated RESTful API https://data.ecb.europa.eu/help/api/overview.

        Args:
            proxy: Proxies specifications: a dictionary mapping protocol names (e.g. 'http', 'https') to proxy URLs. If not provided, environment variables 'HTTP_PROXY', 'HTTPS_PROXY' are used.
            verify: Whether to verify SSL certificates. Either of: `True`: Verifies certificates using the default trust store; `False`: Bypasses certificate verification (use with caution!); Path to a PEM-encoded certificate file: Uses the specified certificate to verify the server's certificate chain.

        Examples:
            >>> from ecbdata import ecbdata
            >>> df = ecbdata.get_series('ICP.M.U2.Y.XEF000.3.INX')
            >>> # Or to specify Proxies
            >>> from ecbdata import ECB_DataPortal
            >>> ecbdata = ECB_DataPortal(proxies={'https': '<https-proxies>',
            >>>                                   'http': '<http-proxies>'},
            >>>                          verify=False)
            >>> df = ecbdata.get_series('ICP.M.U2.Y.XEF000.3.INX')
        """
        self.proxies = proxies
        self.verify = verify
        self._session = self.Session(proxies=self.proxies, verify=self.verify)


    def Session(self, proxies: dict=None, verify: bool or str=None):
        """
        Wrapper around :class:`requests:requests.Session`.

        The Session object allows you to persist certain parameters across requests. It also persists cookies across
        all requests made from the Session instance, and will use urllib3’s connection pooling. So if you’re making
        several requests to the same host, the underlying TCP connection will be reused, which can result in a
        significant performance increase (see HTTP persistent connection).

        For more details see the documentation of the wrapped :class:`requests:requests.Session` class.

        Args:
            proxy: Proxies specifications: a dictionary mapping protocol names (e.g. 'http', 'https') to proxy URLs. If not provided, environment variables 'HTTP_PROXY', 'HTTPS_PROXY' are used.
            verify: Whether to verify SSL certificates. Either of: `True`: Verifies certificates using the default trust store; `False`: Bypasses certificate verification (use with caution!); Path to a PEM-encoded certificate file: Uses the specified certificate to verify the server's certificate chain.

        """
        if not hasattr(self, '_session') or not self._session:
            session = requests.Session()
            session.proxies = proxies or {}
            if verify:
                session.verify = verify
            self._session = session
            return session


    def _search_string(self, ticker, start=None, end=None,
                       detail=None, updatedafter=None,
                       firstnobservations=None, lastnobservations=None,
                       includehistory=False
                       ):
        """Constructs the url string for the options specified."""
        includehistory = 'true' if includehistory else 'false'

        decoded = re.findall(r"(\w+)\.", ticker)
        db = decoded[0]
        ticker_str = '.'.join(re.findall(r"\.(\w+)", ticker))
        url = f"{WSENTRYPOINT}/service/data/{db}/{ticker_str}?format=csvdata"
        if start: url += f'&startPeriod={start}'
        if end:   url += f'&endPeriod={end}'
        if detail: url += f"&detail={detail}"
        if updatedafter: url += f"&updatedafter={updatedafter}"
        if firstnobservations: url += f"&firstnobservations={firstnobservations}"
        if lastnobservations: url += f"&lastnobservations={lastnobservations}"
        if includehistory: url += f"&includehistory={includehistory}"
        return url

    def __response_handler(self, response):

        errors_msgs = {
        304: "No changes. There have been no changes to the data since the timestamp supplied in the If-Modified-Since header.",
        400: "Syntax error. Syntactic or semantic issue with the parameters supplied.",
        404: "No results found. There are no results matching the query.",
        406: "Not Acceptable.",
        500: "Internal Server Error. Feel free to try again later or to contact the support hotline https://ecb-registration.escb.eu/statistical-information.",
        501: "Not implemented.",
        503: "Service unavailable: Web service is temporarily unavailable.",
        }
        if response.status_code!=200:
            if response.status_code in errors_msgs:
                raise Exception(f'REQUEST ERROR {response.status_code}: '+errors_msgs[response.status_code])
            else:
                print(f'REQUEST ERROR {response.status_code}: ')
                response.raise_for_status()

    def get_series(self, ticker, start: str=None, end: str=None,
                   detail: str=None, updatedafter: str=None,
                   firstnobservations: int=None, lastnobservations: int=None, includehistory: bool=False):
        """
        Downloads data for selected ticker.

        Args:
            ticker:
            start: It is possible to define a start date for which observations are to be returned. The values should be given according to the syntax defined in ISO 8601 or as SDMX reporting periods. The format will vary depending on the frequency. The supported formats are: YYYY for annual data (e.g. 2013); YYYY-S[1-2]  for semi-annual data (e.g. 2013-S1); YYYY-Q[1-4]  for quarterly data (e.g. 2013-Q1); YYYY-MM  for monthly data (e.g. 2013-01); YYYY-W[01-53]  for weekly data (e.g. 2013-W01); YYYY-MM-DD  for daily data (e.g. 2013-01-01).
            end:   It is possible to define an end date for which observations are to be returned. The values should be given according to the syntax defined in ISO 8601 or as SDMX reporting periods. The format will vary depending on the frequency. The supported formats are: YYYY for annual data (e.g. 2013); YYYY-S[1-2]  for semi-annual data (e.g. 2013-S1); YYYY-Q[1-4]  for quarterly data (e.g. 2013-Q1); YYYY-MM  for monthly data (e.g. 2013-01); YYYY-W[01-53]  for weekly data (e.g. 2013-W01); YYYY-MM-DD  for daily data (e.g. 2013-01-01).
            detail: Using the detail parameter, it is possible to specify the desired amount of information to be returned by the web service. Possible options are as follows. full: the data (Time series and Observations) and the Attributes will be returned. This is the default. dataonly: the Attributes will be excluded from the returned message. serieskeysonly: only the Time series will be returned, excluding the Attributes and the Observations. This can be used to list Time series that match a certain query without returning the actual data. nodata: the Time series will be returned, including the Attributes, but the Observations will not.
            updatedafter: By supplying a percent-encoded ISO 8601 timestamp for the updatedafter parameter, it is possible to retrieve the latest version of changed values in the database after a certain point in time (i.e. updates and revisions). This will include: the observations that have been added since the supplied timestamp; the observations that have been revised since the supplied timestamp; the observations that have been deleted since the supplied timestamp. For example, the percent-encoded representation for 2009-05-15T14:15:00+01:00 would be: 2009-05-15T14%3A15%3A00%2B01%3A00. Developers who update their local databases with data stored in the ECB Data Portal should make use of the updatedafter parameter, as this will significantly improve performance. Instead of systematically downloading data that have not changed, you will only receive the changes that were made in the database after you last performed the same query. If nothing has changed, the server will respond with a HTTP 304 response code.
            firstnobservations:  returns first `firstnobservations` observations.
            lastnobservations: returns last `lastnobservations` observations.
            includehistory: Using the includehistory parameter, you can instruct the web service to return previous versions of the matching data. This allows you to see how the data have evolved over time (i.e. see when new data were released, revised or deleted). Possible options are: false: only the version currently in production will be returned. This is the default. true: the version currently in production and all previous versions will be returned.
        Returns:
            pandas.DataFrame

        Examples:
            >>> from ecbdata import ecbdata
            >>> df = ecbdata.get_series('ICP.M.U2.Y.XEF000.3.INX')
        """
        # response = _session.get(url=f"{WSENTRYPOINT}/service/data/{db}/{ticker_str}?format=csvdata")
        response = self._session.get(url=self._search_string(ticker=ticker, start=start, end=end,
                                                             detail=detail, updatedafter=updatedafter,
                                                             firstnobservations=firstnobservations,
                                                             lastnobservations=lastnobservations,
                                                             includehistory=includehistory))
        self.__response_handler(response=response)
        df = pd.read_csv(io.StringIO(response.content.decode()))
        return df



ecbdata = ECB_DataPortal()

