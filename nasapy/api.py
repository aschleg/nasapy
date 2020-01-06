# encoding=utf-8

"""

"""


import datetime
from urllib.parse import urljoin
from pandas import DataFrame

import requests


class Nasa(object):
    r"""
    Class object containing the methods for interacting with NASA API endpoints that require an API key.

    Parameters
    ----------
    key : str, default None
        The generated API key received from the NASA API. Registering for an API key can be done on the `NASA API
        webpage <https://api.nasa.gov/>`_. If :code:`None`, a 'DEMO_KEY' with a much more restricted access limit
        is used.

    Attributes
    ----------
    key : str, None
        The specified key when initializing the class.
    limit_remaining : int
        The number of API calls available.
    mars_weather_limit_remaining : int
        The number of API calls available for the :code:`mars_weather` method.

    Methods
    -------
    picture_of_the_day
        Returns the URL and other information for the NASA Picture of the Day.
    mars_weather
        Returns per-Sol (Martian Days) summary data for each of the last seven available Sols.
    asteroid_feed
        Returns a list of asteroids based on their closest approach date to Earth.
    get_asteroids
        Returns data from the overall asteroid data-set or specific asteroids given an ID.
    coronal_mass_ejection
        Returns data collected on coronal mass ejection events from the Space Weather Database of Notifications,
        Knowledge, Information (DONKI).
    geomagnetic_storm
        Returns data collected on geomagnetic storm events from the Space Weather Database of Notifications, Knowledge,
        Information (DONKI).
    interplantary_shock
        Returns data collected on interplantary shock events from the Space Weather Database of Notifications,
        Knowledge, Information (DONKI).
    solar_flare
        Returns data on solar flare events from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI).
    solar_energetic_particle
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API related to solar energetic particle events.
    magnetopause_crossing
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API related to magnetopause crossing events.
    radiation_belt_enhancement
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API related to radiation belt enhancement events.
    hight_speed_stream
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API related to hight speed stream events.
    wsa_enlil_simulation
        Returns data available from the Space Weather Database of Notifications, Knowledge, Information
        (DONKI) API.
    epic
        The EPIC API provides data on the imagery collected by the DSCOVR's Earth Polychromatic Imaging Camera
        (EPIC).
    earth_imagery
        Retrieves the URL and other information from the Landsat 8 image database for the specified lat/lon location
        and date.
    earth_assets
        Retrieves the datetimes and asset names of available imagery for a specified lat-lon location over a given
        date range. The satellite that takes the images passes over each point approximately once every sixteen days.
    mars_rover
        Retrieves image data collected by the Mars rovers Curiosity, Discovery and Spirit.
    genelab_search
        Retrieves available data from the GeneLab and other bioinformatics databases such as the National Institutes
        of Health (NIH) / National Center for Biotechnology Information (NCBI), Gene Expression Omnibus (GEO), the
        European Bioinformatics Institute's (EBI) Proteomics Identification (PRIDE), and the Argonne National
        Laboratory's (ANL) Metagenomics Rapid Annotations using Subsystems Technology (MG-RAST).
    techport
        Retrieves available NASA project data.

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
        Returns the URL and other information for the NASA Astronomy Picture of the Day.

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
                raise TypeError('date parameter must be a string representing a date in YYYY-MM-DD format or a '
                                'datetime object.')

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

        Notes
        -----
        All the data is from the NASA JPL Asteroid team (http://neo.jpl.nasa.gov/). The API is maintained by the
        `SpaceRocks team <https://github.com/SpaceRocks/>`_

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

        Notes
        -----
        All the data is from the NASA JPL Asteroid team (http://neo.jpl.nasa.gov/). The API is maintained by the
        `SpaceRocks team <https://github.com/SpaceRocks/>`_

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

    def epic(self, color='natural', date=None, available=False):
        r"""
        The EPIC API provides data on the imagery collected by the DSCOVR's Earth Polychromatic Imaging Camera
        (EPIC).

        Parameters
        ----------
        color : str, {'natural', 'enhanced'}
            Specifies the type of imagery to return. Must be one of 'natural' (default) or 'enhanced'
        date : str, datetime, default None
            String representing a date in 'YYYY-MM-DD' format or a datetime object
        available : bool, default False
            Alternative listing of all dates with specified color imagery

        Raises
        ------
        TypeError
            Raised if parameter :code:`available` is not boolean (True or False).
        TypeError
            Raised if parameter :code:`date` is not a string or a datetime object.
        ValueError
            Raised if parameter :code:`color` is not one of 'natural' or 'enhanced'

        Returns
        -------
        list
            List of dictionaries representing the returned JSON data from the EPIC API.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Get EPIC data from the beginning of 2019.
        >>> e = n.epic(date='2019-01-01')
        # Print the first result
        >>> e[0]
        {'identifier': '20190101015633',
         'caption': "This image was taken by NASA's EPIC camera onboard the NOAA DSCOVR spacecraft",
         'image': 'epic_RGB_20190101015633',
         'version': '02',
         'centroid_coordinates': {'lat': -27.281877, 'lon': 155.325443},
         'dscovr_j2000_position': {'x': 350941.733992,
          'y': -1329357.949188,
          'z': -711000.841667},
         'lunar_j2000_position': {'x': -281552.637877,
          'y': -263898.385852,
          'z': 34132.662255},
         'sun_j2000_position': {'x': 25746688.614416,
          'y': -132882102.563308,
          'z': -57603901.841971},
         'attitude_quaternions': {'q0': 0.621256,
          'q1': 0.675002,
          'q2': 0.397198,
          'q3': 0.025296},
         'date': '2019-01-01 01:51:44',
         'coords': {'centroid_coordinates': {'lat': -27.281877, 'lon': 155.325443},
          'dscovr_j2000_position': {'x': 350941.733992,
           'y': -1329357.949188,
           'z': -711000.841667},
          'lunar_j2000_position': {'x': -281552.637877,
           'y': -263898.385852,
           'z': 34132.662255},
          'sun_j2000_position': {'x': 25746688.614416,
           'y': -132882102.563308,
           'z': -57603901.841971},
          'attitude_quaternions': {'q0': 0.621256,
           'q1': 0.675002,
           'q2': 0.397198,
           'q3': 0.025296}}}

        Notes
        -----
        If a :code:`date` is not given and :code:`available` is :code:`False`, a listing of all dates with the
        specified color imagery is returned using the :code:`all` endpoint of the EPIC API.

        The EPIC API provides information on the daily imagery collected by DSCOVR's Earth Polychromatic Imaging
        Camera (EPIC) instrument. Uniquely positioned at the Earth-Sun Lagrange point, EPIC provides full disc
        imagery of the Earth and captures unique perspectives of certain astronomical events such as lunar transits
        using a 2048x2048 pixel CCD (Charge Coupled Device) detector coupled to a 30-cm aperture Cassegrain telescope.

        """
        url = self.host + '/EPIC/api/'

        if color not in ('natural', 'enhanced'):
            raise ValueError("color parameter must be 'natural' (default), or 'enhanced'.")

        if not isinstance(available, bool):
            raise TypeError('available parameter must be boolean (True or False).')

        if date is not None:
            if not isinstance(date, (str, datetime.datetime)):
                raise TypeError("date parameter must be a string representing a date in YYYY-MM-DD format or a "
                                "datetime object.")

            if isinstance(date, datetime.datetime):
                date = date.strftime('%Y-%m-%d')

            url = url + '{color}/date/{date}'.format(date=date, color=color)

        elif available:
            url = url + '{color}/available'.format(color=color)

        else:
            url = url + '{color}/all'.format(color=color)

        r = requests.get(url,
                         params={'api_key': self.__api_key})

        if r.status_code != 200 or r.text == '':
            r = {}
        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']
            r = r.json()

        return r

    def earth_imagery(self, lat, lon, dim=0.025, date=None, cloud_score=False):
        r"""
        Retrieves the URL and other information from the Landsat 8 image database for the specified lat/lon location
        and date.

        Parameters
        ----------
        lat : int, float
            Latitude of the desired imagery location
        lon : int, float
            Longitude of the desired imagery location
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
        # Get imagery at latitude 1.5, longitude 100.75 and include the computed cloud score calculation.
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
            Latitude of the desired imagery location
        lon : int, float
            Longitude of the desired imagery location
        begin_date : str, datetime
            Beginning of date range in which to search for available assets. Must be a string representing a date in
            'YYYY-MM-DD' format or a datetime object
        end_date : str, datetime, default None
            End of date range in which to search for available assets. If not specified, defaults to the current date.
            If specified, Must be a string representing a date in 'YYYY-MM-DD' format or a datetime object

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

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Get assets available beginning from 2014-02-01 at lat-lon 100.75, 1.5
        >>> n.earth_assets(lat=100.75, lon=1.5, begin_date='2014-02-01')

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

    def mars_rover(self, sol=None, earth_date=None, camera='all', rover='curiosity', page=1):
        r"""
        Retrieves image data collected by the Mars rovers Curiosity, Discovery and Spirit.

        Parameters
        ----------
        sol : int, None (default)
            The sol (Martian rotation or day) on which the images were collected. Either this parameter or
            :code:`earth_date` must be provided. The parameter :code:`earth_date` is an alternative parameter for
            searching for a specific date. The sol values count up from the rover's landing date, for example, the
            Curiosity's 100th sol would be the 100th Martian rotation since the rover landed.
        earth_date : str, datetime, None (default)
            Alternative search parameter for finding data on a specific date. Must be a string representing a date
            in 'YYYY-MM-DD' format or a datetime object. Either :code:`earth_date` or :code:`sol` must be specified.
        camera : str, {'all', FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', 'MAHLI', 'MARDI', 'NAVCAM', 'PANCAM', 'MINITES'}
            Filter results to a specific camera on the Mars Curiosity, Opportunity or Spirit rovers. Defaults to 'all',
            which includes all cameras.
        rover : str, {'curiosity', 'opportunity', 'spirit'}
            Specifies the Mars rover to return data. Defaults to the Curiosity rover which has more available cameras.
        page : int, default 1
            Page number of results to return. 25 results per page are returned.

        Raises
        ------
        ValueError
            Raised if both :code:`sol` and :code:`earth_date` parameters are not specified.
        ValueError
            Raised if the :code:`camera` parameter is not one of 'all' (default), 'FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', "
            "'MAHLI', 'MARDI', 'NAVCAM', 'PANCAM', or 'MINITES'
        ValueError
            Raised if :code:`rover` parameter is not one of 'curiosity' (default), 'opportunity', 'spirit'
        TypeError
            Raised if :code:`earth_date` (if provided) is not a string or a datetime object.

        Returns
        -------
        list
            List of dictionaries representing the returned JSON data from the Mars Rover API.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Return image data collected on Curiosity's 1000th sol.
        >>> r = n.mars_rover(sol=1000)
        # Print the first result in the list collection.
        {'id': 102693,
         'sol': 1000,
         'camera': {'id': 20,
          'name': 'FHAZ',
          'rover_id': 5,
          'full_name': 'Front Hazard Avoidance Camera'},
         'img_src': 'http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FLB_486265257EDR_F0481570FHAZ00323M_.JPG',
         'earth_date': '2015-05-30',
         'rover': {'id': 5,
          'name': 'Curiosity',
          'landing_date': '2012-08-06',
          'launch_date': '2011-11-26',
          'status': 'active',
          'max_sol': 2540,
          'max_date': '2019-09-28',
          'total_photos': 366206,
          'cameras': [{'name': 'FHAZ', 'full_name': 'Front Hazard Avoidance Camera'},
           {'name': 'NAVCAM', 'full_name': 'Navigation Camera'},
           {'name': 'MAST', 'full_name': 'Mast Camera'},
           {'name': 'CHEMCAM', 'full_name': 'Chemistry and Camera Complex'},
           {'name': 'MAHLI', 'full_name': 'Mars Hand Lens Imager'},
           {'name': 'MARDI', 'full_name': 'Mars Descent Imager'},
           {'name': 'RHAZ', 'full_name': 'Rear Hazard Avoidance Camera'}]}}

        """
        if str.lower(rover) not in ('curiosity', 'opportunity', 'spirit'):
            raise ValueError("rover parameter must be one of 'curiosity' (default), 'opportunity', or 'spirit'.")

        if camera not in ['FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', 'MAHLI', 'MARDI', 'NAVCAM', 'PANCAM', 'MINITES', 'all']:
            raise ValueError("camera parameter must be one of 'all' (default), 'FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', "
                             "'MAHLI', 'MARDI', 'NAVCAM', 'PANCAM', or 'MINITES'")

        url = self.host + '/mars-photos/api/v1/rovers/{rover}/photos'.format(rover=str.lower(rover))

        params = {
            'page': page,
            'api_key': self.__api_key
        }

        if camera != 'all':
            params['camera'] = camera

        if sol is not None and earth_date is not None:
            raise ValueError('either the sol or earth_date parameter should be specified, not both.')

        elif sol is not None:
            params['sol'] = sol

        elif earth_date is not None:
            if not isinstance(earth_date, (str, datetime.datetime)):
                raise TypeError('end date parameter must be a string representing a date in YYYY-MM-DD format or a '
                                'datetime object.')

            if isinstance(earth_date, datetime.datetime):
                earth_date = earth_date.strftime('%Y-%m-%d')

            params['earth_date'] = earth_date

        r = requests.get(url,
                         params=params)

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.__limit_remaining = r.headers['X-RateLimit-Remaining']

        return r.json()['photos']

    def genelab_search(self, term=None, database='cgene', page=0, size=25, sort=None, order='desc',
                       ffield=None, fvalue=None):
        r"""
        Retrieves available data from the GeneLab and other bioinformatics databases such as the National Institutes
        of Health (NIH) / National Center for Biotechnology Information (NCBI), Gene Expression Omnibus (GEO), the
        European Bioinformatics Institute's (EBI) Proteomics Identification (PRIDE), and the Argonne National
        Laboratory's (ANL) Metagenomics Rapid Annotations using Subsystems Technology (MG-RAST).

        Parameters
        ----------
        term : str, default None
            Search by specific keyword(s). Case-insensitive boolean operators (AND, OR, NOT) can be used as well
            to include and filter specific keywords.
        database : str, {'cgene', 'nih_geo_gse', 'ebi_pride', 'mg_rast'}
            Determines the database(s) to query. Defaults to the 'cgene' (GeneLab) database, but other available
            databases include 'nih_geo_gse' (NIH GEO), 'ebi_pride' (EBI PRIDE), or 'mg_rast' (MG-RAST). Multiple
            databases can be queried by separating values with commas. For example,
            'cgene,nih_geo_gse,ebi_pride,mg_rast' will query all available databases.
        page : int, default 0
            Specifies the page of results to return. Defaults to the first page (0).
        size : int, default 25
            Specifies the number of results to return per page. Default is 25 results per page.
        sort : str, default None
            Sorts by a specific field name in the returned JSON data.
        order : str, {'desc', 'asc'}
            Determines the sorting order. Must be one of 'desc' (descending) or 'asc' (ascending).
        ffield : str, default None
            Filters the returned data based on the defined field. Should be paired with the :code:`fvalue` parameter.
            Only the 'cgene' (GeneLab) database can be filtered.
        fvalue : str, default None
            Filters the returned data based on value or values in the specified :code:`ffield` parameter field. Only
            the 'cgene' (GeneLab) database can be filtered.

        Raises
        ------
        ValueError
            Raised if :code:`order` parameter is not one of 'desc' (default), or 'asc'.
        ValueError
            Raised if :code:`page` parameter is less than 0.
        ValueError
            Raised if :code:`size` parameter is 0 or less.
        HTTPError
            Raised if result does not have a 200 status code.

        Returns
        -------
        dict
            Dictionary object representing the returned JSON data.

        Examples
        --------
        # Initialize API connection with a Demo Key
        >>> n = Nasa()
        # Find Gene studies in the cgene database related to 'mouse liver'
        >>> n.genelab_search(term='mouse liver')

        Notes
        -----
        The `GeneLab public data repository <https://genelab-data.ndc.nasa.gov/genelab/projects>`_ provides the same
        functionality as the API in a searchable HTML interface. For more information on the available bioinformatics
        databases, please see the following links:
        `Gene Expression Omnibus (GEO) <https://www.ncbi.nlm.nih.gov/geo/>`_
        `European Bioinformatics Institute (EBI) <https://www.ebi.ac.uk/pride/archive/>`_
        `Argonne National Laboratory's (ANL) <http://www.mg-rast.org>`_

        """
        url = 'https://genelab-data.ndc.nasa.gov/genelab/data/search'

        if order not in ('desc', 'asc'):
            raise ValueError('order parameter must be "desc" (descending, default), or "asc" (ascending)')

        if page < 0:
            raise ValueError('page parameter must be at least 0 (start)')

        if size <= 0:
            raise ValueError('size of results to return cannot be 0 or less.')

        params = {
            'term': term,
            'sort': sort,
            'type': database,
            'from': page,
            'size': size,
            'order': str.upper(order),
            'ffield': ffield,
            'fvalue': fvalue,
            'api_key': self.__api_key
        }

        r = _return_api_result(url=url, params=params)

        return r

    def techport(self, project_id=None, last_updated=None, return_format='json'):
        r"""
        Retrieves available NASA project data.

        Parameters
        ----------
        project_id : str, int, default None
            The ID of the project record. If not specified, all available projects will be returned.
        last_updated : str, datetime
            Returns projects only updated after the specified date. Must be a string representing a date in
            'YYYY-MM-DD' format or a datetime object.
        return_format : str, {'json', 'xml'}
            Specifies the return format of the data. Defaults to 'json', but 'xml' formatted data is also available.

        Raises
        ------
        ValueError
            Raised if :code:`return_foramt` is not one of 'json' (default) or 'xml'.
        TypeError
            Raised if :code:`last_updated` is not a string or a datetime object.

        Returns
        -------
        dict or str
            If :code:`return_format` is 'json', a dictionary representing the JSON formatted data is returned.
            Otherwise, a string formatted for XML is returned.

        """
        url = self.host + '/techport/api/projects/'

        if return_format not in ('json', 'xml'):
            raise ValueError("type parameter must be one of 'json' (default), or 'xml'.")

        if last_updated is not None:
            if not isinstance(last_updated, (str, datetime.datetime)):
                raise TypeError('end date parameter must be a string representing a date in YYYY-MM-DD format or a '
                                'datetime object.')

            if isinstance(last_updated, datetime.datetime):
                last_updated = last_updated.strftime('%Y-%m-%d')

        if project_id is None:
            r = requests.get(url,
                             params={'updatedSince': last_updated,
                                     'api_key': self.__api_key})
        else:
            url = url + '{project_id}'.format(project_id=project_id)

            if return_format == 'xml':
                url = url + '.xml'

            r = requests.get(url,
                             params={'api_key': self.__api_key})

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        self.__limit_remaining = r.headers['X-RateLimit-Remaining']

        if return_format == 'xml':
            r = r.text
        else:
            r = r.json()

        return r

    # def mars_mission_manifest(self, rover):
    #     url = self.host + '/mars-photos/api/manifests/{rover}'.format(rover=rover)
    #
    #     r = requests.get(url)
    #
    #     return r

    # def patents(self, query, concept_tags=False, limit=None):
    #     url = self.host + '/patents/content'
    #
    #     if limit is not None:
    #         if not isinstance(limit, int):
    #             raise TypeError('limit parameter must None (return all results) or an int.')
    #
    #     if not isinstance(concept_tags, bool):
    #         raise TypeError('concept_tags parameter must be boolean (True or False).')
    #
    #     r = requests.get(url,
    #                      params={
    #                          'query': query,
    #                          'limit': limit,
    #                          'api_key': self.__api_key
    #                      })
    #
    #     if r.status_code != 200 or r.text == '':
    #         r = {}
    #     else:
    #         self.__limit_remaining = r.headers['X-RateLimit-Remaining']
    #         r = r.json()
    #
    #     return r


