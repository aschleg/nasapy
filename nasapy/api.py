# encoding=utf-8

"""

"""

from urllib.parse import urljoin
from datetime import datetime
import requests


class Nasa(object):

    def __init__(self, key=None):

        if key is not None:
            self._key = key
        else:
            self._key = 'DEMO_KEY'

        self._host = 'https://api.nasa.gov'
        self.limit_remaining = None
        self.insight_weather_remaining = None

    def picture_of_the_day(self, date=None, hd=False):
        url = urljoin(self._host + '/planetary/', 'apod')

        r = requests.get(url,
                         params={
                             'api_key': self._key,
                             'date': date,
                             'hd': hd
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason)

        else:
            self.limit_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def insight_weather(self):
        url = self._host + '/insight_weather/'

        r = requests.get(url,
                         params={
                             'api_key': self._key,
                             'ver': 1.0,
                             'feedtype': 'json'
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.insight_weather_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def asteroid_feed(self, start_date=None, end_date=None):
        url = self._host + '/neo/v1/feed'

        if start_date is None:
            start_date = datetime.today().strftime('%Y-%m-%d')

        r = requests.get(url,
                         params={
                             'api_key': self._key,
                             'start_date': start_date,
                             'end_date': end_date
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.limit_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def get_asteroids(self, asteroid_id=None):
        url = self._host + '/neo/rest/v1/neo/'

        if asteroid_id is not None:
            url = url + str(asteroid_id)

        else:
            url = url + 'browse/'

        r = requests.get(url,
                         params={
                             'api_key': self._key
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.limit_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def neo_sentry(self, active=True):
        pass

    def coronal_mass_ejection(self, start_date=None, end_date=None,
                              accurate_only=True, speed=None, complete_entry=True, half_angle=0,
                              catalog='ALL', keyword=None):

        if catalog not in ('ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG'):
            raise ValueError("catalog parameter must be one of ('ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG')")

        url = self._host + '/DONKI/CMEAnalysis'

        r = requests.get(url,
                         params={
                             'api_key': self._key,
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
            self.limit_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def geomagnetic_storm(self, start_date=None, end_date=None):
        url = self._host + '/DONKI/GST'

        r = requests.get(url,
                         params={
                             'api_key': self._key,
                             'startDate': start_date,
                             'endDate': end_date
                         })

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.reason, r.url)

        else:
            self.limit_remaining = r.headers['X-RateLimit-Remaining']
            return r.json()

    def interplantery_shock(self, start_date=None, end_date=None, location='ALL', catalog='ALL'):
        pass

    def solar_flare(self, start_date=None, end_date=None):
        pass

    def solar_energetic_particle(self, start_date=None, end_date=None):
        pass
