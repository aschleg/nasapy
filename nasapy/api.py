# encoding=utf-8

"""

"""


import datetime
import requests


def tle(search_satellite=None, satellite_number=None):
    r"""
    Returns two-line element set records provided by CelesTrak. A two-line element set (TLE) is a data format
    encoding a list of orbital elements of an Earth-orbiting object for a given point in time.

    Parameters
    ----------
    search_satellite : str, default None
        Searches satellites by name designation.
    satellite_number : str, int, default None
        Specfic satellite ID number.

    Returns
    -------
    dict
        Dictionary object representing the returned JSON data.

    Examples
    --------
    # The TLE endpoint does not require API authentication, thus we can call the function without initializing the
    # Nasa class
    # Retrieve available data for a specific satellite ID.
    >>> tle(satellite_number=43553)
    {'@id': 'https://data.ivanstanojevic.me/api/tle/43553',
     '@type': 'TleModel',
     'satelliteId': 43553,
     'name': '1998-067PB',
     'date': '2019-10-14T19:13:21+00:00',
     'line1': '1 43553U 98067PB  19287.80094257  .00010817  00000-0  12491-3 0  9999',
     'line2': '2 43553  51.6389 108.1812 0005967 223.4274 136.6250 15.62481474 71504'}

    """
    url = 'https://data.ivanstanojevic.me/api/tle'

    if search_satellite is not None:
        r = requests.get(url,
                         params={'search': search_satellite})

    elif satellite_number is not None:
        url = url + '/{satellite_number}'.format(satellite_number=satellite_number)

        r = requests.get(url)

    else:
        r = requests.get(url)

    if r.status_code == 404:
        raise requests.exceptions.HTTPError(r.json()['response']['message'])

    return r.json()


def media_search(query=None, center=None, description=None, keywords=None, location=None, media_type=None,
                 nasa_id=None, page=1, photographer=None, secondary_creator=None, title=None, year_start=None,
                 year_end=None):
    r"""
    Performs a general search for images from the images.nasa.gov API based on parameters and criteria specified.
    At least one parameter must be provided.

    Parameters
    ----------
    query : str, None (default)
        Query terms to search.
    center : str, None (default)
        NASA center that published the results.
    description :  str, None (default)
        Search for specific terms in the 'description' field of the resulting data.
    keywords : str, None (default)
        Search for specific terms in the 'keywords' field of the resulting data. Multiple values should be
        comma-separated.
    location : str, None (default)
        Search for terms in the 'locations' field of the resulting data.
    media_type : str, {None, 'image', 'audio', 'image,audio', 'audio,image'}
        Filter results to specific media types. Options include 'image', 'audio', 'image,audio', 'audio,image'.
        The default :code:`None` includes all media types.
    nasa_id : str, None (default)
        The media asset's NASA ID.
    page : int, 1 (default)
        Page number of results to return. Starts at 1.
    photographer : str, None (default)
        The primary photographer's name.
    secondary_creator : str, None (default)
        A secondary photographer/videographer's name.
    title : str, None (default)
        Search terms in the 'title' field of the resulting data.
    year_start : str, datetime, None (default)
        The start year for results. If provided, must be a string representing a year in YYYY format or a
        datetime object.
    year_end : str, datetime, None (default)
        The end year for results. If provided, must be a string representing a year in YYYY format or a
        datetime object.

    Raises
    ------
    ValueError
        Raised if no parameters are specified.
    ValueError
        Raised if the :code:`media_type` parameter is not one of 'image', 'audio', 'image,audio', 'audio,image'
        (if specified).
    TypeError
        Raised if :code:`year_start` parameter (if provided) is not a string or a datetime object.
    TypeError
        Raised if :code:`year_end` parameter (if provided) is not a string or a datetime object.

    Returns
    -------
    dict
        Dictionary containing matching search results.

    Examples
    --------
    # Initialize API connection
    >>> n = Nasa()
    # Search for media related to 'apollo 11' with 'moon landing' in the description of the items.
    >>> r = n.media_search(query='apollo 11', description='moon landing')
    # Print the first returned media item from the resulting collection.
    >>> r['items'][0]
    {'href': 'https://images-assets.nasa.gov/video/Apollo 11 Overview/collection.json',
     'data': [{'description': 'Video highlights from the historic first manned landing on the moon, during the Apollo 11 mission in July 1969.',
       'date_created': '2013-05-15T00:00:00Z',
       'nasa_id': 'Apollo 11 Overview',
       'media_type': 'video',
       'keywords': ['Apollo 11', 'Moon'],
       'center': 'HQ',
       'title': 'Apollo 11 Overview'}],
     'links': [{'href': 'https://images-assets.nasa.gov/video/Apollo 11 Overview/Apollo 11 Overview~thumb.jpg',
       'rel': 'preview',
       'render': 'image'},
      {'href': 'https://images-assets.nasa.gov/video/Apollo 11 Overview/Apollo 11 Overview.srt',
       'rel': 'captions'}]}

    """
    url = 'https://images-api.nasa.gov/search'

    if all(p is None for p in (query, center, description, keywords, location, media_type, nasa_id,
                               photographer, secondary_creator, title, year_start, year_end)):
        raise ValueError('at least one parameter is required')

    if media_type is not None:
        if media_type not in ('image', 'audio', 'image,audio', 'audio,image'):
            raise ValueError("media_type parameter must be one of 'image' or 'audio' or a combination of both "
                             "('image,audio' or 'audio,image'.")

    if year_start is not None:
        if not isinstance(year_start, (str, datetime.datetime)):
            raise TypeError('year start parameter must be a string representing a year in YYYY format or a '
                            'datetime object.')

        if isinstance(year_start, datetime.datetime):
            year_start = year_start.strftime('%Y')

    if year_end is not None:
        if not isinstance(year_end, (str, datetime.datetime)):
            raise TypeError('year end parameter must be a string representing a year in YYYY format or a '
                            'datetime object.')

        if isinstance(year_end, datetime.datetime):
            year_end = year_end.strftime('%Y')

    r = requests.get(url,
                     params={
                         'q': query,
                         'center': center,
                         'description': description,
                         'keywords': keywords,
                         'location': location,
                         'media_type': media_type,
                         'nasa_id': nasa_id,
                         'page': page,
                         'photographer': photographer,
                         'secondary_creator': secondary_creator,
                         'title': title,
                         'year_start': year_start,
                         'year_end': year_end
                     })

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.reason, r.url)

    else:
        return r.json()['collection']


