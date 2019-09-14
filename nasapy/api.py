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
                              accurate_only=True, speed=None, complete_entry=True, half_angle=0,
                              catalog='ALL', keyword=None):

        if catalog not in ('ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG'):
            raise ValueError("catalog parameter must be one of ('ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG')")

        if not isinstance(complete_entry, bool):
            raise TypeError('complete_entry parameter must be boolean (True or False).')

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
            return r.json()

    def geomagnetic_storm(self, start_date=None, end_date=None):
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
            return r.json()

    def interplantery_shock(self, start_date=None, end_date=None, location='ALL', catalog='ALL'):

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
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/FLR',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def solar_energetic_particle(self, start_date=None, end_date=None):
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/SEP',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def magnetopause_crossing(self, start_date=None, end_date=None):
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/MPC',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def radiation_belt_enhancement(self, start_date=None, end_date=None):
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/RBE',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def hight_speed_stream(self, start_date=None, end_date=None):
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/HSS',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def wsa_enlil_simulation(self, start_date=None, end_date=None):
        self.__limit_remaining, r = _donki_request(url=self.host + '/DONKI/WSAEnlilSimulations',
                                                   key=self.__api_key,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return r

    def epic(self, date, color='natural'):
        pass

    def earth_imagery(self, lat, long, dim=0.025, date=None, cloud_score=False):
        pass


def _donki_request(key, url, start_date, end_date):
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
