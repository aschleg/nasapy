import vcr
import pytest

from nasapy.api import *
from requests.exceptions import HTTPError

tape = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    serializer='json',
    record_mode='new_episodes'
)


@vcr.use_cassette('tests/cassettes/media_search.yml')
def test_media_search():
    s = media_search(query='apollo 11', description='moon landing')

    assert isinstance(s, dict)
    assert isinstance(s['items'], list)

    with pytest.raises(ValueError):
        media_search(media_type='test')
    with pytest.raises(ValueError):
        media_search()
    with pytest.raises(TypeError):
        media_search(year_start=1)
    with pytest.raises(TypeError):
        media_search(year_end=1)


@vcr.use_cassette('tests/cassettes/media_asset_manifest.yml')
def test_media_asset_manifest():
    m = media_asset_manifest(nasa_id='as11-40-5874')

    assert isinstance(m, list)

    with pytest.raises(HTTPError):
        media_asset_manifest(nasa_id='1')


@vcr.use_cassette('tests/cassettes/media_asset_metadata.yml')
def test_media_asset_metadata():
    m = media_asset_metadata(nasa_id='as11-40-5874')

    assert isinstance(m, dict)
    assert 'location' in m.keys()

    with pytest.raises(HTTPError):
        media_asset_metadata(nasa_id='1')


@vcr.use_cassette('tests/cassettes/media_asset_captions.yml')
def test_media_asset_captions():
    m = media_asset_captions(nasa_id='172_ISS-Slosh')

    assert isinstance(m, dict)
    assert 'location' in m.keys()
    assert 'captions' in m.keys()

    with pytest.raises(HTTPError):
        media_asset_captions(nasa_id='1')


@vcr.use_cassette('tests/cassettes/tle.yml')
def test_tle():
    tle_all = tle()
    tle_sat_num = tle(satellite_number=43553)
    tle_search = tle(search_satellite='1998-067PB')

    assert isinstance(tle_all, dict)
    assert isinstance(tle_sat_num, dict)
    assert isinstance(tle_search, dict)

    with pytest.raises(HTTPError):
        tle(satellite_number=1)
