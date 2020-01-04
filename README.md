# NasaPy

[![Documentation Status](https://readthedocs.org/projects/nasapy/badge/?version=latest)](https://nasapy.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/aschleg/nasapy.svg?branch=master)](https://travis-ci.org/aschleg/nasapy)
[![Build status](https://ci.appveyor.com/api/projects/status/h36pef9i0o1rjosy?svg=true)](https://ci.appveyor.com/project/aschleg/nasapy)
[![Coverage Status](https://coveralls.io/repos/github/aschleg/nasapy/badge.svg)](https://coveralls.io/github/aschleg/nasapy)
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

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aschleg/nasapy/master?filepath=notebooks)

The following are Jupyter Notebooks that explore a facet of the `nasapy` library in more depth. The notebooks can 
also be launched interactively with binder by clicking the "launch binder" badge above.

* [Plot Earth Fireball Impacts with nasapy, pandas and folium](https://github.com/aschleg/nasapy/blob/master/notebooks/Plot%20Earth%20Fireball%20Impacts%20with%20nasapy%2C%20pandas%20and%20folium.ipynb)

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