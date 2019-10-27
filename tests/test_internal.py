import pytest
import os
import datetime

from nasapy.nasa import _check_dates, _donki_request


key = os.environ.get('NASA_KEY')


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