def media_asset_manifest(nasa_id):
    r"""
    Returns the media asset's manifest, which contains the available versions of the asset and it's metadata
    location.

    Parameters
    ----------
    nasa_id : str
        The ID of the media asset.

    Returns
    -------
    list
        List of dictionaries containing the media asset's manifest.

    Examples
    --------
    # Initialize API connection with a Demo Key
    >>> n = Nasa()
    # Get the manifest for the NASA media asset 'as11-40-5874'
    >>> n.media_asset_manifest(nasa_id='as11-40-5874')
    [{'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~orig.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~large.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~medium.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~small.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/as11-40-5874~thumb.jpg'},
     {'href': 'http://images-assets.nasa.gov/image/as11-40-5874/metadata.json'}]

    """
    return _media_assets(endpoint='asset', nasa_id=nasa_id)


def media_asset_metadata(nasa_id):
    r"""
    Retrieves the specified media asset's metadata.

    Parameters
    ----------
    nasa_id : str
        The ID of the media asset.

    Returns
    -------
    dict
        Dictionary containing the metadata of the provided media asset ID.

    """
    return _media_assets(endpoint='metadata', nasa_id=nasa_id)


def media_asset_captions(nasa_id):
    r"""
    Retrieves the captions and location of the captions .srt file for a media asset from the NASA image API.

    Parameters
    ----------
    nasa_id : str
        The ID of the media asset.

    Returns
    -------
    dict
        Dictionary object containing the resulting data from the API given the media asset ID. The dictionary will
        contain two keys, :code:`location` and :code:`captions`. The :code:`location` key can be used to
        download the .srt file directly while the :code:`captions` key can be used in conjunction with a library
        such as srt for parsing media asset captions.

    """
    return _media_assets(endpoint='captions', nasa_id=nasa_id)