def exoplanets(table='exoplanets', select=None, count=None, colset=None, where=None, order=None, ra=None, dec=None,
               aliastable=None, objname=None, return_df=False):
    r"""
    Provides access to NASA's Exoplanet Archive.

    Parameters
    ----------
    table : str, default 'exoplanets'
        Specifies which table to query.
    select : str
        Specifies which columns within the chosen table to return. Multiple columns can be returned by comma-separating
        the column names and distinct values can be returned by adding 'distinct ' in front of the desired column
        names.
    count : str
        Can be used to return the number of rows which fulfill the given query, including queries using where
        clauses or cone searches.
    colset : str
        Returns a set of pre-defined columns that have been created by the archive. Currently, this keyword is only
        used by the Composite Planet Data ('compositepars') table.
    where : str
        Takes a SQL-like query string to filter the returned results. Please see the examples section for more.
    order : str
        Returns the data sorted by the specified column. Append ' desc' for descending or ' asc' for ascending values.
    ra : str
        Specifies an area of the sky to search for all objects within that area.
    dec : str
        Specifies an area of the sky to search for all objects within that area.
    aliastable : str
        Requests a list of aliases for a particular confirmed planet.
    objname : str
        When parameter `aliastable` is specified, `objname` must also be passed with the planet's name.
    return_df : bool, default False
        If `True`, returns the JSON data as a pandas DataFrame.

    Returns
    -------
    dict or pandas DataFrame
        If parameter `return_df` is `True`, a pandas DataFrame of the returned results. Otherwise, a dictionary
        representing the returned JSON data from the API is returned.

    Examples
    --------
    # Get all exoplanets data as a pandas DataFrame.
    >>> exoplanets(return_df=True)
    # Get all confirmed planets in the Kepler field.
    >>> exoplanets(where='pl_kepflag=1')
    # Stars known to host exoplanets as a pandas DataFrame.
    >>> exoplanets(select='distinct pl_hostname', order='pl_hostname', return_df=True)

    """
    host = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?'

    r = requests.get(host,
                     params={
                         'table': table,
                         'select': select,
                         'count': count,
                         'colset': colset,
                         'where': where,
                         'order': order,
                         'ra': ra,
                         'dec': dec,
                         'aliastable': aliastable,
                         'objname': objname,
                         'format': 'json'
                     }).json()

    if return_df:
        r = DataFrame(r)

    return r


