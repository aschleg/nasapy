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
    s_year = media_search(query='apollo 11', year_start=str(datetime.datetime.strptime('2013-01-01', '%Y-%m-%d').year))
    s_year2 = media_search(query='apollo 11', year_end=str(datetime.datetime.strptime('2015-01-01', '%Y-%m-%d').year))

    assert isinstance(s, dict)
    assert isinstance(s['items'], list)

    assert isinstance(s_year, dict)
    assert isinstance(s_year['items'], list)

    assert isinstance(s_year2, dict)
    assert isinstance(s_year2['items'], list)

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


@vcr.use_cassette('tests/cassettes/close_approach.yml')
def test_close_approach():
    cad = close_approach(des=433, date_min='1900-01-01', date_max='2100-01-01', dist_max=0.2)
    cad_dt = close_approach(date_min='2010-01-01', date_max=datetime.datetime.strptime('2019-10-28', '%Y-%m-%d'))
    cad_dt2 = close_approach(date_min=datetime.datetime.strptime('2019-10-28', '%Y-%m-%d'), date_max='2025-01-01')

    assert isinstance(cad, dict)
    assert 'data' in cad.keys()

    assert isinstance(cad_dt, dict)
    assert 'data' in cad_dt.keys()

    assert isinstance(cad_dt2, dict)
    assert 'data' in cad_dt2.keys()

    with pytest.raises(TypeError):
        close_approach(date_min=1)
    with pytest.raises(ValueError):
        close_approach(h_min=1, h_max=0.9)
    with pytest.raises(ValueError):
        close_approach(v_inf_min=10, v_inf_max=9)
    with pytest.raises(ValueError):
        close_approach(v_rel_min=2, v_rel_max=1.5)
    with pytest.raises(TypeError):
        close_approach(pha='false')
    with pytest.raises(TypeError):
        close_approach(nea='false')
    with pytest.raises(TypeError):
        close_approach(comet='false')
    with pytest.raises(TypeError):
        close_approach(nea_comet='false')
    with pytest.raises(TypeError):
        close_approach(neo='false')
    with pytest.raises(TypeError):
        close_approach(fullname='false')
    with pytest.raises(TypeError):
        close_approach(limit='1')
    with pytest.raises(ValueError):
        close_approach(limit=-1)


@vcr.use_cassette('tests/cassettes/fireballs.yml')
def test_fireballs():
    f = fireballs(limit=1)
    f_dt = fireballs(date_min=datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'),
                     date_max=datetime.datetime.strptime('2020-01-01', '%Y-%m-%d'),
                     limit=1)

    assert isinstance(f, dict)
    assert 'data' in f.keys()

    assert isinstance(f_dt, dict)
    assert 'data' in f_dt.keys()

    with pytest.raises(TypeError):
        fireballs(date_min=1)
    with pytest.raises(TypeError):
        fireballs(date_max=1)
    with pytest.raises(ValueError):
        fireballs(vel_min=2, vel_max=1)
    with pytest.raises(ValueError):
        fireballs(alt_min=2, alt_max=1)
    with pytest.raises(TypeError):
        fireballs(req_loc='false')
    with pytest.raises(TypeError):
        fireballs(req_alt='false')
    with pytest.raises(TypeError):
        fireballs(req_vel='false')
    with pytest.raises(TypeError):
        fireballs(req_vel_comp='false')
    with pytest.raises(TypeError):
        fireballs(vel_comp='false')
    with pytest.raises(TypeError):
        fireballs(limit='1')
    with pytest.raises(ValueError):
        fireballs(limit=-1)
