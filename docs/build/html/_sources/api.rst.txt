
.. _api:

API Reference
=============

:mod:`Nasa` - NASA API Wrapper
------------------------------

.. class:: Nasa([key=None])

    Class object containing the methods for interacting with NASA API endpoints that require an API key.

    :param key: The generated API key received from the NASA API. Registering for an API key can be done on the `NASA API webpage <https://api.nasa.gov/>`_. If :code:`None`, a 'DEMO_KEY' with a much more restricted access limited is used.

Astronomy Picture of the Day
++++++++++++++++++++++++++++

.. method:: Nasa.picture_of_the_day([date=None][, hd=False])

    Returns the URL and other information for the NASA Astronomy Picture of the Day.

    :param date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date.
    :param hd: If True, returns the associated high-definition image of the Astrononmy Picture of the Day.
    :rtype: dict. Dictionary object of the JSON data returned from the API.

    .. code-block:: python

        # Initialize Nasa API Class with a demo key
        n = Nasa()
        # Return today's picture of the day
        n.picture_of_the_day()
        # Return a previous date's picture of the day with the high-definition URL included.
        n.picture_of_the_day('2019-01-01', hd=True)

Mars Weather Insight
++++++++++++++++++++

.. method:: Nasa.mars_weather()

    Returns per-Sol (Martian Days) summary data for each of the last seven available Sols. Data is provided by NASA's
    InSight Mars lander and as such data for particular Sols may be recalculated as more data is received. For more
    information on the data returned, please see `NASA's documentation <https://github.com/nasa/api-docs/blob/gh-pages/InSight%20Weather%20API%20Documentation.pdf>`_.

    :rtype: dict. Dictionary object representing the returned JSON data from the API.

    .. code-block:: python

        # Initialize NASA API object with a demo key
        n = NASA()
        # Return the most recent data for the previous seven Sols (Martian Days)
        n.mars_weather()

Near Earth Objects
++++++++++++++++++