def tle(search_satellite=None, satellite_number=None):
    r"""
    Returns two-line element set records provided by CelesTrak. A two-line element set (TLE) is a data format
    encoding a list of orbital elements of an Earth-orbiting object for a given point in time.

    Parameters
    ----------
    search_satellite : str, default None
        Searches satellites by name designation.
    satellite_number : str, int, default None
        Specfic satellite ID number.

    Returns
    -------
    dict
        Dictionary object representing the returned JSON data.

    Examples
    --------
    # The TLE endpoint does not require API authentication, thus we can call the function without initializing the
    # Nasa class. Retrieve available data for a specific satellite ID.
    >>> tle(satellite_number=43553)
    {'@id': 'https://data.ivanstanojevic.me/api/tle/43553',
     '@type': 'TleModel',
     'satelliteId': 43553,
     'name': '1998-067PB',
     'date': '2019-10-14T19:13:21+00:00',
     'line1': '1 43553U 98067PB  19287.80094257  .00010817  00000-0  12491-3 0  9999',
     'line2': '2 43553  51.6389 108.1812 0005967 223.4274 136.6250 15.62481474 71504'}

    """
    url = 'https://data.ivanstanojevic.me/api/tle'

    if search_satellite is not None:
        r = requests.get(url,
                         params={'search': search_satellite})

    elif satellite_number is not None:
        url = url + '/{satellite_number}'.format(satellite_number=satellite_number)

        r = requests.get(url)

    else:
        r = requests.get(url)

    if r.status_code == 404:
        raise requests.exceptions.HTTPError(r.json()['response']['message'])

    return r.json()


def media_search(query=None, center=None, description=None, keywords=None, location=None, media_type=None,
                 nasa_id=None, page=1, photographer=None, secondary_creator=None, title=None, year_start=None,
                 year_end=None):
    r"""
    Performs a general search for media from the images.nasa.gov API based on parameters and criteria specified.
    At least one parameter must be provided.

    Parameters
    ----------
    query : str, None (default)
        Query terms to search.
    center : str, None (default)
        NASA center that published the results.
    description :  str, None (default)
        Search and filter for specific terms in the 'description' field of the resulting data.
    keywords : str, None (default)
        Search and filter for specific terms in the 'keywords' field of the resulting data. Multiple values should be
        comma-separated.
    location : str, None (default)
        Search for terms in the 'locations' field of the resulting data.
    media_type : str, {None, 'image', 'audio', 'image,audio', 'audio,image'}
        Filter results to specific media types. Options include 'image', 'audio', 'image,audio', 'audio,image'.
        The default :code:`None` includes all media types.
    nasa_id : str, None (default)
        The media asset's NASA ID.
    page : int, 1 (default)
        Page number of results to return. Starts at 1.
    photographer : str, None (default)
        The primary photographer's name.
    secondary_creator : str, None (default)
        A secondary photographer/videographer's name.
    title : str, None (default)
        Search terms in the 'title' field of the resulting data.
    year_start : str, datetime, None (default)
        The start year for results. If provided, must be a string representing a year in YYYY format or a
        datetime object.
    year_end : str, datetime, None (default)
        The end year for results. If provided, must be a string representing a year in YYYY format or a
        datetime object.

    Raises
    ------
    ValueError
        Raised if no parameters are specified.
    ValueError
        Raised if the :code:`media_type` parameter is not one of 'image', 'audio', 'image,audio', 'audio,image'
        (if specified).
    TypeError
        Raised if :code:`year_start` parameter (if provided) is not a string or a datetime object.
    TypeError
        Raised if :code:`year_end` parameter (if provided) is not a string or a datetime object.

    Returns
    -------
    dict
        Dictionary containing matching search results.

    Examples
    --------
    # Search for media related to 'apollo 11' with 'moon landing' in the description of the items.
    >>> r = media_search(query='apollo 11', description='moon landing')
    # Print the first returned media item from the resulting collection.
    >>> r['items'][0]
    {'href': 'https://images-assets.nasa.gov/video/Apollo 11 Overview/collection.json',
     'data': [{'description': 'Video highlights from the historic first manned landing on the moon, during the Apollo 11 mission in July 1969.',
       'date_created': '2013-05-15T00:00:00Z',
       'nasa_id': 'Apollo 11 Overview',
       'media_type': 'video',
       'keywords': ['Apollo 11', 'Moon'],
       'center': 'HQ',
       'title': 'Apollo 11 Overview'}],
     'links': [{'href': 'https://images-assets.nasa.gov/video/Apollo 11 Overview/Apollo 11 Overview~thumb.jpg',
       'rel': 'preview',
       'render': 'image'},
      {'href': 'https://images-assets.nasa.gov/video/Apollo 11 Overview/Apollo 11 Overview.srt',
       'rel': 'captions'}]}

    """
    url = 'https://images-api.nasa.gov/search'

    if all(p is None for p in (query, center, description, keywords, location, media_type, nasa_id,
                               photographer, secondary_creator, title, year_start, year_end)):
        raise ValueError('at least one parameter is required')

    if media_type is not None:
        if media_type not in ('image', 'audio', 'image,audio', 'audio,image'):
            raise ValueError("media_type parameter must be one of 'image' or 'audio' or a combination of both "
                             "('image,audio' or 'audio,image'.")

    if year_start is not None:
        if not isinstance(year_start, (str, datetime.datetime)):
            raise TypeError('year start parameter must be a string representing a year in YYYY format or a '
                            'datetime object.')

        if isinstance(year_start, datetime.datetime):
            year_start = year_start.strftime('%Y')

    if year_end is not None:
        if not isinstance(year_end, (str, datetime.datetime)):
            raise TypeError('year end parameter must be a string representing a year in YYYY format or a '
                            'datetime object.')

        if isinstance(year_end, datetime.datetime):
            year_end = year_end.strftime('%Y')

    params = {
        'q': query,
        'center': center,
        'description': description,
        'keywords': keywords,
        'location': location,
        'media_type': media_type,
        'nasa_id': nasa_id,
        'page': page,
        'photographer': photographer,
        'secondary_creator': secondary_creator,
        'title': title,
        'year_start': year_start,
        'year_end': year_end
    }

    r = _return_api_result(url=url, params=params)

    return r['collection']


