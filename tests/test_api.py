import vcr
import os
import pytest
from nasapy.api import Nasa
from requests.exceptions import HTTPError
import datetime


tape = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    serializer='json',
    record_mode='once'
)

key = os.environ.get('NASA_KEY')


def nasa_api():
    nasa = Nasa(key=key)

    return nasa


nasa = nasa_api()


@vcr.use_cassette('tests/cassettes/initialization.yml')
def test_initialization():
    nasa_demo = Nasa()
    assert nasa_demo._key == 'DEMO_KEY'

    potd = nasa_demo.picture_of_the_day()

    assert isinstance(potd, dict)

    assert nasa._key == key

    potd = nasa.picture_of_the_day()

    assert isinstance(potd, dict)


@vcr.use_cassette('tests/cassettes/picture_of_the_day.yml')
def test_picture_of_the_day():
    potd = nasa.picture_of_the_day()
    potd_hd = nasa.picture_of_the_day(hd=True)
    potd_date = nasa.picture_of_the_day(date='2019-01-01')

    keys = ['date', 'explanation', 'media_type', 'service_version', 'title', 'url']

    assert isinstance(potd, dict)
    assert len(set(keys).difference(potd.keys())) == 0
    assert isinstance(potd_hd, dict)
    assert isinstance(potd_date, dict)

    assert nasa.limit_remaining is not None

    with pytest.raises(HTTPError):
        nasa.picture_of_the_day(date='2019/01/01')


@vcr.use_cassette('tests/cassettes/insights_weather.yml')
def test_mars_weather():
    weather = nasa.mars_weather()

    sols = ['259', '260', '261', '262', '263', '264', '265']

    assert isinstance(weather, dict)
    assert 'sol_keys' in weather.keys()
    assert len(set(sols).intersection(weather.keys())) > 0

    assert nasa.mars_weather_remaining is not None


@vcr.use_cassette('tests/cassettes/asteroid_feed.yml')
def test_asteroid_feed():
    feed = nasa.asteroid_feed()
    date_today = datetime.datetime.today().strftime('%Y-%m-%d')

    assert isinstance(feed, dict)
    assert isinstance(feed['element_count'], int)
    assert 'near_earth_objects' in feed.keys()
    assert date_today in feed['near_earth_objects'].keys()

    with pytest.raises(HTTPError):
        nasa.asteroid_feed(start_date='2019/01/01')
    with pytest.raises(HTTPError):
        nasa.asteroid_feed(end_date='2019/01/01')


@vcr.use_cassette('tests/cassettes/get_asteroids.yml')
def test_get_asteroids():
    ast = nasa.get_asteroids(asteroid_id=3542519)
    ast_browse = nasa.get_asteroids()

    assert isinstance(ast, dict)
    assert isinstance(ast_browse, dict)