def close_approach_data(date_min='now', date_max='+60', dist_min=None, dist_max='0.05', h_min=None, h_max=None,
                        v_inf_min=None, v_inf_max=None, v_rel_min=None, v_rel_max=None, orbit_class=None, pha=False,
                        nea=False, comet=False, nea_comet=False, neo=False, kind=None, spk=None, des=None,
                        body='Earth', sort='date', limit=None, fullname=False):
    r"""
    Provides data for currently known close-approach data for all asteroids and comets in NASA's Jet Propulsion
    Laboratory's (JPL) Small-Body Database.

    Parameters
    ----------
    date_min : str, datetime, default 'now'
        Excludes data earlier than the given date. Defaults to 'now', representing the current date, but can also be
        a string representing a date in 'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    date_max :'str, datetime, 'now', default '+60'
        Excludes data later than the given date. Defaults to '+60', representing 60 days after the :code:`date_min`
        parameter. Accepts a string of '+D' where D represents the number of days or a string representing a date in
        'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object. 'now' is also an acceptable value
        and will exclude date later than the current date.
    dist_min : str, float, int, default None
        Excludes data with an approach distance less than the given value (if provided). The default unit is AU
        (astronomical units), and LD (lunar distance) is also available. For example, '0.05' would return AU units
        whereas '0.05LD' would return LD units.
    dist_max : str, float int, default None
        Excludes data with an approach distance greater than the given value (if specified). The default unit is AU
        (astronomical units), and LD (lunar distance) is also available. For example, '0.05' would return AU units
        whereas '0.05LD' would return LD units.
    h_min : float, int, default None
        Exclude data from objects with H-values less than the given value.
    h_max : float, int, default None
        Exclude data from objects with H-values greater than the given value.
    v_inf_min : float, int, default None
        Exclude data with V-infinity less than this positive value in km/s
    v_inf_max : float, int, default None
        Exclude data with V-infinity greater than this positive value in km/s
    v_rel_min : float, int, default None
        Exclude data with V-relative less than this positive value in km/s
    v_rel_max : float, int, default None
        Exclude data with V-relative greater than this positive value in km/s
    orbit_class : str
        Limits data to specified orbit-class.
    pha : bool, default False
    nea : bool, default False
    comet : bool, default False
    nea_comet : bool, default False
    neo : bool, default False
    kind : str, {'a', 'an', 'au', 'c', 'cn', 'cu', 'n', 'u'}, default None
        Filters returned data to specified type of object. Available options include 'a'=asteroid,
        'an'=numbered-asteroids, 'au'=unnumbered-asteroids, 'c'=comets, 'cn'=numbered-comets, 'cu'=unnumbered-comets,
        'n'=numbered-objects, and 'u'=unnumbered-objects
    spk : str, int, default None
        Return data only for the matching SPK-ID.
    des : str, default None
        Filters data to objects matching the given destination.
    body : str, default "Earth"
        Filters data to close-approaches of the specified body. 'ALL' or '*' returns all close-approaches to the
        available bodies.
    sort : str, {'date', 'dist', 'dist-min', 'v-inf', 'v-rel', 'h', 'object'}
        Sorts the returned data by the specified field. Defaults to 'date' ascending. To sort by descending, add a '-'
        in front of the sort value, for example, '-date'.
    limit : int, default None
        Limit data to the first number of results specified by the parameter. Must be greater than 0.
    fullname : bool, default False
        Includes the full-format object name/designation

    Raises
    ------

    Returns
    -------
    dict

    """
    url = 'https://ssd-api.jpl.nasa.gov/cad.api'

    if h_min is not None and h_max is not None:
        if h_min > h_max:
            raise ValueError('h_min parameter must be less than h_max')

    if v_inf_min is not None and v_inf_max is not None:
        if v_inf_min > v_inf_max:
            raise ValueError('v_inf_min parameter must be less than v_inf_max')

    if v_rel_min is not None and v_rel_max is not None:
        if v_rel_min > v_rel_max:
            raise ValueError('v_rel_min parameter must be less than v_rel_max')

    if limit is not None:
        if not isinstance(limit, int):
            raise TypeError('limit parameter must be an integer (if specified)')

        elif limit <= 0:
            raise ValueError('limit parameter must be greater than 0')

    if not isinstance(pha, bool):
        raise TypeError('pha parameter must be boolean (True or False)')

    if not isinstance(nea, bool):
        raise TypeError('nea parameter must be boolean (True or False)')

    if not isinstance(comet, bool):
        raise TypeError('comet parameter must be boolean (True or False)')

    if not isinstance(neo, bool):
        raise TypeError('neo parameter must be boolean (True or False)')

    if not isinstance(fullname, bool):
        raise TypeError('fullname parameter must be boolean (True or False)')

    r = requests.get(url,
                     params={
                         'date-min': date_min,
                         'date-max': date_max,
                         'dist-min': dist_min,
                         'dist-max': dist_max,
                         'h-min': h_min,
                         'h-max': h_max,
                         'v-inf-min': v_inf_min,
                         'v-inf-max': v_inf_max,
                         'v-rel-min': v_rel_min,
                         'v-rel-max': v_rel_max,
                         'class': orbit_class,
                         'pha': pha,
                         'nea': nea,
                         'comet': comet,
                         'nea-comet': nea_comet,
                         'neo': neo,
                         'kind': kind,
                         'spk': spk,
                         'des': des,
                         'body': body,
                         'sort': sort,
                         'limit': limit,
                         'fullname': fullname
                     })

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.reason, r.url)

    else:
        return r.json()