def media_asset_manifest(nasa_id):
    r"""
    Returns the media asset's manifest, which contains the available versions of the asset and it's metadata
    location.

    Parameters
    ----------
    nasa_id : str
        The ID of the media asset.

    Returns
    -------
    list
        List of dictionaries containing the media asset's manifest.

    Examples
    --------
    # Get the manifest for the NASA media asset 'as11-40-5874'
    >>> media_asset_manifest(nasa_id='as11-40-5874')
    [{'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~orig.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~large.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~medium.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~small.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~thumb.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/metadata.json'}]

    """
    return _media_assets(endpoint='asset', nasa_id=nasa_id)


def media_asset_metadata(nasa_id):
    r"""
    Retrieves the specified media asset's metadata.

    Parameters
    ----------
    nasa_id : str
        The ID of the media asset.

    Returns
    -------
    dict
        Dictionary containing the metadata of the provided media asset ID.

    """
    return _media_assets(endpoint='metadata', nasa_id=nasa_id)


def media_asset_captions(nasa_id):
    r"""
    Retrieves the captions and location of the captions .srt file for a media asset from the NASA image API.

    Parameters
    ----------
    nasa_id : str
        The ID of the media asset.

    Returns
    -------
    dict
        Dictionary object containing the resulting data from the API given the media asset ID. The dictionary will
        contain two keys, :code:`location` and :code:`captions`. The :code:`location` key can be used to
        download the .srt file directly while the :code:`captions` key can be used in conjunction with a library
        such as srt for parsing media asset captions.

    """
    return _media_assets(endpoint='captions', nasa_id=nasa_id)


def close_approach(date_min='now', date_max='+60', dist_min=None, dist_max='0.05', h_min=None, h_max=None,
                   v_inf_min=None, v_inf_max=None, v_rel_min=None, v_rel_max=None, orbit_class=None, pha=False,
                   nea=False, comet=False, nea_comet=False, neo=False, kind=None, spk=None, des=None,
                   body='Earth', sort='date', limit=None, fullname=False, return_df=False):
    r"""
    Provides data for currently known close-approach data for all asteroids and comets in NASA's Jet Propulsion
    Laboratory's (JPL) Small-Body Database.

    Parameters
    ----------
    date_min : str, datetime, default 'now'
        Excludes data earlier than the given date. Defaults to 'now', representing the current date, but can also be
        a string representing a date in 'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    date_max :'str, datetime, 'now', default '+60'
        Excludes data later than the given date. Defaults to '+60', representing 60 days after the :code:`date_min`
        parameter. Accepts a string of '+D' where D represents the number of days or a string representing a date in
        'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object. 'now' is also an acceptable value
        and will exclude date later than the current date.
    dist_min : str, float, int, default None
        Excludes data with an approach distance less than the given value (if provided). The default unit is AU
        (astronomical units), and LD (lunar distance) is also available. For example, '0.05' or 0.05 would return
        AU units whereas '0.05LD' would return LD units.
    dist_max : str, float int, default None
        Excludes data with an approach distance greater than the given value (if specified). The default unit is AU
        (astronomical units), and LD (lunar distance) is also available. For example, '0.05' would return AU units
        whereas '0.05LD' would return LD units.
    h_min : float, int, default None
        Exclude data from objects with H-values less than the given value.
    h_max : float, int, default None
        Exclude data from objects with H-values greater than the given value.
    v_inf_min : float, int, default None
        Exclude data with V-infinity less than this positive value in km/s
    v_inf_max : float, int, default None
        Exclude data with V-infinity greater than this positive value in km/s
    v_rel_min : float, int, default None
        Exclude data with V-relative less than this positive value in km/s
    v_rel_max : float, int, default None
        Exclude data with V-relative greater than this positive value in km/s
    orbit_class : str
        Limits data to specified orbit-class
    pha : bool, default False
        If True, limits the resulting data to only PHA objects
    nea : bool, default False
        If True, limits the returned data to only NEA objects
    comet : bool, default False
        If True, limits the returned data to comet objects only
    nea_comet : bool, default False
        If True, limits the returned data to NEA comet objects only
    neo : bool, default False
        If True, limits the returned data to only NEO objects
    kind : str, {'a', 'an', 'au', 'c', 'cn', 'cu', 'n', 'u'}, default None
        Filters returned data to specified type of object. Available options include 'a'=asteroid,
        'an'=numbered-asteroids, 'au'=unnumbered-asteroids, 'c'=comets, 'cn'=numbered-comets, 'cu'=unnumbered-comets,
        'n'=numbered-objects, and 'u'=unnumbered-objects
    spk : str, int, default None
        Return data only for the matching SPK-ID.
    des : str, default None
        Filters data to objects matching the given destination.
    body : str, default "Earth"
        Filters data to close-approaches of the specified body. 'ALL' or '*' returns all close-approaches to the
        available bodies.
    sort : str, {'date', 'dist', 'dist-min', 'v-inf', 'v-rel', 'h', 'object'}
        Sorts the returned data by the specified field. Defaults to 'date' ascending. To sort by descending, add a '-'
        in front of the sort value, for example, '-date'.
    limit : int, default None
        Limit data to the first number of results specified by the parameter. Must be greater than 0.
    fullname : bool, default False
        Includes the full-format object name/designation
    return_df : bool, default False
        If True, returns the 'data' field of the returned JSON data as a pandas DataFrame with column names extracted
        from the 'fields' key of the returned JSON.

    Raises
    ------
    ValueError
        Raised if :code:`h_min` is greater than :code:`h_max`
    ValueError
        Raised if :code:`v_inf_min` parameter is greater than :code:`v_inf_max`
    ValueError
        Raised if :code:`v_rel_min` parameter is greater than :code:`v_rel_max`
    ValueError
        Raised if :code:`limit` parameter is 0 or less.
    TypeError
        Raised if :code:`limit` parameter is not an integer (if specified)
    TypeError
        Raised if :code:`pha` is not boolean (True or False)
    TypeError
        Raised if :code:`nea` is not boolean (True or False)
    TypeError
        Raised if :code:`comet` is not boolean (True or False)
    TypeError
        Raised if :code:`neo` is not boolean (True or False)
    TypeError
        Raised if :code:`fullname` is not boolean (True or False)
    HTTPError
        Raised if the returned status code of the resulting data is not 200 (success)

    Returns
    -------
    dict
        Dictionary object representing the returned JSON data from the API.

    Examples
    --------
    # Get all close-approach object data in the year 2019 with a maximum approach distance of 0.01AU.
    >>> close_approach(date_min='2019-01-01', date_max='2019-12-31', dist_max=0.01)
    # Get close-approach data for asteroid 433 Eros within 0.2AU from the years 1900 to 2100.
    >>> close_approach(des='433', date_min='1900-01-01', date_max='2100-01-01', dist_max=0.2)
    # Return close-approach data from the beginning of 2000 to the beginning of 2020 as a pandas DataFrame.
    >>> close_approach(date_min='2000-01-01', date_max='2020-01-01', return_df=True)

    Notes
    -----
    Each close-approach record is a list containing the following fields in the corresponding order:

    * des - primary designation of the asteroid or comet (e.g., 443, 2000 SG344)
    * orbit_id - orbit ID
    * jd - time of close-approach (JD Ephemeris Time)
    * cd - time of close-approeach (formatted calendar date/time)
    * dist - nominal approach distance (au)
    * dist_min - minimum (3-sigma) approach distance (au)
    * dist_max - maximum (3-sigma) approach distance (au)
    * v_rel - velocity relative to the approach body at close approach (km/s)
    * v_inf - velocity relative to a massless body (km/s)
    * t_sigma_f - 3-sigma uncertainty in the time of close-approach (formatted in days, hours, and minutes;
        days are not included if zero; example “13:02” is 13 hours 2 minutes; example “2_09:08” is 2 days 9 hours 8
        minutes)
    * body - name of the close-approach body (e.g., Earth)
        * only output if the body query parameters is set to ALL
    * h - absolute magnitude H (mag)
    * fullname - formatted full-name/designation of the asteroid or comet
        * optional - only output if requested with the appropriate query flag
        * formatted with leading spaces for column alignment in monospaced font tables

    """
    url = 'https://ssd-api.jpl.nasa.gov/cad.api'

    if date_min != 'now':
        if not isinstance(date_min, (str, datetime.datetime)):
            raise TypeError("date parameter must be a string representing a date in YYYY-MM-DD or YYYY-MM-DDThh:mm:ss "
                            "format, 'now' for the current date, or a datetime object.")

        if isinstance(date_min, datetime.datetime):
            date_min = date_min.strftime('%Y-%m-%dT%H:%M:%S')

    if isinstance(date_max, datetime.datetime):
        date_max = date_max.strftime('%Y-%m-%dT%H:%M:%S')

    if h_min is not None and h_max is not None:
        if h_min > h_max:
            raise ValueError('h_min parameter must be less than h_max')

    if v_inf_min is not None and v_inf_max is not None:
        if v_inf_min > v_inf_max:
            raise ValueError('v_inf_min parameter must be less than v_inf_max')

    if v_rel_min is not None and v_rel_max is not None:
        if v_rel_min > v_rel_max:
            raise ValueError('v_rel_min parameter must be less than v_rel_max')

    if limit is not None:
        if not isinstance(limit, int):
            raise TypeError('limit parameter must be an integer (if specified)')

        elif limit <= 0:
            raise ValueError('limit parameter must be greater than 0')

    if not isinstance(pha, bool):
        raise TypeError('pha parameter must be boolean (True or False)')

    if not isinstance(nea, bool):
        raise TypeError('nea parameter must be boolean (True or False)')

    if not isinstance(comet, bool):
        raise TypeError('comet parameter must be boolean (True or False)')

    if not isinstance(nea_comet, bool):
        raise TypeError('nea_comet parameter must be boolean (True or False)')

    if not isinstance(neo, bool):
        raise TypeError('neo parameter must be boolean (True or False)')

    if not isinstance(fullname, bool):
        raise TypeError('fullname parameter must be boolean (True or False)')

    params = {
        'date-min': date_min,
        'date-max': date_max,
        'dist-min': dist_min,
        'dist-max': dist_max,
        'h-min': h_min,
        'h-max': h_max,
        'v-inf-min': v_inf_min,
        'v-inf-max': v_inf_max,
        'v-rel-min': v_rel_min,
        'v-rel-max': v_rel_max,
        'class': orbit_class,
        'pha': pha,
        'nea': nea,
        'comet': comet,
        'nea-comet': nea_comet,
        'neo': neo,
        'kind': kind,
        'spk': spk,
        'des': des,
        'body': body,
        'sort': sort,
        'limit': limit,
        'fullname': fullname
    }

    r = _return_api_result(url=url, params=params)

    if return_df:
        r = DataFrame(r['data'], columns=r['fields'])

    return r


