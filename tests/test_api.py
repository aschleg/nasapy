import vcr
import os
import pytest
from nasapy.api import Nasa
from requests.exceptions import HTTPError


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

    assert isinstance(potd, dict)
    assert isinstance(potd_hd, dict)
    assert isinstance(potd_date, dict)

    with pytest.raises(HTTPError):
        nasa.picture_of_the_day(date='2019/01/01')
