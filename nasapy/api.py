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


def close_approach_data(date_min='now', date_max='+60', dist_min=None, dist_max=0.05, h_min=None, h_max=None,
                        v_inf_min=None, v_inf_max=None, v_rel_min=None, v_rel_max=None, orbit_class=None, pha=False,
                        nea=False, comet=False, nea_comet=False, neo=True, kind=None, spk=None, des=None,
                        body='Earth', sort='date', limit=None, fullname=False):
    url = 'https://ssd-api.jpl.nasa.gov/cad.api'


def fireballs(date_min=None, date_max=None, energy_min=None, energy_max=None, impact_e_min=None, impact_e_max=None,
              vel_min=None, vel_max=None, alt_min=None, alt_max=None, req_loc=False, req_alt=False, req_vel=False,
              req_vel_comp=False, vel_comp=False, sort='-date', limit=None):
    url = 'https://ssd-api.jpl.nasa.gov/fireball.api'


def _donki_request(key, url, start_date=None, end_date=None):
    r"""

    Parameters
    ----------

    Returns
    -------

    """
    start_date, end_date = _check_dates(start_date=start_date, end_date=end_date)

    r = requests.get(url,
                     params={
                         'api_key': key,
                         'startDate': start_date,
                         'endDate': end_date
                     })

    limit_remaining = r.headers['X-RateLimit-Remaining']

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.reason, r.url)

    if r.text == '':
        r = {}
    else:
        r = r.json()

    return limit_remaining, r


def _check_dates(start_date=None, end_date=None):
    r"""

    Parameters
    ----------

    Returns
    -------

    """
    if start_date is not None:
        if not isinstance(start_date, (str, datetime.datetime)):
            raise TypeError('start_date parameter must be a string representing a date in YYYY-MM-DD format or '
                            'a datetime object.')

    if end_date is not None:
        if not isinstance(end_date, (str, datetime.datetime)):
            raise TypeError('end_date parameter must be a string representing a date in YYYY-MM-DD format or '
                            'a datetime object.')

        if isinstance(end_date, datetime.datetime):
            end_date = end_date.strftime('%Y-%m-%d')

    if isinstance(start_date, datetime.datetime):
        start_date = start_date.strftime('%Y-%m-%d')

    return start_date, end_date


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