def fireballs(date_min=None, date_max=None, energy_min=None, energy_max=None, impact_e_min=None, impact_e_max=None,
              vel_min=None, vel_max=None, alt_min=None, alt_max=None, req_loc=False, req_alt=False, req_vel=False,
              req_vel_comp=False, vel_comp=False, sort='date', limit=None, return_df=False):
    r"""
    Returns available data on fireballs (objects that burn up in the upper atmosphere of Earth).

    Parameters
    ----------
    date_min : str, datetime, default None
        Excludes data earlier than the given date. Can be a string representing a date in 'YYYY-MM-DD' format or
        'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    date_max : str, datetime, default None
        Excludes data later than the given date. Can be a string representing a date in 'YYYY-MM-DD' format or
        'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    energy_min : int, float, default None
        Excludes data with total-radiated-energy less than the positive value of the specified value in joules
        :math:`\times 10^{10}`.
    energy_max : int, float, default None
        Excludes data with total-radiated-energy greater than the positive value of the specified value in joules
        :math:`\times 10^{10}`.
    impact_e_min : int, float, default None
        Excludes data with estimated impact energy less than the positive value of the specified value in kilotons (kt)
    impact_e_max : int, float, default None
        Excludes data with estimated impact energy greater than the positive value of the specified value in kilotons
        (kt)
    vel_min : int, float, default None
        Excludes data with velocity-at-peak-brightness less than the positive value of the specified value in km/s
    vel_max : int, float, default None
        Excludes data with velocity-at-peak-brightness greater than the positive value of the specified value in km/s
    alt_min : int, float, default None
        Excludes data from objects with an altitude less than the specified value
    alt_max : int, float, default None
        Excludes data from objects with an altitude greater than the specified value
    req_loc : bool, default False
        If True, latitude and longitude required for object to be included in results.
    req_alt : bool, default False
        If True, objects without an altitude are excluded.
    req_vel : bool, default False
        If True, objects without a velocity are not included in results.
    req_vel_comp : bool, default False
        If True, excludes objects without velocity components
    vel_comp : bool, default False
        If True, include velocity components
    sort : str, {'date', 'energy', 'impact-e', 'vel', 'alt'}
        Sorts data on specified field. Default sort order is ascending, for descending, prepend a '-'. For example,
        for date descending, the sort value would be '-date'.
    limit : int, default None
        Limits data to the first number of results specified. Must be greater than 0 if passed.
    return_df : bool, default False
        If True, returns the 'data' field of the returned JSON data as a pandas DataFrame with column names extracted
        from the 'fields' key of the returned JSON.

    Raises
    ------
    TypeError
        Raised if :code:`date_min` parameter is not a string representing a date or dateimt or a datetime object.
    TypeError
        Raised if :code:`date_max` parameter is not a string representing a date or dateimt or a datetime object.
    TypeError
        Raised if :code:`req_loc` parameter is not boolean (if specified)
    TypeError
        Raised if :code:`req_alt` parameter is not boolean (if specified)
    TypeError
        Raised if :code:`req_vel` parameter is not boolean (if specified)
    TypeError
        Raised if :code:`req_vel_comp` parameter is not boolean (if specified)
    TypeError
        Raised if :code:`vel_comp` parameter is not boolean (if specified)
    TypeError
        Raised if :code:`limit` parameter is not an integer
    ValueError
        Raised if :code:`vel_min` parameter is greater than :code:`vel_max` parameter (if both are specified).
    ValueError
        Raised if :code:`alt_min` parameter is greater than :code:`alt_max` parameter (if both are specified).
    ValueError
        Raised if :code:`limit` parameter is 0 or less

    Returns
    -------
    dict
        Dictionary object representing the returned JSON results from the API.

    Examples
    --------
    # Get all available data in reverse chronological order
    >>> n = fireballs()
    # Return the earlieset record
    >>> fireballs(limit=1)
    # Get data from the beginning of 2019
    >>> fireballs(date_min='2019-01-01')
    # Return fireball data from the beginning of the millennium to the beginning of 2020 as a pandas DataFrame.
    >>> fireballs(date_min='2000-01-01', date_max='2020-01-01', return_df=True)

    Notes
    -----
    Each returned record is provided as an element of the object and each record is a list of fields corresponding to
    the fields below. The names of each field contained in the returned results in each record can also be found in the
    'fields' key of the returned dictionary.

    * date - date/time of peak brightness (GMT)
    * lat - latitude at peak brightness (degrees)
    * lon - longitude at peak brightness (degrees)
    * lat-dir - latitude direction (“N” or “S”)
    * lon-dir - latitude direction (“E” or “W”)
    * alt - altitude above the geoid at peak brightness (km)
    * vel - velocity at peak brightness (km/s)
    * energy - approximate total radiated energy (1010 joules)
    * impact-e - approximate total impact energy (kt)
    * vx - pre-entry estimated velocity (Earth centered X component, km/s)
    * vy - pre-entry est. velocity (Earth centered Y component, km/s)
    * vz - pre-entry est. velocity (Earth centered Z component, km/s)

    Note that many fields can be undefined (null) in a particular data record. The only fields which are guaranteed
    to be defined are `date`, `energy`, and `impact-e`. Where the location is known, all four related fields
    (`lat`, `lat-dir`, `lon`, and `lon-dir`) are defined. Where the location is not known (reported), all four location
    fields will be null.

    The date is reported as a string in `YYYY-MM-DD hh:mm:ss` format. Both `lat` and `lon` are reported as strings in
    decimal degrees. The `lat-dir` field will be either N or S (or null). Similarly, the `lon-dir` field will be either
    E or W (or null). The `alt` field is reported as a string in decimal km and is referenced to the Earth geoid. The
    `vel` field is reported as a string in decimal km/s. Total radiated energy is reported in the `energy` field as a
    string in decimal joules × 1010 (for example, a reported value of 3.6 is 3.6 × 1010 joules). Impact energy is
    reported in the `impact-e` field in units of kilotons (kt).

    All fields are relative to the fireball’s peak-brightness event.

    """
    url = 'https://ssd-api.jpl.nasa.gov/fireball.api'

    if date_min is not None:
        if not isinstance(date_min, (str, datetime.datetime)):
            raise TypeError('date_min parameter must be a string representing a date in YYYY-MM-DD or '
                            'YYYY-MM-DDThh:mm:ss formats or a datetime object.')

        if isinstance(date_min, datetime.datetime):
            date_min = date_min.strftime('%Y-%m-%d')

    if date_max is not None:
        if not isinstance(date_max, (str, datetime.datetime)):
            raise TypeError('date_min parameter must be a string representing a date in YYYY-MM-DD or '
                            'YYYY-MM-DDThh:mm:ss formats or a datetime object.')

        if isinstance(date_max, datetime.datetime):
            date_max = date_max.strftime('%Y-%m-%d')

    if vel_min is not None and vel_max is not None:
        if vel_min > vel_max:
            raise ValueError('vel_min parameter must be less than vel_max.')

    if alt_min is not None and alt_max is not None:
        if alt_min > alt_max:
            raise ValueError('alt_min parameter must be less than alt_max.')

    if not isinstance(req_loc, bool):
        raise TypeError('req_loc parameter must be boolean (True or False).')

    if not isinstance(req_alt, bool):
        raise TypeError('req_alt parameter must be boolean (True or False).')

    if not isinstance(req_vel, bool):
        raise TypeError('req_vel parameter must be boolean (True or False).')

    if not isinstance(req_vel_comp, bool):
        raise TypeError('req_vel_comp parameter must be boolean (True or False).')

    if not isinstance(vel_comp, bool):
        raise TypeError('vel_comp parameter must be boolean (True or False).')

    if not isinstance(return_df, bool):
        raise TypeError('return_df parameter must be boolean (True or False).')

    if limit is not None:
        if not isinstance(limit, int):
            raise TypeError('limit parameter must be an integer (if specified).')

        elif limit <= 0:
            raise ValueError('limit parameter must be greater than 0.')

    params = {
        'date-min': date_min,
        'date-max': date_max,
        'energy-min': energy_min,
        'energy-max': energy_max,
        'impact-e-min': impact_e_min,
        'impact-e-max': impact_e_max,
        'vel-min': vel_min,
        'vel-max': vel_max,
        'alt-min': alt_min,
        'alt-max': alt_max,
        'req-loc': req_loc,
        'req-alt': req_alt,
        'req-vel': req_vel,
        'req-vel-comp': req_vel_comp,
        'vel-comp': vel_comp,
        'sort': sort,
        'limit': limit
    }

    r = _return_api_result(url=url,
                           params=params)

    if return_df:
        r = DataFrame(r['data'], columns=r['fields'])

    return r


