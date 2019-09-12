# encoding=utf-8

"""

"""

from urllib.parse import urljoin
from datetime import datetime
import requests


class Nasa(object):

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

    def asteroid_feed(self, start_date=None, end_date=None):
        url = self.host + '/neo/rest/v1/feed'

        if start_date is None:
            start_date = datetime.today().strftime('%Y-%m-%d')

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
