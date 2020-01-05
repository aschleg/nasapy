import os
import pandas as pd

import vcr
import pytest

from nasapy.api import *
from requests.exceptions import HTTPError


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


def test_julian_date():
    j1 = julian_date(year=2019, modified=False)
    j2 = julian_date(year=2019)
    j3 = julian_date()

    assert j1 == 2458467.5
    assert j2 == 58467.0
    assert isinstance(j3, (int, float))


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
    f_df = fireballs(limit=10, return_df=True)

    assert isinstance(f, dict)
    assert 'data' in f.keys()

    assert isinstance(f_dt, dict)
    assert 'data' in f_dt.keys()

    assert isinstance(f_df, pd.DataFrame)

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
    with pytest.raises(TypeError):
        fireballs(return_df='false')


@vcr.use_cassette('tests/cassettes/mission_design.yml')
def test_mission_design():
    des = mission_design(des=1, orbit_class=True)
    sstr = mission_design(sstr='apophis')
    spk = mission_design(spk=2000433)

    assert isinstance(des, dict)
    assert isinstance(sstr, dict)
    assert isinstance(spk, dict)

    with pytest.raises(ValueError):
        mission_design()
    with pytest.raises(ValueError):
        mission_design(des=1, mjd0=0)
    with pytest.raises(ValueError):
        mission_design(des=1, mjd0=100000)
    with pytest.raises(ValueError):
        mission_design(des=1, span=0)
    with pytest.raises(ValueError):
        mission_design(des=1, span=10000)
    with pytest.raises(ValueError):
        mission_design(des=1, tof_min=0)
    with pytest.raises(ValueError):
        mission_design(des=1, tof_min=10000)
    with pytest.raises(ValueError):
        mission_design(des=1, tof_max=0)
    with pytest.raises(ValueError):
        mission_design(des=1, tof_max=10000)
    with pytest.raises(ValueError):
        mission_design(des=1, step=3)
    with pytest.raises(TypeError):
        mission_design(des=1, orbit_class=1)


@vcr.use_cassette('tests/cassettes/nhats.yml')
def test_nhats():

    summary = nhats()
    summary_df = nhats(return_df=True)
    des = nhats(des=99942)
    des2 = nhats(des=99942, delta_v=6, duration=360, launch='2020-2045')
    des3 = nhats(spk=2000433)

    assert isinstance(summary, dict)
    assert isinstance(summary_df, pd.DataFrame)
    assert isinstance(des, dict)
    assert isinstance(des2, dict)
    assert isinstance(des3, dict)

    with pytest.raises(ValueError):
        nhats(des=99942, spk=2000433)
    with pytest.raises(ValueError):
        nhats(delta_v=1)
    with pytest.raises(ValueError):
        nhats(duration=1)
    with pytest.raises(ValueError):
        nhats(stay=1)
    with pytest.raises(ValueError):
        nhats(launch='2010')
    with pytest.raises(ValueError):
        nhats(magnitude=1)
    with pytest.raises(ValueError):
        nhats(des=99942, magnitude=20)
    with pytest.raises(ValueError):
        nhats(orbit_condition_code=10)
    with pytest.raises(TypeError):
        nhats(plot='true')
    with pytest.raises(TypeError):
        nhats(return_df='true')


@vcr.use_cassette('tests/cassettes/scout.yml')
def test_scout():

    s = scout()
    s_df = scout(return_df=True)
    s2 = scout(tdes='P20UvyK', plot='el:ca')
    s3 = scout(tdes='P20UvyK', orbits=True)
    s4 = scout(tdes='P20UvyK', eph_start='now')

    assert isinstance(s, dict)
    assert isinstance(s_df, pd.DataFrame)
    assert isinstance(s2, dict)
    assert isinstance(s3, dict)
    assert isinstance(s4, dict)

    with pytest.raises(ValueError):
        scout(n_orbits=0)

    with pytest.raises(ValueError):
        scout(fov_diam=-1)

    with pytest.raises(ValueError):
        scout(fov_ra=0)

    with pytest.raises(ValueError):
        scout(fov_dec=45)

    with pytest.raises(ValueError):
        scout(fov_vmag=0)

    with pytest.raises(ValueError):
        scout(eph_start='2009-12-31', eph_stop='2010-01-01')

    with pytest.raises(TypeError):
        scout(eph_start=2019)

    with pytest.raises(TypeError):
        scout(eph_stop=2020)

    with pytest.raises(TypeError):
        scout(tdes='P20UvyK', orbits='1')

    with pytest.raises(TypeError):
        scout(return_df='true')


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

    space = nasa.genelab_search(term='space', size=1)
    databases = nasa.genelab_search(term='space', database='cgene,nih_geo_gse', size=1)
    order = nasa.genelab_search(term='space', database='cgene,nih_geo_gse', order='asc', size=1)

    assert isinstance(space, dict)
    assert isinstance(databases, dict)
    assert isinstance(order, dict)

    with pytest.raises(ValueError):
        nasa.genelab_search(page=-1)
    with pytest.raises(ValueError):
        nasa.genelab_search(order=1)
    with pytest.raises(ValueError):
        nasa.genelab_search(size=0)


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
    with pytest.raises(ValueError):
        nasa.mars_rover(sol=1000, earth_date='2015-06-03')


@vcr.use_cassette('tests/cassettes/techport.yml')
def test_techport():
    project_id = nasa.techport(project_id=17792)
    xml = nasa.techport(project_id=17792, return_format='xml')
    last_updated = nasa.techport(last_updated='2019-10-01')
    last_updated_dt = nasa.techport(last_updated=datetime.datetime.strptime('2019-10-01', '%Y-%m-%d'))

    assert isinstance(project_id, dict)
    assert isinstance(xml, str)
    assert isinstance(last_updated, dict)
    assert isinstance(last_updated_dt, dict)

    with pytest.raises(ValueError):
        nasa.techport(return_format='test')
    with pytest.raises(TypeError):
        nasa.techport(last_updated=1)


@vcr.use_cassette('tests/cassettes/exoplanets.yml')
def test_exoplanets():
    pass


@vcr.use_cassette('tests/cassettes/sentry.yml')
def test_sentry():
    s = sentry()
    s1 = sentry(return_df=True)
    s2 = sentry(des=99942)
    s3 = sentry(des=99942, return_df=True)

    assert isinstance(s, dict)
    assert isinstance(s1, DataFrame)
    assert isinstance(s2, dict)
    assert isinstance(s3, DataFrame)

    with pytest.raises(ValueError):
        sentry(spk='value', des='value')
    with pytest.raises(ValueError):
        sentry(h_max=-20)
    with pytest.raises(ValueError):
        sentry(ps_min=-25)
    with pytest.raises(ValueError):
        sentry(ip_min=2)
    with pytest.raises(ValueError):
        sentry(last_obs_days=5)
    with pytest.raises(TypeError):
        sentry(complete_data='false')
    with pytest.raises(TypeError):
        sentry(removed='false')
