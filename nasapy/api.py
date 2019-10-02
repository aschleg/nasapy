# encoding=utf-8

"""

"""

from urllib.parse import urljoin
import datetime
import requests


class Nasa(object):
    r"""

    Parameters
    ----------

    Attributes
    ----------

    Methods
    -------

    Examples
    --------

    """
    def __init__(self, key=None):

        self.api_key = key

        self.host = 'https://api.nasa.gov'
        self.limit_remaining = None
        self.mars_weather_limit_remaining = None
    
    @property
    def api_key(self):
        return self.__api_key

    @property
    def limit_remaining(self):
        return self.__limit_remaining

    @property
    def mars_weather_limit_remaining(self):
        return self.__mars_weather_limit_remaining

    @api_key.setter
    def api_key(self, api_key):
        if api_key is not None:
            self.__api_key = api_key
        else:
            self.__api_key = 'DEMO_KEY'

    @limit_remaining.setter
    def limit_remaining(self, remaining):
        self.__limit_remaining = remaining

    @mars_weather_limit_remaining.setter
    def mars_weather_limit_remaining(self, remaining):
        self.__mars_weather_limit_remaining = remaining

    def picture_of_the_day(self, date=None, hd=False):
        r"""
        Returns the URL and other information for the NASA Picture of the Day.

        Parameters
        ----------
        date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the  current
            date.
        hd : bool, default False
            If True, returns the associated high-definition image of the Astrononmy Picture of the Day.

        Raises
        ------
        TypeError
            Raised if the parameter :code:`date` is not a string or a datetime object.
        TypeError
            Raised if the parameter :code:`hd` is not boolean.
        HTTPError
            Raised if the returned status code is not 200 (success).

        Returns
        -------
        dict
            Dictionary object of the JSON data returned from the API.

        Examples
        --------
        # Initialize Nasa API Class with a demo key
        >>> n = Nasa()
        # Return today's picture of the day
        >>> n.picture_of_the_day()
        # Return a previous date's picture of the day with the high-definition URL included.
        >>> n.picture_of_the_day('2019-01-01', hd=True)

        """
        if date is not None:
            if not isinstance(date, (str, datetime.datetime)):
                raise TypeError('date parameter must be a string representing a date in YYYY-MM-DD format or a datetime '
                                'object.')

        if not isinstance(hd, bool):
            raise TypeError('hd parameter must be True or False (boolean).')

        if isinstance(date, datetime.datetime):
            date = date.strftime('%Y-%m-%d')

        url = urljoin(self.host + '/planetary/', 'apod')

        r = requests.get(url,
                         params={
                             'api_key': self.api_key,
                             'date': date,
                             'hd': hd
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason)

        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def mars_weather(self):
        r"""
        Returns per-Sol (Martian Days) summary data for each of the last seven available Sols.

        Raises
        ------
        HTTPError
        Raised when the returned status code is not 200 (success).

        Returns
        -------
        dict
            Dictionary object repreenting the returned JSON data from the API.

        Examples
        --------
        # Initialize NASA API object with a demo key
        >>> n = NASA()
        # Return the most recent data for the previous seven Sols (Martian Days)
        >>> n.mars_weather()

        Notes
        -----
        Data is provided by NASA's InSight Mars lander and as such data for particular Sols may be recalculated as
        more data is received.

        For more information on the data returned, please see
        `NASA's documentation
        <https://github.com/nasa/api-docs/blob/gh-pages/InSight%20Weather%20API%20Documentation.pdf>`_

        """
        url = self.host + '/insight_weather/'

        r = requests.get(url,
                         params={
                             'api_key': self.__api_key,
                             'ver': 1.0,
                             'feedtype': 'json'
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.__mars_weather_limit_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def asteroid_feed(self, start_date, end_date=None):
        r"""
        Returns a list of asteroids based on their closest approach date to Earth.

        Parameters
        ----------
        start_date : str, datetime
            String representing a date in YYYY-MM-DD format or a datetime object.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to seven days
            after the provided :code:`start_date`.

        Raises
        ------
        TypeError
            Raised if the :code:`start_date` parameter is not a string or a datetime object.
        TypeError
            Raised if the :code:`end_date` parameter is not a string or a datetime object.
        HTTPError
            Raised if the returned status code is not 200 (success).

        Returns
        -------
        dict
            Dictionary representing the returned JSON data from the API.

        Examples
        --------
        # Initialize the NASA API with a demo key.
        >>> n = NASA()
        # Get asteroids approaching Earth at the beginning of 2019.
        >>> n.asteroid_feed(start_date='2019-01-01')

        """
        url = self.host + '/neo/rest/v1/feed'

        start_date, end_date = _check_dates(start_date=start_date, end_date=end_date)

        r = requests.get(url,
                         params={
                             'api_key': self.__api_key,
                             'start_date': start_date,
                             'end_date': end_date
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def get_asteroids(self, asteroid_id=None):
        r"""
        Returns data from the overall asteroid data-set or specific asteroids given an ID.

        Parameters
        ----------
        asteroid_id : str, int, default None
            If None, the entire asteroid data set is returned. If an :code:`asteroid_id` is provided, data on that
            specific asteroid is returned.

        Raises
        ------
        HTTPError:
            Raised if the returned status code from the API is not 200 (success).

        Returns
        -------
        dict
            Dictionary object representing the returned JSON data from the NASA API.

        Examples
        --------
        # Initialize NASA API with a demo key.
        >>> n = Nasa()
        # Get entire asteroid data set.
        >>> n.get_asteroids()
        # Get asteroid with ID 3542519
        >>> n.get_asteroids(asteroid_id=3542519)

        """
        url = self.host + '/neo/rest/v1/neo/'

        if asteroid_id is not None:
            url = url + str(asteroid_id)

        else:
            url = url + 'browse/'

        r = requests.get(url,
                         params={
                             'api_key': self.__api_key
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def neo_sentry(self, active=True):
        pass

    def coronal_mass_ejection(self, start_date=None, end_date=None,
                              accurate_only=True, speed=0, complete_entry=True, half_angle=0,
                              catalog='ALL', keyword=None):
        r"""
        Returns data collected on coronal mass ejection events from the Space Weather Database of Notifications,
        Knowledge, Information (DONKI).

        Parameters
        ----------
        start_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior
            to the current date in UTC time.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current
            date in UTC time.
        accurate_only : bool, default True
            If True (default), only the most accurate results collected are returned.
        complete_entry : bool, default True
            If True (default), only results with complete data is returned.
        speed : int, default 0
            The lower limit of the speed of the CME event. Default is 0
        half_angle : int, default 0
            The lower limit half angle of the CME event. Default is 0.
        catalog : str, {'ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG'}
            Specifies which catalog of data to return results. Defaults to 'ALL'.
        keyword : str, default None
            Filter results by a specific keyword.

        Raises
        ------
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        ValueError
            Raised if the :code:`catalog` parameter is not one of {'ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG'}.
        TypeError
            Raised if parameter :code:`complete_entry` is not boolean (True or False).
        TypeError
            Raised if parameter :code:`accurate_only` is not boolean (True or False).

        Returns
        -------
        list
            List of results representing returned JSON data. If no data is returned, an empty dictionary is returned.

        Examples
        --------
        # Initialize NASA API with a demo key
        >>> n = Nasa()
        # View data from coronal mass ejection events from the last thirty days
        >>> n.coronal_mass_ejection()
        # View all CME events from the beginning of 2019.
        >>> n.coronal_mass_ejection(start_date='2019-01-01', end_date=datetime.datetime.today())

        """
        start_date, end_date = _check_dates(start_date=start_date, end_date=end_date)

        if catalog not in ('ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG'):
            raise ValueError("catalog parameter must be one of ('ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG')")

        if not isinstance(complete_entry, bool):
            raise TypeError('complete_entry parameter must be boolean (True or False).')

        if not isinstance(accurate_only, bool):
            raise TypeError('accurate_only parameter must be boolean (True or False).')

        url = self.host + '/DONKI/CMEAnalysis'

        r = requests.get(url,
                         params={
                             'api_key': self.__api_key,
                             'startDate': start_date,
                             'endDate': end_date,
                             'mostAccurateOnly': accurate_only,
                             'completeEntryOnly': complete_entry,
                             'speed': speed,
                             'halfAngle': half_angle,
                             'catalog': catalog,
                             'keyword': keyword
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']

            if r.text == '':
                r = {}
            else:
                r = r.json()

            return r

    def geomagnetic_storm(self, start_date=None, end_date=None):
        r"""
        Returns data collected on geomagnetic storm events from the Space Weather Database of Notifications, Knowledge,
        Information (DONKI).

        Parameters
        ----------
        start_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior
            to the current date in UTC time.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current
            date in UTC time.

        Raises
        ------
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.

        Returns
        -------
        list
            List of results representing returned JSON data. If no data is returned, an empty dictionary is returned.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Get geomagnetic storm events from the last thirty days.
        >>> n.geomagnetic_storm()
        [{'gstID': '2019-08-31T12:00:00-GST-001',
          'startTime': '2019-08-31T12:00Z',
          'allKpIndex': [{'observedTime': '2019-08-31T15:00Z',
            'kpIndex': 6,
            'source': 'NOAA'},
           {'observedTime': '2019-09-01T15:00Z', 'kpIndex': 6, 'source': 'NOAA'}],
          'linkedEvents': [{'activityID': '2019-08-30T12:17:00-HSS-001'}]}]

        """
        start_date, end_date = _check_dates(start_date=start_date, end_date=end_date)

        url = self.host + '/DONKI/GST'

        r = requests.get(url,
                         params={
                             'api_key': self.__api_key,
                             'startDate': start_date,
                             'endDate': end_date
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']

            if r.text == '':
                r = {}
            else:
                r = r.json()

            return r

    def interplantary_shock(self, start_date=None, end_date=None, location='ALL', catalog='ALL'):
        r"""
        Returns data collected on interplantary shock events from the Space Weather Database of Notifications,
        Knowledge, Information (DONKI).

        Parameters
        ----------
        start_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior
            to the current date in UTC time.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current
            date in UTC time.
        location : str, {'ALL', 'Earth', 'MESSENGER', 'STEREO A', 'STEREO B'}
            Filters returned results to specified location of the interplantary shock event. Defaults to 'ALL'.
        catalog : str, {'ALL', 'SWRC_CATALOG', 'WINSLOW_MESSENGER_ICME_CATALOG'}
            Filters results to a specified catalog of collected data. Defaults to 'ALL'.

        Raises
        ------
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        ValueError
            Raised if :code:`location` parameter is not one of {'ALL', 'Earth', 'MESSENGER', 'STEREO A', 'STEREO B'}
        ValueError
            Raised if :code:`catalog` parameter is not one of {'ALL', 'SWRC_CATALOG', 'WINSLOW_MESSENGER_ICME_CATALOG'}
        TypeError
            Raised if :code:`location` parameter is not a string.
        TypeError
            Raised if :code:`catalog` parameter is not a string.

        Returns
        -------
        list
            List of results representing returned JSON data. If no data is returned, an empty list is returned.

        Examples
        --------

        """
        start_date, end_date = _check_dates(start_date=start_date, end_date=end_date)

        if not isinstance(location, str):
            raise TypeError('location parameter must be a string')

        if not isinstance(catalog, str):
            raise TypeError('catalog parameter must be a string')

        if location not in ('ALL', 'Earth', 'MESSENGER', 'STEREO A', 'STEREO B'):
            raise ValueError(
                "location parameter must be one of {'ALL' (default), 'Earth', 'MESSENGER', 'STEREO A', 'STEREO B'}")

        if catalog not in ('ALL', 'SWRC_CATALOG', 'WINSLOW_MESSENGER_ICME_CATALOG'):
            raise ValueError(
                "catalog parameter must be one of {'ALL' (default) 'SWRC_CATALOG', 'WINSLOW_MESSENGER_ICME_CATALOG'}")

        url = self.host + '/DONKI/IPS'

        r = requests.get(url,
                         params={
                             'api_key': self.__api_key,
                             'startDate': start_date,
                             'endDate': end_date,
                             'location': location,
                             'catalog': catalog
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']

            if r.text == '':
                r = {}
            else:
                r = r.json()

            return r

    def solar_flare(self, start_date=None, end_date=None):
        r"""
        Returns data on solar flare events from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI).

        Parameters
        ----------
        start_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior
            to the current date in UTC time.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current
            date in UTC time.

        Raises
        ------
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.

        Returns
        -------
        list
            If data is available in the specified date range, a list of dictionary objects representing the data from
            the API is returned. If no data is available, an empty dictionary is returned.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Get solar flare events from May of 2019
        >>> n.solar_flare(start_date='2019-05-01', end_date='2019-05-31')
        [{'flrID': '2019-05-06T05:04:00-FLR-001',
          'instruments': [{'id': 11, 'displayName': 'GOES15: SEM/XRS 1.0-8.0'}],
          'beginTime': '2019-05-06T05:04Z',
          'peakTime': '2019-05-06T05:10Z',
          'endTime': None,
          'classType': 'C9.9',
          'sourceLocation': 'N08E50',
          'activeRegionNum': 12740,
          'linkedEvents': None}]

        """
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/FLR',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def solar_energetic_particle(self, start_date=None, end_date=None):
        r"""
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API related to solar energetic particle events.

        Parameters
        ----------
        start_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior
            to the current date in UTC time.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current
            date in UTC time.

        Raises
        ------
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.

        Returns
        -------
        list
            If data is available in the specified date range, a list of dictionary objects representing the data from
            the API is returned. If no data is available, an empty dictionary is returned.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Get data from April 2017
        >>> n.solar_energetic_particle(start_date='2017-04-01', end_date='2017-04-30')
        [{'sepID': '2017-04-18T23:39:00-SEP-001',
          'eventTime': '2017-04-18T23:39Z',
          'instruments': [{'id': 6, 'displayName': 'STEREO A: IMPACT 13-100 MeV'}],
          'linkedEvents': [{'activityID': '2017-04-18T19:15:00-FLR-001'},
           {'activityID': '2017-04-18T19:48:00-CME-001'}]}]

        """
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/SEP',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def magnetopause_crossing(self, start_date=None, end_date=None):
        r"""
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API related to magnetopause crossing events.

        Parameters
        ----------
        start_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior
            to the current date in UTC time.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current
            date in UTC time.

        Raises
        ------
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.

        Returns
        -------
        list
            If data is available in the specified date range, a list of dictionary objects representing the data from
            the API is returned. If no data is available, an empty dictionary is returned.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Get data on magnetopause crossing events from 2018 to the current date.
        >>> n.magnetopause_crossing(start_date='2018-01-01')
        [{'mpcID': '2018-05-05T14:33:00-MPC-001',
          'eventTime': '2018-05-05T14:33Z',
          'instruments': [{'id': 15, 'displayName': 'MODEL: SWMF'}],
          'linkedEvents': [{'activityID': '2018-05-05T09:27:00-HSS-001'}]}]

        """
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/MPC',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def radiation_belt_enhancement(self, start_date=None, end_date=None):
        r"""
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API related to radiation belt enhancement events.

        Parameters
        ----------
        start_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior
            to the current date in UTC time.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current
            date in UTC time.

        Raises
        ------
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.

        Returns
        -------
        list
            If data is available in the specified date range, a list of dictionary objects representing the data from
            the API is returned. If no data is available, an empty dictionary is returned.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Get data on radiation belt enhancement events from the last 30 days.
        >>> n.radiation_belt_enhancement()
        [{'rbeID': '2019-08-31T18:50:00-RBE-001',
          'eventTime': '2019-08-31T18:50Z',
          'instruments': [{'id': 14, 'displayName': 'GOES13: SEM/EPS >0.8 MeV'}],
          'linkedEvents': [{'activityID': '2019-08-30T12:17:00-HSS-001'}]}]

        """
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/RBE',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def hight_speed_stream(self, start_date=None, end_date=None):
        r"""
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API related to hight speed stream events.

        Parameters
        ----------
        start_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior
            to the current date in UTC time.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current
            date in UTC time.

        Raises
        ------
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.

        Returns
        -------
        list
            If data is available in the specified date range, a list of dictionary objects representing the data from
            the API is returned. If no data is available, an empty dictionary is returned.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Get data on hight speed stream events from the beginning of September 2019.
        >>> n.hight_speed_stream()
        [{'hssID': '2019-09-09T01:22:00-HSS-001',
          'eventTime': '2019-09-09T01:22Z',
          'instruments': [{'id': 9, 'displayName': 'ACE: SWEPAM'}],
          'linkedEvents': None},
         {'hssID': '2019-09-12T20:21:00-HSS-001',
          'eventTime': '2019-09-12T20:21Z',
          'instruments': [{'id': 9, 'displayName': 'ACE: SWEPAM'},
           {'id': 10, 'displayName': 'ACE: MAG'}],
          'linkedEvents': None},
         {'hssID': '2019-09-17T03:00:00-HSS-001',
          'eventTime': '2019-09-17T03:00Z',
          'instruments': [{'id': 20, 'displayName': 'STEREO A: IMPACT'},
           {'id': 21, 'displayName': 'STEREO A: PLASTIC'}],
          'linkedEvents': None}]

        """
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/HSS',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def wsa_enlil_simulation(self, start_date=None, end_date=None):
        r"""
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API.

        Parameters
        ----------
        start_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior
            to the current date in UTC time.
        end_date : str, datetime, default None
            String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current
            date in UTC time.

        Raises
        ------
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.
        TypeError
            Raised if parameter :code:`start_date` is not a string representing a date in YYYY-MM-DD format or
            a datetime object.

        Returns
        -------
        list
            If data is available in the specified date range, a list of dictionary objects representing the data from
            the API is returned. If no data is available, an empty dictionary is returned.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Get data from the first simulation performed in 2019.
        >>> wsa = n.wsa_enlil_simulation(start_date='2019-01-01')
        >>> wsa[0]
        {'simulationID': 'WSA-ENLIL/14394/1',
         'modelCompletionTime': '2019-01-03T18:26Z',
         'au': 2.0,
         'cmeInputs': [{'cmeStartTime': '2019-01-02T23:12Z',
           'latitude': -27.0,
           'longitude': 45.0,
           'speed': 430.0,
           'halfAngle': 18.0,
           'time21_5': '2019-01-03T07:15Z',
           'isMostAccurate': True,
           'levelOfData': 1,
           'ipsList': [],
           'cmeid': '2019-01-02T23:12:00-CME-001'}],
         'estimatedShockArrivalTime': None,
         'estimatedDuration': None,
         'rmin_re': None,
         'kp_18': None,
         'kp_90': None,
         'kp_135': None,
         'kp_180': None,
         'isEarthGB': False,
         'impactList': None}

        """
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/WSAEnlilSimulations',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def epic(self, color='natural', date=None, all_dates=True, available=False):
        url = self.host + '/EPIC/api/'

        if color not in ('natural', 'enhanced'):
            raise ValueError("color parameter must be 'natural' (default), or 'enhanced'.")

        if None in (date, all_dates, available):
            url = url + '{color}/all'.format(color=color)

        elif date is not None:
            if not isinstance(date, (str, datetime.datetime)):
                raise TypeError("date parameter must be a string representing a date in YYYY-MM-DD format or a "
                                "datetime object.")

            if isinstance(date, datetime.datetime):
                date = date.strftime('%Y-%m-%d')

            url = url + '{color}/date/{date}'.format(date=date, color=color)

        r = requests.get(url,
                         params={'api_key': self.__api_key})

        return r

    def earth_imagery(self, lat, lon, dim=0.025, date=None, cloud_score=False):
        r"""
        Retrieves the URL and other information from the Landsat 8 image database for the specified lat/lon location
        and date.

        Parameters
        ----------
        lat : int, float
            Latitude
        lon : int, float
            Longitude
        dim : float, default 0.025
            Width and height of the image in degrees.
        date : str, datetime, default None
            Date the image was taken. If specified, must be a string representing a date in 'YYYY-MM-DD' format or a
            datetime object. If None, the most recent image available from the current date is returned.
        cloud_score : bool, default False
            Calculate the percentage of the image covered by clouds.

        Raises
        ------
        TypeError
            Raised if :code:`cloud_score` parameter is not boolean (True or False)
        TypeError
            Raised if :code:`lat` parameter is not an int or float
        TypeError
            Raised if :code:`lon` parameter is not an int or float
        TypeError
            Raised if :code:`dim` parameter is not a float
        TypeError
            Raised if :code:`date` parameter is not a string or a datetime object.
        ValueError
            Raised if :code:`lat` parameter is not between :math:`[-90, 90]`
        ValueError
            Raised if :code:`lon` parameter is not between :math:`[-180, 180]`

        Returns
        -------
        dict
            Dictionary object representing the returned JSON data from the API.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        >>> n.earth_imagery(lon=100.75, lat=1.5, cloud_score=True)
        {'cloud_score': 0.9947187123297982,
         'date': '2014-01-03T03:30:22',
         'id': 'LC8_L1T_TOA/LC81270592014003LGN00',
         'resource': {'dataset': 'LC8_L1T_TOA', 'planet': 'earth'},
         'service_version': 'v1',
         'url': 'https://earthengine.googleapis.com/api/thumb?thumbid=9081d44f6984d0e4791922804beb54a4&token=e5c9e249894564f93533f02dbd87a1a3'}

        """
        url = self.host + '/planetary/earth/imagery/'

        if not isinstance(cloud_score, bool):
            raise TypeError('cloud score parameter must be boolean (True or False).')
        if not isinstance(lat, (int, float)):
            raise TypeError('lat parameter must be an int or float')
        if not isinstance(lon, (int, float)):
            raise TypeError('lon parameter must be an int or float')
        if not isinstance(dim, float):
            raise TypeError('dim parameter must be a float')

        if not -90 <= lat <= 90:
            raise ValueError('latitudes values range from -90 to 90')
        if not -180 <= lon <= 180:
            raise ValueError('longitude values range from -180 to 180')

        if date is not None:
            if not isinstance(date, (str, datetime.datetime)):
                raise TypeError('date parameter must be a string representing a date in YYYY-MM-DD format or a '
                                'datetime object.')

            if isinstance(date, datetime.datetime):
                date = date.strftime('%Y-%m-%d')

        r = requests.get(url,
                         params={
                             'lon': lon,
                             'lat': lat,
                             'dim': dim,
                             'date': date,
                             'cloud_score': cloud_score,
                             'api_key': self.__api_key
                         })

        if r.status_code != 200 or r.text == '':
            r = {}
        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']
            r = r.json()

        return r

    def earth_assets(self, lat, lon, begin_date, end_date=None):
        r"""
        Retrieves the datetimes and asset names of available imagery for a specified lat-lon location over a given
        date range. The satellite that takes the images passes over each point approximately once every sixteen days.

        Parameters
        ----------
        lat : int, float
            Latitude
        lon : int, float
            Longitude
        begin_date : str, datetime
            Beginning of date range in which to search for available assets.
        end_date : str, datetime, default None
            End of date range in which to search for available assets. If not specified, defaults to the current date.

        Raises
        ------
        ValueError
            Raised if :code:`lat` parameter is not between :math:`[-90, 90]`
        ValueError
            Raised if :code:`lon` parameter is not between :math:`[-180, 180]`
        TypeError
            Raised if :code:`begin_date` parameter is not a string representative of a datetime or a datetime object.
        TypeError
            Raised if :code:`end_date` parameter is not a string representative of a datetime or a datetime object.

        Returns
        -------
        dict
            Dictionary object representing the returned JSON data from the API.

        Notes
        -----
        The assets endpoint is meant to support the imagery endpoint by making it easier for users to find available
        imagery for a given location.

        """
        url = self.host + '/planetary/earth/assets'

        if not isinstance(begin_date, (str, datetime.datetime)):
            raise TypeError('begin date parameter must be a string representing a date in YYYY-MM-DD format or a '
                            'datetime object.')

        if isinstance(begin_date, datetime.datetime):
            begin_date = begin_date.strftime('%Y-%m-%d')

        if end_date is not None:
            if not isinstance(end_date, (str, datetime.datetime)):
                raise TypeError('end date parameter must be a string representing a date in YYYY-MM-DD format or a '
                                'datetime object.')

            if isinstance(end_date, datetime.datetime):
                end_date = end_date.strftime('%Y-%m-%d')

        if not -90 <= lat <= 90:
            raise ValueError('latitudes values range from -90 to 90')
        if not -180 <= lon <= 180:
            raise ValueError('longitude values range from -180 to 180')

        r = requests.get(url,
                         params={
                             'api_key': self.__api_key,
                             'lat': lat,
                             'lon': lon,
                             'begin_date': begin_date,
                             'end_date': end_date
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']

            return r.json()

    def exoplanets(self, table, select, count, colset, where, order, ra, dec):
        host = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?'

        r = requests.get(host,
                         params={
                             'api_key': self.__api_key,
                             'table': table,
                             'select': select,
                             'count': count,
                             'colset': colset,
                             'where': where,
                             'order': order,
                             'ra': ra,
                             'dec': dec,
                             'format': 'json'
                         })


def _donki_request(key, url, start_date=None, end_date=None):
    r"""

    Parameters
    ----------

    Returns
    -------

    """
    start_date, end_date = _check_dates(start_date=start_date, end_date=end_date)

    r = requests.get(url,
                     params={
                         'api_key': key,
                         'startDate': start_date,
                         'endDate': end_date
                     })

    limit_remaining = r.headers['X-RateLimit-Remaining']

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.reason, r.url)

    else:
        if r.text == '':

            r = {}
        else:
            r = r.json()

    return limit_remaining, r


def _check_dates(start_date=None, end_date=None):
    r"""

    Parameters
    ----------

    Returns
    -------

    """
    if start_date is not None:
        if not isinstance(start_date, (str, datetime.datetime)):
            raise TypeError('start_date parameter must be a string representing a date in YYYY-MM-DD format or '
                            'a datetime object.')

    if end_date is not None:
        if not isinstance(end_date, (str, datetime.datetime)):
            raise TypeError('end_date parameter must be a string representing a date in YYYY-MM-DD format or '
                            'a datetime object.')

        if isinstance(end_date, datetime.datetime):
            end_date = end_date.strftime('%Y-%m-%d')

    if isinstance(start_date, datetime.datetime):
        start_date = start_date.strftime('%Y-%m-%d')

    return start_date, end_date