def mission_design(des=None, spk=None, sstr=None, orbit_class=False, mjd0=None, span=None, tof_min=None,
                   tof_max=None, step=None):
    r"""
    Provides access to the Jet Propulsion Laboratory/Solar System Dynamics small body mission design suite API.

    Parameters
    ----------
    des : str, default None
        The designation (provisional or IAU-number) of the desired object to search.
    spk : int, str, default None
        The SPK-ID of the desired object to search.
    sstr : str, default None
        Object search string.
    orbit_class : bool, default False
        If True, returns the orbit class in human readable format instead of the default three-letter code.
    mjd0 : int, default None
        First launch date in Modified Julian Date. Must be between [33282, 73459].
    span : int, default None
        Duration of the launch-date period to be explored in days. Must be between [10, 9200].
    tof_min : int, default None
        Minimum time of flight in days. Must be between [10, 9200].
    tof_max : int, default None
        Maximum time of flight in days. Must be between [10, 9200].
    step : int, default None, {1,2,5,10,15,20,30}
        Time step used to advance the launch date and the time of flight. Size of transfer map is limited to
        1,500,000 points.

    Raises
    ------
    ValueError
        Raised if :code:`des`, :code:`spk` and :code:`sstr` parameters are None.
    ValueError
        Raised if parameter :code:`mjd0` is not between [33282, 73459].
    ValueError
        Raised if parameter :code:`span` is not between [10, 9200].
    ValueError
        Raised if parameter :code:`tof_min` is not between [10, 9200].
    ValueError
        Raised if parameter :code:`tof_max` is not between [10, 9200].
    ValueError
        Raised if parameter :code:`step` is not one of (1, 2, 5, 10, 15, 20, 30), if specified.
    TypeError
        Raised if parameter :code:`orbit_class` is not boolean (True or False).

    Returns
    -------
    dict
        Dictionary object representing the returned JSON data from the API.

    Examples
    --------
    # Search for mission design data for SPK-ID 2000433
    >>> r = mission_design(spk=2000433)
    # Print the object data from the returned dictionary object.
    >>> r['object']
    {'data_arc': '45762',
     'md_orbit_id': '656',
     'orbit_class': 'AMO',
     'spkid': '2000433',
     'condition_code': '0',
     'orbit_id': '656',
     'fullname': '433 Eros (A898 PA)',
     'des': '433'}
    # Get Missions to 1 Ceres
    >>> r = mission_design(des=1, mjd0=59000, span=1800, tof_min=120, tof_max=1500, step=5)
    >>> r['object']
    {'data_arc': '8822',
     'md_orbit_id': '46',
     'orbit_class': 'MBA',
     'spkid': '2000001',
     'condition_code': '0',
     'orbit_id': '46',
     'fullname': '1 Ceres',
     'des': '1'}

    """
    url = 'https://ssd-api.jpl.nasa.gov/mdesign.api'

    if all(p is None for p in (des, spk, sstr)):
        raise ValueError('A designation (:code:`des` parameter), SPK-ID (:code:`spk` parameter`), or object search '
                         'string (:code:`sstr`) must be specified to perform a search.')

    if mjd0 is not None:
        if not 33282 <= mjd0 <= 73459:
            raise ValueError('The Modified Julian date must be in range [33282, 73459] ({julian_date})'
                             .format(julian_date=str(mjd0)))
    if span is not None:
        if not 10 <= span <= 9200:
            raise ValueError('The span parameter must be in range [10, 9200]')

    if tof_min is not None:
        if not 10 <= tof_min <= 9200:
            raise ValueError('The tof_min parameter must be in range [10, 9200]')

    if tof_max is not None:
        if not 10 <= tof_max <= 9200:
            raise ValueError('The tof_max parameter must be in range [10, 9200]')

    if step is not None:
        if step not in (1, 2, 5, 10, 15, 20, 30):
            raise ValueError('step parameter must be one of {1, 2, 5, 10, 15, 20, 30}')

    if not isinstance(orbit_class, bool):
        raise TypeError('orbit_class parameter must be boolean (True or False)')

    params = {
        'class': orbit_class,
        'mjd0': mjd0,
        'span': span,
        'tof-min': tof_min,
        'tof-max': tof_max,
        'step': step
    }

    if des is not None:
        params['des'] = des
    elif spk is not None:
        params['spk'] = spk
    elif sstr is not None:
        params['sstr'] = sstr

    r = _return_api_result(url=url, params=params)

    return r


