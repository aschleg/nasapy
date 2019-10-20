
.. _api:

API Reference
=============

:mod:`Nasa` - NASA API Wrapper
------------------------------

.. class:: Nasa([key=None])

    Class object containing the methods for interacting with NASA API endpoints that require an API key.

    :param: key: The generated API key received from the NASA API. Registering for an API key can be done on the `NASA API webpage <https://api.nasa.gov/>`_. If :code:`None`, a 'DEMO_KEY' with a much more restricted access limited is used.

Astronomy Picture of the Day
----------------------------

.. method:: Nasa.picture_of_the_day([date=None], [hd=False])

    Returns the URL and other information for the NASA Astronomy Picture of the Day.

    :param: date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date.
    :param: hd: If True, returns the associated high-definition image of the Astrononmy Picture of the Day.
    :rtype: dict. Dictionary object of the JSON data returned from the API.

Mars Weather Insight
--------------------

.. method:: Nasa.mars_weather()

    Returns per-Sol (Martian Days) summary data for each of the last seven available Sols. Data is provided by NASA's
    InSight Mars lander and as such data for particular Sols may be recalculated as more data is received. For more
    information on the data returned, please see `NASA's documentation <https://github.com/nasa/api-docs/blob/gh-pages/InSight%20Weather%20API%20Documentation.pdf>`_.

    :rtype: dict. Dictionary object repreenting the returned JSON data from the API.

Near Earth Objects
------------------

    All the data is from the NASA JPL Asteroid team (http://neo.jpl.nasa.gov/). The API is maintained by the
    `SpaceRocks team <https://github.com/SpaceRocks/>`_

.. method:: Nasa.asteroid_feed([start_date], [end_date=None])

    Returns a list of asteroids based on their closest approach date to Earth.

    :param: start_date: String representing a date in YYYY-MM-DD format or a datetime object.
    :param: end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to seven days after the provided :code:`start_date`.
    :rtype: dict. Dictionary representing the returned JSON data from the API.

.. method:: Nasa.get_asteroids([asteroid_id=None])

    Returns data from the overall asteroid data-set or specific asteroids given an ID.

    :param: asteroid_id: If None, the entire asteroid data set is returned. If an :code:`asteroid_id` is provided, data on that specific asteroid is returned.
    :rtype: dict. Dictionary object representing the returned JSON data from the NASA API.

DONKI (Space Weather Database of Notifications, Knowledge, and Information)
---------------------------------------------------------------------------

    The `Space Weather Database Of Notifications, Knowledge, Information (DONKI) <https://ccmc.gsfc.nasa.gov/donki/>`_
    is a comprehensive on-line tool for space weather forecasters, scientists, and the general space science community.
    DONKI provides chronicles the daily interpretations of space weather observations, analysis, models, forecasts, and
    notifications provided by the Space Weather Research Center (SWRC), comprehensive knowledge-base search
    functionality to support anomaly resolution and space science research, intelligent linkages, relationships,
    cause-and-effects between space weather activities and comprehensive webservice API access to information stored in
    DONKI.

.. method:: Nasa.coronal_mass_ejection([start_date=None], [end_date=None], [accurate_only=True], [speed=0], [complete_entry=True], [half_angle=0], [catalog='ALL'], [keyword=None])

    Returns data collected on coronal mass ejection events.

    :param: start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param: end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :param: accurate_only: If True (default), only the most accurate results collected are returned.
    :param: complete_entry: If True (default), only results with complete data is returned.
    :param: speed: The lower limit of the speed of the CME event. Default is 0
    :param: half_angle: The lower limit half angle of the CME event. Default is 0.
    :param: catalog: Specifies which catalog of data to return results. Defaults to 'ALL' and must be one of {'ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG'}.
    :param: keyword: Filter results by a specific keyword.
    :rtype: list. List of results representing returned JSON data. If no data is returned, an empty dictionary is returned.

.. method:: Nasa.geomagnetic_storm([start_date=None], [end_date=None])

    Returns data collected on geomagnetic storm events.

    :param: start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param: end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :rtype: list: List of results representing returned JSON data. If no data is returned, an empty dictionary is returned.