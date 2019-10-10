import vcr
import os
import pytest
from nasapy.api import Nasa, _check_dates, _donki_request
from requests.exceptions import HTTPError
import datetime


tape = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    serializer='json',
    record_mode='new_episodes'
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
    potd_datetime = nasa.picture_of_the_day(date=datetime.datetime.strptime('2019-01-01', '%Y-%m-%d'))

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
    feed_datetime = nasa.asteroid_feed(
        start_date=datetime.datetime.strptime('2019-01-01', '%Y-%m-%d') - datetime.timedelta(7))

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
    cme_no_date = nasa.coronal_mass_ejection(start_date='2019-09-21', end_date='2019-09-21')

    assert isinstance(cme, (list, dict))
    assert isinstance(cme_swrc, (list, dict))

    assert cme_no_date == {}
    assert cme_swrc[0]['catalog'] == 'SWRC_CATALOG'
    assert len(set(keys).difference(cme[0].keys())) == 0

    with pytest.raises(ValueError):
        nasa.coronal_mass_ejection(catalog='test')
    with pytest.raises(TypeError):
        nasa.coronal_mass_ejection(complete_entry='True')
    with pytest.raises(TypeError):
        nasa.coronal_mass_ejection(accurate_only='True')


@vcr.use_cassette('tests/cassettes/geomagnetic_storm.yml')
def test_geomagnetic_storm():
    keys = ['gstID', 'startTime', 'allKpIndex', 'linkedEvents']

    ge = nasa.geomagnetic_storm()
    ge_no_dat = nasa.geomagnetic_storm(start_date='2019-09-21', end_date='2019-09-21')

    assert ge_no_dat == {}
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
    with pytest.raises(TypeError):
        nasa.interplantary_shock(location=2)
    with pytest.raises(TypeError):
        nasa.interplantary_shock(catalog=2)


@vcr.use_cassette('tests/cassettes/solar_flare.yml')
def test_solar_flare():
    sf = nasa.solar_flare(start_date='2019-01-01', end_date='2019-02-01')
    assert isinstance(sf, (list, dict))
    assert isinstance(sf[0], dict)

    sf_no_dat = nasa.solar_flare()
    assert sf_no_dat == {}


@vcr.use_cassette('tests/cassettes/solar_energetic_particle.yml')
def test_solar_energetic_particle():
    sp = nasa.solar_energetic_particle(start_date='2017-01-01', end_date='2017-05-01')
    assert isinstance(sp, list)
    assert isinstance(sp[0], dict)

    sp_no_dat = nasa.solar_energetic_particle()
    assert sp_no_dat == {}
    assert isinstance(sp_no_dat, dict)


@vcr.use_cassette('tests/cassettes/magnetopause_crossing.yml')
def test_magnetopause_crossing():
    mc = nasa.magnetopause_crossing(start_date='2018-01-01', end_date='2018-05-31')
    assert isinstance(mc, list)
    assert isinstance(mc[0], dict)

    mc_no_dat = nasa.magnetopause_crossing()
    assert mc_no_dat == {}
    assert isinstance(mc_no_dat, dict)


@vcr.use_cassette('tests/cassettes/radiation_belt_enhancement.yml')
def test_radiation_belt_enhancement():
    rbe = nasa.radiation_belt_enhancement(start_date='2019-08-01')
    assert isinstance(rbe, list)
    assert isinstance(rbe[0], dict)

    rbe_no_dat = nasa.radiation_belt_enhancement(start_date='2019-09-22')
    assert rbe_no_dat == {}
    assert isinstance(rbe_no_dat, dict)


@vcr.use_cassette('tests/cassettes/hight_speed_stream.yml')
def test_hight_speed_stream():
    hss = nasa.hight_speed_stream()
    assert isinstance(hss, list)
    assert isinstance(hss[0], dict)

    hss_no_dat = nasa.hight_speed_stream(start_date='2019-09-22')
    assert hss_no_dat == {}
    assert isinstance(hss_no_dat, dict)


@vcr.use_cassette('tests/cassettes/wsa_simulation.yml')
def test_wsa_simulation():
    wsa = nasa.wsa_enlil_simulation(start_date='2019-01-01', end_date='2019-01-05')
    assert isinstance(wsa, list)
    assert isinstance(wsa[0], dict)

    wsa_no_dat = nasa.wsa_enlil_simulation()
    assert wsa_no_dat == {}
    assert isinstance(wsa_no_dat, dict)


@vcr.use_cassette('tests/cassettes/epic.yml')
def test_epic():

    enhanced = nasa.epic(color='enhanced', date='2019-01-01')
    natural = nasa.epic(date='2019-01-01')
    available_dates = nasa.epic(available=True)
    available_dates_enhanced = nasa.epic(color='enhanced', available=True)
    epic_datetime = nasa.epic(date=datetime.datetime.strptime('2019-01-01', '%Y-%m-%d'))
    epic_all_dates = nasa.epic()

    assert isinstance(enhanced, list)
    assert isinstance(enhanced[0], dict)
    assert isinstance(natural, list)
    assert isinstance(natural[0], dict)
    assert isinstance(available_dates, list)
    assert isinstance(available_dates_enhanced, list)
    assert isinstance(epic_datetime, list)
    assert isinstance(epic_datetime[0], dict)
    assert isinstance(epic_all_dates, list)

    with pytest.raises(ValueError):
        nasa.epic(color='test')
    with pytest.raises(TypeError):
        nasa.epic(available='True')
    with pytest.raises(TypeError):
        nasa.epic(date=1)


@vcr.use_cassette('tests/cassettes/genelab_search.yml')
def test_genelab_search():
    pass