def nhats(spk=None, des=None, delta_v=12, duration=450, stay=8, launch='2020-2045', magnitude=None,
          orbit_condition_code=None, plot=False, return_df=False):
    r"""
    Returns data available from the Near-Earth Object Human Space Flight Accessible Targets Study (NHATS) in the
    Small Bodies Database

    Parameters
    ----------
    delta_v : int, {12, 4, 5, 6, 7, 8, 9, 10, 11}, default None
        Minimum total delta-v in km/s.
    duration : int, {450, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420}
        Minimum total distribution in number of days.
    stay : int, {8, 16, 24, 32}
        Minimum stay in days.
    launch : str, {'2020-2045', '2020-2025', '2025-2030', '2030-2035', '2035-2040', '2040-2045'}
        The proposed launch window as a year range.
    magnitude : int, default None, {16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30}
        The object's maximum absolute magnitude, also denoted as H.
    orbit_condition_code : int, default None, {0, 1, 2, 3, 4, 5, 6, 7, 8}
        The object's maximum orbit condition code (OCC).
    spk : int, default None
        Returns data for a specific object by its SPK-ID.
    des : str, default None
        Returns data for a specific object by its designation.
    plot : bool, default False
        If True, include base-64 encoded plot image file content. Will include a new output field 'plot_base64' in the
        returned results if True.
    return_df : bool, default False
        If True and parameters `spk` and `des` are None, returns the 'data' field of the returned JSON data as a
        pandas DataFrame with column names extracted from the 'fields' key of the returned JSON.

    Raises
    ------
    ValueError
        Raised if both :code:`des` and :code:`spk` are specified.
    ValueError
        Raised if :code:`delta_v` parameter is not one of {4, 5, 6, 7, 8, 9, 10, 11, 12}.
    ValueError
        Raised if :code:`duration` parameter is not one of {60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450}.
    ValueError
        Raised if :code:`stay` parameter is not one of {8, 16, 24, 32}.
    ValueError
        Raised if :code:`launch` parameter is not one of {'2020-2025', '2025-2030', '2030-2035', '2035-2040',
        '2040-2045', '2020-2045'}
    ValueError
        Raised if :code:`magnitude` parameter is not one of {16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        30}, if specified.
    ValueError
        Raised if :code:`orbit_condition_code` is not one of {0, 1, 2, 3, 4, 5, 6, 7, 8}, if specified.

    Returns
    -------
    dict
        Dictionary object representing the returned JSON data from the API.

    Examples
    --------
    # Get all available summary data for NHATS objects.
    >>> n = nhats()
    # Get summary data as a pandas DataFrame
    >>> n = nhats(return_df=True)
    # Get the results from a 'standard' search on the NHATS webpage.
    >>> nhats(delta_v=6, duration=360, stay=8, magnitude=26, launch='2020-2045', orbit_condition_code=7)
    # Return data for a specific object by its designation
    >>> nhats(des=99942)

    """
    url = 'https://ssd-api.jpl.nasa.gov/nhats.api'

    if all(p is not None for p in (des, spk)):
        raise ValueError('Only a designation (:code:`des`) or SPK-ID (:code:`spk`) should be specified, not both.')

    if delta_v not in (4, 5, 6, 7, 8, 9, 10, 11, 12):
        raise ValueError('delta_v parameter must be one of {4, 5, 6, 7, 8, 9, 10, 11, 12}.')

    if duration not in (60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450):
        raise ValueError('duration parameter must be one of '
                         '{60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450}.')

    if stay not in (8, 16, 24, 32):
        raise ValueError('stay parameter must be one of {8, 16, 24, 32}.')

    if launch not in ('2020-2025', '2025-2030', '2030-2035', '2035-2040', '2040-2045', '2020-2045'):
        raise ValueError("launch parameter must be one of "
                         "{'2020-2025', '2025-2030', '2030-2035', '2035-2040','2040-2045', '2020-2045'}.")

    if magnitude is not None:
        if magnitude not in (16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30):
            raise ValueError('magnitude parameter must be one of '
                             '{16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30}, if specified.')

    if orbit_condition_code is not None:
        if orbit_condition_code not in (0, 1, 2, 3, 4, 5, 6, 7, 8):
            raise ValueError('occ parameter must be one of {0, 1, 2, 3, 4, 5, 6, 7, 8}, if specified.')

    if not isinstance(plot, bool):
        raise TypeError('plot parameter must be boolean (True or False)')

    if magnitude is not None:
        if des is not None or spk is not None:
            raise ValueError('magnitude parameter cannot be specified when passing a des or spk.')

    if not isinstance(return_df, bool):
        raise TypeError('return_df parameter must be boolean (True or False)')

    params = {
        'dv': delta_v,
        'dur': duration,
        'stay': stay,
        'launch': launch,
        'h': magnitude,
        'occ': orbit_condition_code,
        'plot': plot
    }

    if des is not None:
        params['des'] = des
        return_df = False
    elif spk is not None:
        params['spk'] = spk
        return_df = False

    r = _return_api_result(url=url, params=params)

    if return_df:
        r = DataFrame(r['data'])

    return r


def scout(tdes=None, plot=None, data_files=None, orbits=None, n_orbits=None, eph_start=None, eph_stop=None,
          eph_step=None, obs_code=None, fov_diam=None, fov_ra=None, fov_dec=None, fov_vmag=None, return_df=False):
    r"""
    Provides access and data available from NASA's Center for Near-Earth Object Studies (CNEOS) Scout system.

    Parameters
    ----------
    tdes : str, default None
        Filter results by an object's temporary designation.
    plot : str, default None
        Includes the plot files for the specified object of the select type. Options include 'el' (elements), 'ca'
        (close approach) and `sr` (systematic-ranging) or any combination delimited by ':'. For example, 'ca:el:sr'
        would include plot files of each available type.
    data_files : str, default None, {'list', 'mpc'}
        Returns available data files or the requested data file for the specified object. Currently only 'mpc' is available.
    orbits : bool, default None
        If True, returns the sampled orbits data for a specified object.
    n_orbits : int, default None
        Limits the number of sampled orbits to this value. Must be in range [1, 1000].
    eph_start : str, datetime, default None
        Get the ephemeris for the specified object at the specified time in UTC.
    eph_stop : str, datetime, default None
        Sets the ephemeris stop-time. Also requires :code:`eph_start` if specified.
    eph_step : str, default None
        Sets the ephemeris step size. Requires both :code:`eph_start` and :code:`eph_stop` to be specified.
    obs_code : str, default None
        Gets the ephemeris for the specified object relative to the specified MPC observatory code.
    fov_diam : float, int, default None
        Specifies the size (diameter) of the field-of-view in arc-minutes.
    fov_ra : str, default None
        Specifies the field-of-view center (R.A component). Requires parameters :code:`fov_diam` and :code:`fov_dec` to
        be set as well. Invalid if :code:`eph_stop` is passed.
    fov_dec : str, default None
        Specifies the field-of-view center (Dec. component). Requires :code:`fov_diam` and :code:`fov_ra` to be
        passed as well. Invalid if :code:`eph_stop` is set.
    fov_vmag : int, default None
        Filters ephemeris results to those with V-magnitude of this value or brighter. Requires :code:`fov_diam` to
        also be specified.
    return_df : bool, default False
        If True and no parameters are specified (returns summary data of all available Scout records), returns the
        'data' field of the returned JSON data as a pandas DataFrame.

    Raises
    ------
    ValueError
        Raised when :code:`n_orbits` is not in range [1, 1000]
    ValueError
        Raised if :code:`eph_start` parameter is more recent than :code:`eph_stop` parameter (if both are specified)
    ValueError
        Raised if :code:`fov_diam` is not in range [0, 1800]
    ValueError
        Raised if :code:`fov_ra` is specified without passing values for :code:`fov_diam` and :code:`fov_dec`
    ValueError
        Raised if :code:`fov_dec` is specified without passing values for :code:`fov_diam` and :code:`fov_ra`.
    TypeError
        Raised if :code:`orbits` is not boolean.
    TypeError
        Raised if :code:`eph_start` is not a string representing a datetime format or a datetime object.
    TypeError
         Raised if :code:`eph_stop` is not a string representing a datetime format or a datetime object.

    Returns
    -------
    dict
        Dictionary object representing the returned JSON data from the API.

    Examples
    --------
    # Get all available summary data.
    >>> scout()
    # Return all summary data as a pandas DataFrame.
    >>> scout(return_df=True)
    # Return data and plot files for a specific object by its temporary designation. Note the object may no longer
    # exist in the current database
    >>> scout(tdes='P20UvyK')
    # Get ephemeris data for a specific object at the current time with a Field of View diameter of 5 arc-minutes
    # with a limiting V-magnitude of 23.1.
    >>> scout(tdes='P20UvyK', fov_diam=5, fov_vmag=23.1)

    """
    url = 'https://ssd-api.jpl.nasa.gov/scout.api'

    if n_orbits is not None:
        if not 1 <= n_orbits <= 1000:
            raise ValueError('n_orbits parameter must be an integer in the range [1, 1000].')

    if eph_start is not None:
        if eph_start != 'now':
            if not isinstance(eph_start, (str, datetime.datetime)):
                raise TypeError("date parameter must be a string representing a date in YYYY-MM-DD or "
                                "YYYY-MM-DDThh:mm:ss format, 'now' for the current date, or a datetime object.")

            if isinstance(eph_start, str):
                eph_start = datetime.datetime.strptime(eph_start, '%Y-%m-%dT%H:%M:%S')

    if eph_stop is not None:
        if not isinstance(eph_stop, (str, datetime.datetime)):
            raise TypeError("date parameter must be a string representing a date in YYYY-MM-DD or "
                            "YYYY-MM-DDThh:mm:ss format, or a datetime object.")

        if isinstance(eph_stop, str):
            eph_stop = datetime.datetime.strptime(eph_stop, '%Y-%m-%dT%H:%M:%S')

    if all(p is isinstance(p, datetime.datetime) for p in (eph_start, eph_stop)):
        if eph_start >= eph_stop:
            raise ValueError('eph_start parameter must be earlier than eph_stop')

    if fov_diam is not None:
        if not 0 <= fov_diam <= 1800:
            raise ValueError('fov_diam parameter must be an integer or float in the range (0, 1800].')

    if fov_ra is not None:
        if fov_diam is None and fov_dec is None:
            raise ValueError('parameters fov_diam and fov_dec must be specified when passing a fov_ra value.')

    if fov_dec is not None:
        if fov_diam is None and fov_ra is None:
            raise ValueError('parameters fov_diam and fov_ra must be specified when passing a fov_dec value')

    if fov_vmag is not None:
        if not 1 <= fov_vmag <= 40:
            raise ValueError('fov_vmag parameter must be an integer in the range [1, 40].')

    if orbits is not None:
        if not isinstance(orbits, bool):
            raise TypeError('orbits parameter must be boolean (True or False).')

    if not isinstance(return_df, bool):
        raise TypeError('return_df parameter must be boolean (True or False)')

    params = {'tdes': tdes,
              'plot': plot,
              'file': data_files,
              'orbits': orbits,
              'n-orbits': n_orbits,
              'eph-start': eph_start,
              'eph-stop': eph_stop,
              'eph-step': eph_step,
              'obs-code': obs_code,
              'fov-diam': fov_diam,
              'fov-ra': fov_ra,
              'fov_dec': fov_dec,
              'fov-vmag': fov_vmag}

    r = _return_api_result(url=url, params=params)

    if return_df:
        if all(p is None for p in (tdes, plot, data_files, orbits, n_orbits, eph_start, eph_stop, eph_step, obs_code,
                                   fov_diam, fov_ra, fov_dec, fov_vmag)):
            if int(r['count']) > 0:
                r = DataFrame(r['data'])

    return r


