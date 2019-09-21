import vcr
import os
import pytest
from nasapy.api import Nasa, _check_dates
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

    potd_demo = nasa_demo.picture_of_the_day()
    potd = nasa.picture_of_the_day()

    assert nasa_demo.api_key == 'DEMO_KEY'
    assert isinstance(potd_demo, dict)
    assert nasa.api_key == key
    assert isinstance(potd, dict)


@vcr.use_cassette('tests/cassettes/picture_of_the_day.yml')
def test_picture_of_the_day():
    potd = nasa.picture_of_the_day()
    potd_hd = nasa.picture_of_the_day(hd=True)
    potd_date = nasa.picture_of_the_day(date='2019-01-01')
    potd_datetime = nasa.picture_of_the_day(date=datetime.datetime.today())

    keys = ['date', 'explanation', 'media_type', 'service_version', 'title', 'url']

    assert isinstance(potd, dict)
    assert len(set(keys).difference(potd.keys())) == 0
    assert isinstance(potd_hd, dict)
    assert isinstance(potd_date, dict)
    assert isinstance(potd_datetime, dict)

    assert nasa.limit_remaining is not None

    with pytest.raises(TypeError):
        nasa.picture_of_the_day(date=1)
    with pytest.raises(TypeError):
        nasa.picture_of_the_day(hd='test')


@vcr.use_cassette('tests/cassettes/mars_weather.yml')
def test_mars_weather():
    weather = nasa.mars_weather()

    assert isinstance(weather, dict)
    assert 'sol_keys' in weather.keys()

    assert nasa.mars_weather_limit_remaining is not None


@vcr.use_cassette('tests/cassettes/asteroid_feed.yml')
def test_asteroid_feed():
    feed = nasa.asteroid_feed(start_date='2019-01-01')
    feed_datetime = nasa.asteroid_feed(start_date=datetime.datetime.today() - datetime.timedelta(7))

    assert isinstance(feed, dict)
    assert isinstance(feed_datetime, dict)
    assert isinstance(feed['element_count'], int)
    assert 'near_earth_objects' in feed.keys()


@vcr.use_cassette('tests/cassettes/get_asteroids.yml')
def test_get_asteroids():
    ast = nasa.get_asteroids(asteroid_id=3542519)
    ast_browse = nasa.get_asteroids()

    assert isinstance(ast, dict)
    assert isinstance(ast_browse, dict)

    with pytest.raises(HTTPError):
        nasa.get_asteroids(asteroid_id=0)


@vcr.use_cassette('tests/cassettes/coronal_mass_ejection.yml')
def test_coronal_mass_ejection():
    keys = ['time21_5', 'latitude', 'longitude', 'halfAngle', 'speed', 'type', 'isMostAccurate',
            'associatedCMEID', 'catalog']

    cme = nasa.coronal_mass_ejection()
    cme_swrc = nasa.coronal_mass_ejection(catalog='SWRC_CATALOG')

    assert isinstance(cme, (list, dict))
    assert isinstance(cme_swrc, (list, dict))

    assert cme_swrc[0]['catalog'] == 'SWRC_CATALOG'
    assert len(set(keys).difference(cme[0].keys())) == 0

    with pytest.raises(ValueError):
        nasa.coronal_mass_ejection(catalog='test')
    with pytest.raises(TypeError):
        nasa.coronal_mass_ejection(complete_entry='True')


@vcr.use_cassette('tests/cassettes/geomagnetic_storm.yml')
def test_geomagnetic_storm():
    keys = ['gstID', 'startTime', 'allKpIndex', 'linkedEvents']

    ge = nasa.geomagnetic_storm()

    assert isinstance(ge, (list, dict))
    assert len(set(keys).difference(ge[0].keys())) == 0


@vcr.use_cassette('tests/cassettes/interplantary_shock.yml')
def test_interplantary_shock():

    shock = nasa.interplantary_shock()
    shock_date = nasa.interplantary_shock(start_date='2019-01-01')

    assert shock == {}
    assert len(shock_date) > 0
    assert isinstance(shock_date, list)
    assert isinstance(shock_date[0], dict)

    with pytest.raises(ValueError):
        nasa.interplantary_shock(catalog='test')
    with pytest.raises(ValueError):
        nasa.interplantary_shock(location='test')


def test_date_check():
    start_date = datetime.datetime.today() - datetime.timedelta(7)
    end_date = datetime.datetime.today()

    start_dt, end_dt = _check_dates(start_date=start_date, end_date=end_date)
    start_str, end_str = _check_dates(start_date='2019-01-01', end_date='2018-01-01')

    assert isinstance(start_dt, str)
    assert isinstance(end_dt, str)

    assert isinstance(start_str, str)
    assert isinstance(end_str, str)

    start_int, end_int = 1, 2

    with pytest.raises(TypeError):
        _check_dates(start_date=start_int, end_date='2019-01-01')
    with pytest.raises(TypeError):
        _check_dates(start_date='2019-01-01', end_date=end_int)