@vcr.use_cassette('tests/cassettes/earth_imagery.yml')
def test_earth_imagery():
    image = nasa.earth_imagery(lat=1.5, lon=100.75)
    image_no_dat = nasa.earth_imagery(lat=1.5, lon=180)
    image_datetime = nasa.earth_imagery(lat=1.5, lon=180,
                                        date=datetime.datetime.strptime('2019-01-01', '%Y-%m-%d'))

    assert isinstance(image, dict)
    assert isinstance(image_datetime, dict)
    assert image_no_dat == {}

    with pytest.raises(TypeError):
        nasa.earth_imagery(lat=1.5, lon=100.75, cloud_score='False')
    with pytest.raises(TypeError):
        nasa.earth_imagery(lat='1.5', lon=100.75)
    with pytest.raises(TypeError):
        nasa.earth_imagery(lon='100.75', lat=1.5)
    with pytest.raises(TypeError):
        nasa.earth_imagery(lat=1.5, lon=100.75, date=1)
    with pytest.raises(TypeError):
        nasa.earth_imagery(dim='1', lat=1.5, lon=100.75)

    with pytest.raises(ValueError):
        nasa.earth_imagery(lat=91, lon=100.75)
    with pytest.raises(ValueError):
        nasa.earth_imagery(lon=181, lat=1.5)


@vcr.use_cassette('tests/cassettes/earth_assets.yml')
def test_earth_assets():
    assets = nasa.earth_assets(lon=100.75, lat=1.5, begin_date='2019-01-01')
    assets_datetime = nasa.earth_assets(lon=100.75, lat=1.5,
                                        begin_date=datetime.datetime.strptime('2019-01-01', '%Y-%m-%d'),
                                        end_date=datetime.datetime.strptime('2019-10-01', '%Y-%m-%d'))

    assert isinstance(assets, dict)
    assert isinstance(assets_datetime, dict)

    with pytest.raises(TypeError):
        nasa.earth_assets(lon=100.75, lat=1.5, begin_date=1)
    with pytest.raises(TypeError):
        nasa.earth_assets(lon=100.75, lat=1.5, begin_date='2019-01-01', end_date=1)
    with pytest.raises(ValueError):
        nasa.earth_assets(lat=91, lon=100.75, begin_date='2019-01-01')
    with pytest.raises(ValueError):
        nasa.earth_assets(lon=181, lat=1.5, begin_date='2019-01-01')


@vcr.use_cassette('tests/cassettes/mars_rover.yml')
def test_mars_rover():
    mars_rover_earth_date = nasa.mars_rover(earth_date='2015-06-03')
    mars_rover_earth_datetime = nasa.mars_rover(earth_date=datetime.datetime.strptime('2015-06-03', '%Y-%m-%d'))
    mars_rover_sol = nasa.mars_rover(sol=1000)
    spirit_rover = nasa.mars_rover(sol=1, rover='spirit')

    assert isinstance(mars_rover_earth_date, list)
    assert isinstance(mars_rover_earth_date[0], dict)

    assert isinstance(mars_rover_earth_datetime, list)

    assert isinstance(mars_rover_sol, list)
    assert isinstance(mars_rover_sol[0], dict)

    assert isinstance(spirit_rover, list)
    assert isinstance(spirit_rover[0], dict)

    with pytest.raises(ValueError):
        nasa.mars_rover(camera='test')
    with pytest.raises(ValueError):
        nasa.mars_rover(rover='test')
    with pytest.raises(TypeError):
        nasa.mars_rover(earth_date=1)


@vcr.use_cassette('tests/cassettes/media_search.yml')
def test_media_search():
    s = nasa.media_search(query='apollo 11', description='moon landing')

    assert isinstance(s, dict)
    assert isinstance(s['items'], list)

    with pytest.raises(ValueError):
        nasa.media_search(media_type='test')
    with pytest.raises(ValueError):
        nasa.media_search()
    with pytest.raises(TypeError):
        nasa.media_search(year_start=1)
    with pytest.raises(TypeError):
        nasa.media_search(year_end=1)


@vcr.use_cassette('tests/cassettes/media_asset_manifest.yml')
def test_media_asset_manifest():
    m = nasa.media_asset_manifest(nasa_id='as11-40-5874')

    assert isinstance(m, list)

    with pytest.raises(HTTPError):
        nasa.media_asset_manifest(nasa_id='1')


@vcr.use_cassette('tests/cassettes/media_asset_metadata.yml')
def test_media_asset_metadata():
    m = nasa.media_asset_metadata(nasa_id='as11-40-5874')

    assert isinstance(m, dict)
    assert 'location' in m.keys()

    with pytest.raises(HTTPError):
        nasa.media_asset_metadata(nasa_id='1')


@vcr.use_cassette('tests/cassettes/media_asset_captions.yml')
def test_media_asset_captions():
    m = nasa.media_asset_captions(nasa_id='172_ISS-Slosh')

    assert isinstance(m, dict)
    assert 'location' in m.keys()
    assert 'captions' in m.keys()

    with pytest.raises(HTTPError):
        nasa.media_asset_captions(nasa_id='1')


@vcr.use_cassette('tests/cassettes/exoplanets.yml')
def test_exoplanets():
    pass


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


def test_donki_request():
    url = 'https://api.nasa.gov//DONKI/FLR'

    limit, r = _donki_request(key=key, url=url, start_date='2019-01-01', end_date='2019-02-01')

    assert isinstance(limit, (str, int))
    assert isinstance(r, list)

    limit_no_dat, r_no_dat = _donki_request(key=key, url=url)

    assert isinstance(limit_no_dat, (str, int))
    assert isinstance(r_no_dat, dict)