def sentry(spk=None, des=None, h_max=None, ps_min=None, ip_min=None, last_obs_days=None, complete_data=False,
           removed=False, return_df=False):
    r"""
    Provides data available from the Center for Near Earth Object Studies (CNEOS) Sentry system.

    Parameters
    ----------
    spk : int, default None
        Returns data available for the object matching the specified SPK-ID.
    des : str, default None
        Selects data for the matching designation.
    h_max : float, int, default None
        Limits data to those with an absolute magnitude, less than or equal to the specified value. Must be in the
        range [-10:100].
    ps_min : int, default None
        Limits results to those with a Palermo scale (PS) greater than or equal to the specified value. Must be in the
        range [-20:20].
    ip_min : float, default None
        Filters data to that which has an impact probability (IP) greater than or equal to the specified value.
    last_obs_days : int, default None
        Number of days since last observation. If negative, filters data to those which have not been observed within
        the specified number of days. If passed, must have an absolute value greater than 6.
    complete_data : bool, default False
        If True, requests the full dataset to be returned.
    removed : bool, default False
        If True, requests the list of removed objects to be returned.
    return_df : bool, default False
        If True, returns the 'data' field of the returned JSON data as a pandas DataFrame. If a `des` or `spk`
        parameter is passed with `return_df=True`, a tuple containing the coerced data field as a pandas DataFrame and
        the `summary` object of the returned data will be returned.

    Raises
    ------
    ValueError
        Raised if :code:`spk` and :code:`des` are both specified.
    ValueError
        Raised if :code:`h_max` is not in range [-10, 100].
    ValueError
        Raised if :code:`ps_min` is not in range [-20, 20].
    ValueError
        Raised if :code:`ip_min` is not in range [-1e-10, 1].
    ValueError
        Raised if :code:`last_obs_days` is not greater than 6.
    TypeError
        Raised if :code:`complete_data` is not boolean (True or False).
    TypeError
        Raised if :code:`removed` is not boolean (True or False).

    Returns
    -------
    dict
        Dictionary object representing the returned JSON data.

    Examples
    --------
    # Get summary data for available sentry objects.
    >>> sentry()
    # Get summary data as a pandas DataFrame
    >>> sentry(return_df=True)
    # Get data for a specific Sentry object by its designation.
    >>> sentry(des=99942)
    # Get data for objects removed from the Sentry system.
    >>> sentry(removed=1)

    """
    url = 'https://ssd-api.jpl.nasa.gov/sentry.api'

    if spk is not None and des is not None:
        raise ValueError('only spk or des should be specified, not both.')

    if h_max is not None:
        if not -10 <= h_max <= 100:
            raise ValueError('h_max parameter must be a float or integer in the range [-10, 100].')

    if ps_min is not None:
        if not -20 <= ps_min <= 20:
            raise ValueError('ps_min parameter must be an integer in the range [-20, 20].')

    if ip_min is not None:
        if not 1e-10 <= ip_min <= 1:
            raise ValueError('ip_min parameter must be a number in the range [1e-10, 1]')

    if last_obs_days is not None:
        if not abs(last_obs_days) > 6:
            raise ValueError('last_obs_days parameter must be an integer whose absolute value is greater than 6.')

    if not isinstance(complete_data, bool):
        raise TypeError('complete_data parameter must be boolean (True or False).')

    if not isinstance(removed, bool):
        raise TypeError('removed parameter must be boolean (True or False).')

    params = {
        'h-max': h_max,
        'ps-min': ps_min,
        'ip-min': ip_min,
        'days': last_obs_days,
    }

    if spk is None and des is None:
        params['all'] = complete_data
        params['removed'] = removed
    else:
        if spk is not None:
            params['spk'] = spk
        if des is not None:
            params['des'] = des

    r = _return_api_result(url=url, params=params)

    if return_df:
        if 'summary' in r.keys():
            r, r2 = DataFrame(r['data']), r['summary']
            return r, r2
        else:
            r = DataFrame(r['data'])

    return r


def julian_date(dt=None, year=None, month=1, day=1, hour=0, minute=0, second=0, modified=True):
    r"""
    Calculates the Julian date or modified Julian date (if specified).

    Parameters
    ----------
    dt : datetime, default None
        Datetime object to convert into a Julian date. Note if a datetime object is supplied to :code:`dt` the other
        parameters will not be evaluated. If None, returns the current datetime converted into a Julian date.
    year : int, str, default None
        Four digit year, such as 2019 or '2019'.
    month : int, default 1
        Month number. For example 1 = January, 12 = December.
    day : int, default 1
        Day of the month.
    hour : int, default 0
        Hour of the day.
    minute : int, default 0
        Minute of the day.
    second : int, default 0
        Second of the day.
    modified : boolean, default True
        If True, returns the modified Julian date, which is the computed Julian Date - 24000000.5.

    Returns
    -------
    float
        The computed Julian or Modified Julian date.

    Examples
    --------
    # Return the modified Julian Date for the current time.
    >>> julian_date()
    # Return the non-modified Julian Date for the current time.
    >>> julian_date(modified=False)
    # Get the modified Julian Date for 2019-01-01 at midnight.
    >>> julian_date(year=2019)

    Notes
    -----
    The equation for calculating the Julian date is defined as:

    .. math::

        J = 367(Year) - /large[ \large( \frac{7(Year + \frac{Month + 9}{12})}{4} \large). \large] +
        \frac{275(Month)}{9}. + Day + 1721013.5 + \frac{\large( \frac{\frac{Second}{60} + Minute}{60} \large) + Hour}{24}

    References
    ----------
    Capt. Vallado, David. Methods of Astrodynamics, A Computer Approach. USAF Academy, CO.

    """
    if all(p is None for p in (dt, year)):
        dt = datetime.datetime.now()

    if dt is None:
        dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    julian = 367 * dt.year - \
             (int(7 * (dt.year + (dt.month + 9)) / 4)) + \
             int((275 * dt.month) / 9) + dt.day + \
             1721013.5 + (((dt.second / 60 + dt.minute) / 60) + dt.hour) / 24

    if modified:
        julian -= 2400000.5

    return julian


def _media_assets(endpoint, nasa_id):
    url = 'https://images-api.nasa.gov/{endpoint}/{nasa_id}'

    r = requests.get(url.format(endpoint=endpoint,
                                nasa_id=nasa_id))

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.reason, r.url)

    else:
        if endpoint == 'asset':
            return r.json()['collection']['items']

        elif endpoint == 'metadata':
            location = r.json()['location']
            r = requests.get(location).json()
            r['location'] = location

            return r

        elif endpoint == 'captions':
            location = r.json()['location']
            r = requests.get(location).text

            r = {
                'location': location,
                'captions': r
            }

    return r


def _donki_request(key, url, start_date=None, end_date=None):
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

    if r.text == '':
        r = {}
    else:
        r = r.json()

    return limit_remaining, r


def _check_dates(start_date=None, end_date=None):
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


def _return_api_result(url, params):
    r = requests.get(url,
                     params=params)

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.reason, r.url)

    else:
        return r.json()
