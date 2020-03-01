# NasaPy

[![Documentation Status](https://readthedocs.org/projects/nasapy/badge/?version=latest)](https://nasapy.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/aschleg/nasapy.svg?branch=master)](https://travis-ci.org/aschleg/nasapy)
[![Build status](https://ci.appveyor.com/api/projects/status/h36pef9i0o1rjosy?svg=true)](https://ci.appveyor.com/project/aschleg/nasapy)
[![Coverage Status](https://coveralls.io/repos/github/aschleg/nasapy/badge.svg)](https://coveralls.io/github/aschleg/nasapy)
[![codecov](https://codecov.io/gh/aschleg/nasapy/branch/master/graph/badge.svg)](https://codecov.io/gh/aschleg/nasapy)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ff660e1ce59a432493b19bd6f4751347)](https://www.codacy.com/manual/aschleg/nasapy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=aschleg/nasapy&amp;utm_campaign=Badge_Grade)
[![Dependencies](https://img.shields.io/librariesio/github/aschleg/nasapy.svg?label=dependencies)](https://libraries.io/github/aschleg/nasapy)
[![https://pypi.org/project/nasapy/](https://img.shields.io/badge/pypi%20version-0.1.0-blue.svg)](https://pypi.org/project/nasapy/)
[![https://pypi.org/project/nasapy/](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6%2C%203.7-blue.svg)](https://pypi.org/project/nasapy/)

Python wrapper for the [nasa.gov API](https://api.nasa.gov/).

## Installation

`nasapy` is most easily installed using `pip`.

```bash
pip install nasapy
```

The library can also be cloned or downloaded into a location of your choosing and then installed using the `setup.py` 
file per the following:

~~~ bash
git clone git@github.com:aschleg/nasapy.git
cd nasapy
python setup.py install
~~~

## Documentation

* [nasapy Documentation](https://nasapy.readthedocs.io/)
* [Nasa's API documentation page](https://api.nasa.gov/)

## Requirements

* Python 3.4+
* `requests>=2.18`
* `pandas>=0.22.0`
  - Although not strictly required to use `nasapy`, the [pandas](https://pandas.pydata.org/) library is needed 
    for returning results as a DataFrame.

## Tutorials and In-Depth Examples

The following are articles that explore a facet of the `nasapy` library in more depth.

* [Plot Earth Fireball Impacts with nasapy, pandas and folium](https://medium.com/@AaronSchlegel/plot-earth-fireball-impacts-with-nasapy-pandas-and-folium-46bb8bd0b99a)
* [Analyzing the Next Decade of Earth Close-Approaching Objects with nasapy](https://medium.com/@AaronSchlegel/analyzing-the-next-decade-of-earth-close-approaching-objects-with-nasapy-8a6194c4a493)
* [Get All NASA Astronomy Pictures of the Day from 2019](https://medium.com/@AaronSchlegel/get-all-nasa-astronomy-pictures-of-the-day-from-2019-with-python-and-nasapy-c31875e2c48)

## Examples and Usage

Although not strictly required to begin interacting with the NASA API, it is recommended to sign up 
to receive an [API access key](https://api.nasa.gov/) that has a significantly higher usage limit available compared 
to the demo key option. Many methods do not require an API key, but for those that do, it is typically a good option to 
use a provided API key rather than the demo key. Using a received API key allows for 1,000 requests per hour, while the 
demo key has 30 requests limit per hour and 50 requests per day.

### Authentication

Assuming an API key was received after signing up, authentication to the NASA API happens when initializing the `Nasa` 
class.

~~~ python
nasa = Nasa(key=key)
~~~  

If using a demo key, the initialization does not require any parameters to be passed.

~~~ python
nasa = Nasa()
~~~

### Remaining Requests Available

The `limit_remaining` attribute of the initialized `Nasa` class allows one to see the number of available requests 
remaining.

~~~ python
nasa.limit_remaining
~~~

### Examples

The following are some quick examples to get started.

#### Astronomy Picture of the Day

~~~ python
# Return today's picture of the day
nasa.picture_of_the_day()
# Return a previous date's picture of the day with the high-definition URL included.
nasa.picture_of_the_day('2019-01-01', hd=True)
~~~

#### Mars Weather

~~~ python
# Return the most recent data for the previous seven Sols (Martian Days)
nasa.mars_weather()
~~~

#### Asteroid Feed

~~~ python
# Get asteroids approaching Earth at the beginning of 2019.
nasa.asteroid_feed(start_date='2019-01-01')
~~~

#### Get Asteroid Data

~~~ python
# Get entire asteroid data set.
nasa.get_asteroids()
# Get asteroid with ID 3542519
nasa.get_asteroids(asteroid_id=3542519)
~~~

#### DONKI (Space Weather Database of Notifications, Knowledge and Information)

~~~ python
# Coronal Mass Ejection Event Data

# View data from coronal mass ejection events from the last thirty days
nasa.coronal_mass_ejection()
# View all CME events from the beginning of 2019.
nasa.coronal_mass_ejection(start_date='2019-01-01', end_date=datetime.datetime.today())

# Geomagnetic Storm Event Data

# Get geomagnetic storm events from the last thirty days.
nasa.geomagnetic_storm()

# Solar Flare Event Data 

# Get solar flare events from May of 2019
nasa.solar_flare(start_date='2019-05-01', end_date='2019-05-31')

# Solar Energetic Particle Data

# Get data from April 2017
nasa.solar_energetic_particle(start_date='2017-04-01', end_date='2017-04-30')

# Magnetopause Crossing Data

# Get data on magnetopause crossing events from 2018 to the current date.
nasa.magnetopause_crossing(start_date='2018-01-01')

# Radiation Belt Enhancement Data

# Get data on radiation belt enhancement events from the last 30 days.
nasa.radiation_belt_enhancement()

# Hight Speed Stream Data

# Get data on hight speed stream events from the beginning of September 2019.
nasa.hight_speed_stream()

# WSA Enlil-Simulation Data

# Get data from the first simulation performed in 2019.
wsa = n.wsa_enlil_simulation(start_date='2019-01-01')
wsa[0]
~~~

#### EPIC (DSCOVR's Earth Polychromatic Imaging Camera)

~~~ python
# Get EPIC data from the beginning of 2019.
e = nasa.epic(date='2019-01-01')
# Print the first result
e[0]
~~~

#### Exoplanets

~~~ python
# Get all exoplanets data as a pandas DataFrame.
exoplanets(return_df=True)
# Get all confirmed planets in the Kepler field.
exoplanets(where='pl_kepflag=1')
# Stars known to host exoplanets as a pandas DataFrame.
exoplanets(select='distinct pl_hostname', order='pl_hostname', return_df=True)
~~~

#### Landsat Images for a given Latitude-Longitude

~~~ python
# Get imagery at latitude 1.5, longitude 100.75 and include the computed cloud score calculation.
nasa.earth_imagery(lon=100.75, lat=1.5, cloud_score=True)

# Get assets available beginning from 2014-02-01 at lat-lon 100.75, 1.5
nasa.earth_assets(lat=100.75, lon=1.5, begin_date='2014-02-01')
~~~ 

#### Available Image data collected by the Mars rovers Curiosity, Discovery and Spirit.

~~~ python
# Return image data collected on Curiosity's 1000th sol.
nasa.mars_rover(sol=1000)
~~~

#### Access GeneLab and Other Bioinformatics Databases

~~~ python
# Find Gene studies in the cgene database related to 'mouse liver'
n.genelab_search(term='mouse liver')
~~~ 

The following functions do not require authentication with an API or demo key.

#### CelesTrak Two-Line Element Set Records

~~~ python
# Retrieve available data for a specific satellite ID.
tle(satellite_number=43553)
~~~ 

#### Search for Available Imagery and Audio from the images.nasa.gov API

~~~ python
# Search for media related to 'apollo 11' with 'moon landing' in the description of the items.
r = media_search(query='apollo 11', description='moon landing')
# Print the first returned media item from the resulting collection.
r['items'][0]
~~~

#### Asteroid and Comet Close Approaches to planets in the past and future

~~~ python
# Get all close-approach object data in the year 2019 with a maximum approach distance of 0.01AU.
close_approach(date_min='2019-01-01', date_max='2019-12-31', dist_max=0.01)
# Get close-approach data for asteroid 433 Eros within 0.2AU from the years 1900 to 2100.
close_approach(des='433', date_min='1900-01-01', date_max='2100-01-01', dist_max=0.2)
# Return close-approach data from the beginning of 2000 to the beginning of 2020 as a pandas DataFrame.
close_approach(date_min='2000-01-01', date_max='2020-01-01', return_df=True)
~~~

#### Fireball atmospheric impact data reported by US Government sensors

~~~ python
# Get all available data in reverse chronological order
n = fireballs()
# Return the earlieset record
fireballs(limit=1)
# Get data from the beginning of 2019
fireballs(date_min='2019-01-01')
# Return fireball data from the beginning of the millennium to the beginning of 2020 as a pandas DataFrame.
fireballs(date_min='2000-01-01', date_max='2020-01-01', return_df=True)
~~~

#### Jet Propulsion Laboratory/Solar System Dynamics small body mission design suite API

~~~ python
# Search for mission design data for SPK-ID 2000433
r = mission_design(spk=2000433)
# Print the object data from the returned dictionary object.
r['object']
~~~

#### Get Data on Near-Earth Object Human Space Flight Accessible Targets

~~~ python
# Get all available summary data for NHATS objects.
n = nhats()
# Get summary data as a pandas DataFrame
n = nhats(return_df=True)
# Get the results from a 'standard' search on the NHATS webpage.
nhats(delta_v=6, duration=360, stay=8, magnitude=26, launch='2020-2045', orbit_condition_code=7)
# Return data for a specific object by its designation
nhats(des=99942)
~~~

#### Get Data from NASA's Center for Near-Earth Object Studies (CNEOS) Scout system

~~~ python
# Get all available summary data.
scout()
# Return all summary data as a pandas DataFrame.
scout(return_df=True)
# Return data and plot files for a specific object by its temporary designation. Note the object may no longer
# exist in the current database
scout(tdes='P20UvyK')
# Get ephemeris data for a specific object at the current time with a Field of View diameter of 5 arc-minutes
# with a limiting V-magnitude of 23.1.
scout(tdes='P20UvyK', fov_diam=5, fov_vmag=23.1)
~~~

#### Get Data from the Center for Near Earth Object Studies (CNEOS) Sentry system

~~~ python
# Get summary data for available sentry objects.
sentry()
# Get summary data as a pandas DataFrame
sentry(return_df=True)
# Get data for a specific Sentry object by its designation.
sentry(des=99942)
# Get data for objects removed from the Sentry system.
sentry(removed=1)
~~~

Other function examples

#### Getting the Julian and Modified Julian Date

~~~ python 
# Return the modified Julian Date for the current time.
julian_date()
# Return the non-modified Julian Date for the current time.
julian_date(modified=False)
# Get the modified Julian Date for 2019-01-01 at midnight.
julian_date(year=2019)
~~~

## License

MIT