All the data is from the NASA JPL Asteroid team (http://neo.jpl.nasa.gov/). The API is maintained by the
`SpaceRocks team <https://github.com/SpaceRocks/>`_

.. method:: Nasa.asteroid_feed([start_date][, end_date=None])

    Returns a list of asteroids based on their closest approach date to Earth.

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to seven days after the provided :code:`start_date`.
    :rtype: dict. Dictionary representing the returned JSON data from the API.

    .. code-block:: python

        # Initialize the NASA API with a demo key.
        n = NASA()
        # Get asteroids approaching Earth at the beginning of 2019.
        n.asteroid_feed(start_date='2019-01-01')

.. method:: Nasa.get_asteroids([asteroid_id=None])

    Returns data from the overall asteroid data-set or specific asteroids given an ID.

    :param asteroid_id: If None, the entire asteroid data set is returned. If an :code:`asteroid_id` is provided, data on that specific asteroid is returned.
    :rtype: dict. Dictionary object representing the returned JSON data from the NASA API.

    .. code-block:: python

        n = Nasa()
        # Get entire asteroid data set.
        n.get_asteroids()
        # Get asteroid with ID 3542519
        n.get_asteroids(asteroid_id=3542519)

DONKI (Space Weather Database of Notifications, Knowledge, and Information)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The `Space Weather Database Of Notifications, Knowledge, Information (DONKI) <https://ccmc.gsfc.nasa.gov/donki/>`_
is a comprehensive on-line tool for space weather forecasters, scientists, and the general space science community.
DONKI provides chronicles the daily interpretations of space weather observations, analysis, models, forecasts, and
notifications provided by the Space Weather Research Center (SWRC), comprehensive knowledge-base search
functionality to support anomaly resolution and space science research, intelligent linkages, relationships,
cause-and-effects between space weather activities and comprehensive webservice API access to information stored in
DONKI.

.. method:: Nasa.coronal_mass_ejection([start_date=None][, end_date=None][, accurate_only=True][, speed=0][, complete_entry=True][, half_angle=0][, catalog='ALL'][, keyword=None])

    Returns data collected on coronal mass ejection events.

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :param accurate_only: If True (default), only the most accurate results collected are returned.
    :param complete_entry: If True (default), only results with complete data is returned.
    :param speed: The lower limit of the speed of the CME event. Default is 0
    :param half_angle: The lower limit half angle of the CME event. Default is 0.
    :param catalog: Specifies which catalog of data to return results. Defaults to 'ALL' and must be one of {'ALL', 'SWRC_CATALOG', 'JANG_ET_AL_CATALOG'}.
    :param keyword: Filter results by a specific keyword.
    :rtype: list. List of results representing returned JSON data. If no data is returned, an empty dictionary is returned.

    .. code-block:: python

        # Initialize NASA API with a demo key
        n = Nasa()
        # View data from coronal mass ejection events from the last thirty days
        n.coronal_mass_ejection()
        # View all CME events from the beginning of 2019.
        n.coronal_mass_ejection(start_date='2019-01-01', end_date=datetime.datetime.today())

.. method:: Nasa.geomagnetic_storm([start_date=None][,end_date=None])

    Returns data collected on geomagnetic storm events.

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :rtype: list: List of results representing returned JSON data. If no data is returned, an empty dictionary is returned.

    .. code-block:: python

        # Initialize API connection with a Demo Key
        n = Nasa()
        # Get geomagnetic storm events from the last thirty days.
        n.geomagnetic_storm()

.. method:: Nasa.interplantary_shock([start_date=None][, end_date=None][, location='ALL'][, catalog='ALL'])

    Returns data collected on interplantary shock events.

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :param location: Filters returned results to specified location of the interplantary shock event. Defaults to 'ALL' and must be one of {'ALL', 'Earth', 'MESSENGER', 'STEREO A', 'STEREO B'}
    :param catalog: Filters results to a specified catalog of collected data. Defaults to 'ALL' and must be one of {'ALL', 'SWRC_CATALOG', 'WINSLOW_MESSENGER_ICME_CATALOG'}
    :rtype: list. List of results representing returned JSON data. If no data is returned, an empty list is returned.

.. method:: Nasa.solar_flare([start_date=None][, end_date=None])

    Returns data on solar flare events.

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :rtype: list. If data is available in the specified date range, a list of dictionary objects representing the data from the API is returned. If no data is available, an empty dictionary is returned.

    .. code-block:: python

        # Initialize API connection with a Demo Key
        n = Nasa()
        # Get solar flare events from May of 2019
        n.solar_flare(start_date='2019-05-01', end_date='2019-05-31')

.. method:: Nasa.solar_energetic_particle([start_date=None][, end_date=None])

    Returns data available related to solar energetic particle events.

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :rtype: list. If data is available in the specified date range, a list of dictionary objects representing the data from the API is returned. If no data is available, an empty dictionary is returned.

    .. code-block:: python

        # Initialize API connection with a Demo Key
        n = Nasa()
        # Get data from April 2017
        n.solar_energetic_particle(start_date='2017-04-01', end_date='2017-04-30')

.. method:: Nasa.magnetopause_crossing([start_date=None][, end_date=None])

    Returns data available related to magnetopause crossing events.

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :rtype: list. If data is available in the specified date range, a list of dictionary objects representing the data from the API is returned. If no data is available, an empty dictionary is returned.

    .. code-block:: python

        # Initialize API connection with a Demo Key
        n = Nasa()
        # Get data on magnetopause crossing events from 2018 to the current date.
        n.magnetopause_crossing(start_date='2018-01-01')

.. method:: Nasa.radiation_belt_enhancement([start_date=None][, end_date=None])

    Returns data available related to radiation belt enhancement events.

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :rtype: list. If data is available in the specified date range, a list of dictionary objects representing the data from the API is returned. If no data is available, an empty dictionary is returned.

    .. code-block:: python

        # Initialize API connection with a Demo Key
        n = Nasa()
        # Get data on radiation belt enhancement events from the last 30 days.
        n.radiation_belt_enhancement()

.. method:: Nasa.hight_speed_stream([start_date=None][, end_date=None])

    Returns data available related to hight speed stream events.

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :rtype: list. If data is available in the specified date range, a list of dictionary objects representing the data from the API is returned. If no data is available, an empty dictionary is returned.

    .. code-block:: python

        # Initialize API connection with a Demo Key
        n = Nasa()
        # Get data on hight speed stream events from the beginning of September 2019.
        n.hight_speed_stream()

.. method:: Nasa.wsa_enlil_simulation([start_date=None][, end_date=None])

    :param start_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to 30 days prior to the current date in UTC time.
    :param end_date: String representing a date in YYYY-MM-DD format or a datetime object. If None, defaults to the current date in UTC time.
    :rtype: list. If data is available in the specified date range, a list of dictionary objects representing the data from the API is returned. If no data is available, an empty dictionary is returned.

    .. code-block:: python

        # Initialize API connection with a Demo Key
        n = Nasa()
        # Get data from the first simulation performed in 2019.
        wsa = n.wsa_enlil_simulation(start_date='2019-01-01')

EPIC (Earth Polychromatic Imaging Camera)
+++++++++++++++++++++++++++++++++++++++++

The EPIC API provides information on the daily imagery collected by DSCOVR's Earth Polychromatic Imaging Camera
(EPIC) instrument. Uniquely positioned at the Earth-Sun Lagrange point, EPIC provides full disc imagery of the
Earth and captures unique perspectives of certain astronomical events such as lunar transits using a 2048x2048
pixel CCD (Charge Coupled Device) detector coupled to a 30-cm aperture Cassegrain telescope.

.. method:: Nasa.epic([color='natural'][, date=None][, available=False])

    :param color: Specifies the type of imagery to return. Must be one of 'natural' (default) or 'enhanced'
    :param date: String representing a date in 'YYYY-MM-DD' format or a datetime object
    :param available: Alternative listing of all dates with specified color imagery
    :rtype: list. List of dictionaries representing the returned JSON data from the EPIC API.

    .. code-block:: python

        # Initialize API connection with a Demo Key
        n = Nasa()
        # Get EPIC data from the beginning of 2019.
        e = n.epic(date='2019-01-01')
        # Print the first result
        e[0]

Earth Satellite Imagery
+++++++++++++++++++++++

This endpoint retrieves the Landsat 8 image for the supplied location and date. The response will include the date
and URL to the image that is closest to the supplied date. The requested resource may not be available for the
exact date in the request.

.. method:: Nasa.earth_imagery(lat, lon[, dim=0.025][, date=None][, cloud_score=False])

    Retrieves the URL and other information from the Landsat 8 image database for the specified lat/lon location and date.

    :param lat: Latitude of the desired imagery location
    :param lon: Longitude of the desired imagery location
    :param dim: Width and height of the image in degrees.
    :param date: Date the image was taken. If specified, must be a string representing a date in 'YYYY-MM-DD' format or a datetime object. If None, the most recent image available from the current date is returned.
    :param cloud_score: Calculate the percentage of the image covered by clouds.
    :rtype: dict. Dictionary object representing the returned JSON data from the API.

    .. code-block:: python

        # Initialize API connection with a Demo Key
        n = Nasa()
        # Get imagery at latitude 1.5, longitude 100.75 and include the computed cloud score calculation.
        n.earth_imagery(lon=100.75, lat=1.5, cloud_score=True)

.. method:: Nasa.earth_assets(lat, lon[, dim=0.025][, begin_date=None][, end_date=None])

    Retrieves the datetimes and asset names of available imagery for a specified lat-lon location over a given date range. The satellite that takes the images passes over each point approximately once every sixteen days.

    :param lat: Latitude of the desired imagery location
    :param lon: Longitude of the desired imagery location
    :param begin_date: Beginning of date range in which to search for available assets. Must be a string representing a date in 'YYYY-MM-DD' format or a datetime object
    :param end_date: End of date range in which to search for available assets. If not specified, defaults to the current date. If specified, Must be a string representing a date in 'YYYY-MM-DD' format or a datetime object
    :rtype: dict. Dictionary object representing the returned JSON data from the API.

Mars Rover Photos
+++++++++++++++++

.. method:: Nasa.mars_rover([sol=None][, earth_date=None][, camera='all'][, rover='curiosity'][, page=1])

    Retrieves image data collected by the Mars rovers Curiosity, Discovery and Spirit.

    :param sol: The sol (Martian rotation or day) on which the images were collected. Either this parameter or :code:`earth_date` must be provided. The parameter :code:`earth_date` is an alternative parameter for searching for a specific date. The sol values count up from the rover's landing date, for example, the Curiosity's 100th sol would be the 100th Martian rotation since the rover landed.
    :param earth_date: Alternative search parameter for finding data on a specific date. Must be a string representing a date in 'YYYY-MM-DD' format or a datetime object. Either :code:`earth_date` or :code:`sol` must be specified.
    :param camera: Filter results to a specific camera on the Mars Curiosity, Opportunity or Spirit rovers. Defaults to 'all', which includes all cameras and must be one of {'all', FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', 'MAHLI', 'MARDI', 'NAVCAM', 'PANCAM', 'MINITES'}
    :param rover: Specifies the Mars rover to return data. Defaults to the Curiosity rover which has more available cameras. Must be one of {'curiosity', 'opportunity', 'spirit'}
    :param page: Page number of results to return. 25 results per page are returned.
    :rtype: list. List of dictionaries representing the returned JSON data from the Mars Rover API.

GeneLab Search
++++++++++++++

.. method:: Nasa.genelab_search(term=None, database='cgene', page=0, size=25, sort=None, order='desc', ffield=None, fvalue=None)

    Retrieves available data from the GeneLab and other bioinformatics databases such as the National Institutes
    of Health (NIH) / National Center for Biotechnology Information (NCBI), Gene Expression Omnibus (GEO), the
    European Bioinformatics Institute's (EBI) Proteomics Identification (PRIDE), and the Argonne National
    Laboratory's (ANL) Metagenomics Rapid Annotations using Subsystems Technology (MG-RAST).

    :param term: Search by specific keyword(s). Case-insensitive boolean operators (AND, OR, NOT) can be used as well to include and filter specific keywords.
    :param database: Determines the database(s) to query. Defaults to the 'cgene' (GeneLab) database, but other available databases include 'nih_geo_gse' (NIH GEO), 'ebi_pride' (EBI PRIDE), or 'mg_rast' (MG-RAST). Multiple databases can be queried by separating values with commas. For example, 'cgene,nih_geo_gse,ebi_pride,mg_rast' will query all available databases.
    :param page: Specifies the page of results to return. Defaults to the first page (0).
    :param size: Specifies the number of results to return per page. Default is 25 results per page.
    :param sort: Sorts by a specific field name in the returned JSON data.
    :param order: Determines the sorting order. Must be one of 'desc' (descending) or 'asc' (ascending).
    :param ffield: Filters the returned data based on the defined field. Should be paired with the :code:`fvalue` parameter. Only the 'cgene' (GeneLab) database can be filtered.
    :param fvalue: Filters the returned data based on value or values in the specified :code:`ffield` parameter field. Only the 'cgene' (GeneLab) database can be filtered.
    :rtype: dict. Dictionary object representing the returned JSON data.

Techport
++++++++

The NASA TechPort system provides an API to make technology project data available in a machine-readable format.
This API can be used to export TechPort data into either an XML or a JSON format.

.. method:: Nasa.techport([project_id=None][, last_updated=None][, return_format='json'])

    Retrieves available NASA project data.

    :param project_id: The ID of the project record. If not specified, all available projects will be returned.
    :param last_updated: Returns projects only updated after the specified date. Must be a string representing a date in 'YYYY-MM-DD' format or a datetime object.
    :param return_format: Specifies the return format of the data. Defaults to 'json', but 'xml' formatted data is also available.
    :rtype: dict or str. If :code:`return_format` is 'json', a dictionary representing the JSON formatted data is returned. Otherwise, a string formatted for XML is returned.

TLE (Two-Line Element Set Data)
+++++++++++++++++++++++++++++++

The TLE API provides up to date two line element set records, the data is updated daily from CelesTrak and served
in JSON format. A two-line element set (TLE) is a data format encoding a list of orbital elements of an
Earth-orbiting object for a given point in time.

.. method:: tle([search_satellite=None][, satellite_number=None])

    Returns two-line element set records provided by CelesTrak.

    :param search_satellite: Searches satellites by name designation.
    :param satellite_number: Specfic satellite ID number.
    :rtype: dict. Specfic satellite ID number.

    .. code-block:: python

        tle(satellite_number=43553)

NASA Image and Video Library
++++++++++++++++++++++++++++

.. method:: media_search([query=None][, center=None][, description=None][, keywords=None][, location=None][, media_type=None][, nasa_id=None][, page=1][, photographer=None][, secondary_creator=None][, title=None][, year_start=None][, year_end=None])

    Performs a general search for images from the images.nasa.gov API based on parameters and criteria specified.
    At least one parameter must be provided.

    :param query: Query terms to search.
    :param center: NASA center that published the results.
    :param description: Search for specific terms in the 'description' field of the resulting data.
    :param keywords: Search and filter for specific terms in the 'keywords' field of the resulting data. Multiple values should be comma-separated.
    :param location: Filter terms in the 'locations' field of the resulting data.
    :param media_type: Filter results to specific media types. Options include 'image', 'audio', 'image,audio', 'audio,image'. The default :code:`None` includes all media types.
    :param nasa_id: The media asset's NASA ID.
    :param page: Page number of results to return. Starts at 1.
    :param photographer: The primary photographer's name.
    :param secondary_creator: A secondary photographer/videographer's name.
    :param title: Search terms in the 'title' field of the resulting data.
    :param year_start: The start year for results. If provided, must be a string representing a year in YYYY format or a datetime object.
    :param year_end: The end year for results. If provided, must be a string representing a year in YYYY format or a datetime object.
    :rtype: dict. Dictionary containing matching search results.

    .. code-block:: python

        # Search for media related to 'apollo 11' with 'moon landing' in the description of the items.
        r = media_search(query='apollo 11', description='moon landing')
        # Output the first returned media item from the resulting collection.
        r['items'][0]

.. method:: media_asset_manifest(nasa_id)

    Returns the media asset's manifest, which contains the available versions of the asset and it's metadata
    location.

    :param nasa_id: The ID of the media asset.
    :rtype: list. List of dictionaries containing the media asset's manifest.

    .. code-block:: python

        # Get the manifest for the NASA media asset 'as11-40-5874'
        media_asset_manifest(nasa_id='as11-40-5874')


.. method:: media_asset_metadata(nasa_id)

    Retrieves the specified media asset's metadata.

    :param nasa_id: The ID of the media asset.
    :rtype: dict. Dictionary containing the metadata of the provided media asset ID.


.. method:: media_asset_captions(nasa_id)

    Retrieves the captions and location of the captions .srt file for a media asset from the NASA image API.

    :param nasa_id: The ID of the media asset.
    :rtype: dict. Dictionary object containing the resulting data from the API given the media asset ID. The dictionary will contain two keys, :code:`location` and :code:`captions`. The :code:`location` key can be used to download the .srt file directly while the :code:`captions` key can be used in conjunction with a library such as srt for parsing media asset captions.

Solar System Dynamics (SSD) and Center for Near-Earth Object Studies (CNEOS)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The following functions provide a Pythonic interface for NASA's `Solar System Dynamics <https://ssd.jpl.nasa.gov/>`_
and `Center for Near-Earth Object Studies <https://cneos.jpl.nasa.gov/>`_ APIs.

.. method:: close_approach([date_min='now'][, date_max='+60'][, dist_min=None][, dist_max='0.05'][, h_min=None][, h_max=None][, v_inf_min=None][, v_inf_max=None][, v_rel_min=None][, v_rel_max=None][, orbit_class=None][, pha=False][, nea=False][, comet=False][, nea_comet=False][, neo=False][, kind=None][, spk=None][, des=None][, body='Earth'][, sort='date'][, limit=None][, fullname=False])

    Provides data for currently known close-approach data for all asteroids and comets in NASA's Jet Propulsion
    Laboratory's (JPL) `Small-Body Database <https://ssd.jpl.nasa.gov/sbdb.cgi>`_.

    :param date_min: Excludes data earlier than the given date. Defaults to 'now', representing the current date, but can also be a string representing a date in 'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    :param date_max: Excludes data later than the given date. Defaults to '+60', representing 60 days after the :code:`date_min` parameter. Accepts a string of '+D' where D represents the number of days or a string representing a date in 'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object. 'now' is also an acceptable value and will exclude date later than the current date.
    :param dist_min: Excludes data with an approach distance less than the given value (if provided). The default unit is AU (astronomical units), and LD (lunar distance) is also available. For example, '0.05' or 0.05 would return AU units whereas '0.05LD' would return LD units.
    :param dist_max: Excludes data with an approach distance greater than the given value (if specified). The default unit is AU (astronomical units), and LD (lunar distance) is also available. For example, '0.05' would return AU units whereas '0.05LD' would return LD units.
    :param h_min: Exclude data from objects with H-values less than the given value.
    :param h_max: Exclude data from objects with H-values greater than the given value.
    :param v_inf_min: Exclude data with V-infinity less than this positive value in km/s
    :param v_inf_max: Exclude data with V-infinity greater than this positive value in km/s
    :param v_rel_min: Exclude data with V-relative less than this positive value in km/s
    :param v_rel_max: Exclude data with V-relative greater than this positive value in km/s
    :param orbit_class: Limits data to specified orbit-class
    :param pha: If True, limits the resulting data to only PHA objects
    :param nea: If True, limits the returned data to only NEA objects
    :param comet: If True, limits the returned data to comet objects only
    :param nea_comet: If True, limits the returned data to NEA comet objects only
    :param neo: If True, limits the returned data to only NEO objects
    :param kind: Filters returned data to specified type of object. Available options include 'a'=asteroid, 'an'=numbered-asteroids, 'au'=unnumbered-asteroids, 'c'=comets, 'cn'=numbered-comets, 'cu'=unnumbered-comets, 'n'=numbered-objects, and 'u'=unnumbered-objects
    :param spk: Return data only for the matching SPK-ID.
    :param des: Filters data to objects matching the given destination.
    :param body: Filters data to close-approaches of the specified body. 'ALL' or '*' returns all close-approaches to the available bodies.
    :param sort: Sorts the returned data by the specified field. Defaults to 'date' ascending. To sort by descending, add a '-' in front of the sort value, for example, '-date'.
    :param limit: Limit data to the first number of results specified by the parameter. Must be greater than 0.
    :param fullname: Includes the full-format object name/designation
    :rtype: dict

    .. code-block:: python

        # Get all close-approach object data in the year 2019 with a maximum approach distance of 0.01AU.
        >>> nasapy.close_approach(date_min='2019-01-01', date_max='2019-12-31', dist_max=0.01)
        # Get close-approach data for asteroid 433 Eros within 0.2AU from the years 1900 to 2100.
        >>> nasapy.close_approach(des='433', date_min='1900-01-01', date_max='2100-01-01', dist_max=0.2)


.. method:: fireballs([date_min=None][, date_max=None][, energy_min=None][, energy_max=None][, impact_e_min=None][, impact_e_max=None][, vel_min=None][, vel_max=None][, alt_min=None][, alt_max=None][, req_loc=False][, req_alt=False][, req_vel=False][, req_vel_comp=False][, vel_comp=False][, sort='date'][, limit=None])

    Returns available data on fireballs (objects that burn up in the upper atmosphere of Earth).

    :param date_min: Excludes data earlier than the given date. Can be a string representing a date in 'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    :param date_max: Excludes data later than the given date. Can be a string representing a date in 'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    :param energy_min: Excludes data with total-radiated-energy less than the positive value of the specified value in joules :math:`\times 10^{10}`.
    :param energy_max: Excludes data with total-radiated-energy greater than the positive value of the specified value in joules :math:`\times 10^{10}`.
    :param impact_e_min: Excludes data with estimated impact energy less than the positive value of the specified value in kilotons (kt)
    :param impact_e_max: Excludes data with estimated impact energy greater than the positive value of the specified value in kilotons (kt)
    :param vel_min: Excludes data with velocity-at-peak-brightness less than the positive value of the specified value in km/s
    :param vel_max: Excludes data with velocity-at-peak-brightness greater than the positive value of the specified value in km/s
    :param alt_min: Excludes data from objects with an altitude less than the specified value
    :param alt_max: Excludes data from objects with an altitude greater than the specified value
    :param req_loc: If True, latitude and longitude required for object to be included in results.
    :param req_alt: If True, objects without an altitude are excluded.
    :param req_vel: If True, objects without a velocity are not included in results.
    :param req_vel_comp: If True, excludes objects without velocity components.
    :param vel_comp: If True, include velocity components
    :param sort: Sorts data on specified field. Default sort order is ascending, for descending, prepend a '-'. For example, for date descending, the sort value would be '-date'.
    :param limit: Limits data to the first number of results specified. Must be greater than 0 if passed.
    :rtype: dict.

    .. code-block:: python

        # Get all available data in reverse chronological order
        >>> n = nasapy.fireballs()
        # Return the earlieset record
        >>> nasapy.fireballs(limit=1)
        # Get data from the beginning of 2019
        >>> nasapy.fireballs(date_min='2019-01-01')