def fireballs(date_min=None, date_max=None, energy_min=None, energy_max=None, impact_e_min=None, impact_e_max=None,
              vel_min=None, vel_max=None, alt_min=None, alt_max=None, req_loc=False, req_alt=False, req_vel=False,
              req_vel_comp=False, vel_comp=False, sort='-date', limit=None):
    r"""
    Returns available data on fireballs (objects that burn up in the upper atmosphere of Earth)

    Parameters
    ----------
    date_min : str, datetime, default None
        Excludes data earlier than the given date. Can be a string representing a date in 'YYYY-MM-DD' format or
        'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    date_max : str, datetime, default None
        Excludes data later than the given date. Can be a string representing a date in 'YYYY-MM-DD' format or
        'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    energy_min : int, float, default None
        Excludes data with total-radiated-energy less than the positive value of the specified value in joules
        :math:`\times 10^{10}`.
    energy_max : int, float, default None
        Excludes data with total-radiated-energy greater than the positive value of the specified value in joules
        :math:`\times 10^{10}`.
    impact_e_min : int, float, default None
        Excludes data with estimated impact energy less than the positive value of the specified value in kilotons (kt)
    impact_e_max : int, float, default None
        Excludes data with estimated impact energy greater than the positive value of the specified value in kilotons
        (kt)
    vel_min : int, float, default None

    vel_max : int, float, default None
    alt_min : int, float, default None
    alt_max : int, float, default None
    req_loc : bool, default False
    req_alt : bool, default False
    req_vel : bool, default False
    req_vel_comp : bool, default False
    vel_comp : bool, default False
    sort : str, {'-date', 'energy', 'impact-e', 'vel', 'alt'}
    limit : int, default None
        Limits data to the first number of results specified. Must be greater than 0 if passed.

    Raises
    ------

    Returns
    -------

    """
    url = 'https://ssd-api.jpl.nasa.gov/fireball.api'

    if vel_min is not None and vel_max is not None:
        if vel_min > vel_max:
            raise ValueError('vel_min parameter must be less than vel_max')

    if alt_min is not None and alt_max is not None:
        if alt_min > alt_max:
            raise ValueError('alt_min parameter must be less than alt_max')

    if not isinstance(req_loc, bool):
        raise TypeError('req_loc parameter must be boolean (True or False)')

    if not isinstance(req_alt, bool):
        raise TypeError('req_alt parameter must be boolean (True or False)')

    if not isinstance(req_vel, bool):
        raise TypeError('req_vel parameter must be boolean (True or False)')

    if not isinstance(req_vel_comp, bool):
        raise TypeError('req_vel_comp parameter must be boolean (True or False)')

    if not isinstance(vel_comp, bool):
        raise TypeError('vel_comp parameter must be boolean (True or False)')

    if limit is not None:
        if not isinstance(limit, int):
            raise TypeError('limit parameter must be an integer (if specified)')

        elif limit <= 0:
            raise ValueError('limit parameter must be greater than 0')

    r = requests.get(url,
                     params={
                         'date-min': date_min,
                         'date-max': date_max,
                         'energy-min': energy_min,
                         'energy-max': energy_max,
                         'impact-e-min': impact_e_min,
                         'impact-e-max': impact_e_max,
                         'vel-min': vel_min,
                         'vel-max': vel_max,
                         'alt-min': alt_min,
                         'alt-max': alt_max,
                         'req-loc': req_loc,
                         'req-alt': req_alt,
                         'req-vel': req_vel,
                         'req-vel-comp': req_vel_comp,
                         'vel-comp': vel_comp,
                         'sort': sort,
                         'limit': limit
                     })

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.reason, r.url)

    else:
        return r.json()


def mission_design(des, spk, sstr, orbit_class, mjd0, span, tof_min, tof_max, step):
    pass


def _media_assets(endpoint, nasa_id):
    url = 'https://images-api.nasa.gov/{endpoint}/{nasa_id}'

    r = requests.get(url.format(endpoint=endpoint,
                                nasa_id=nasa_id))

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.reason, r.url)

    else:
        if endpoint == 'asset':
            return r.json()['collection']['items']

        elif endpoint == 'metadata':
            location = r.json()['location']
            r = requests.get(location).json()
            r['location'] = location

            return r

        elif endpoint == 'captions':
            location = r.json()['location']
            r = requests.get(location).text

            r = {
                'location': location,
                'captions': r
            }

    return r
