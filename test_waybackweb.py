import pytest

from datetime import datetime
from waybackweb import WayBackWebEntry, WrongURLFormatInputException, WrongArticleDateInputException, \
    NoWaybackSnapShotsError, WaybackRequestError

datestring = "12/07/2019"
other_datestring = "07/12/2019"
faulty_url = "example.com"
good_https_url = "https://example.com"
good_http_url = "http://example.com"

existing_archive_link = "http://www.google.com"
inexistant_archive_link = "http://thisprobablyshouldnotexist.hellno"

expected_urlprop_example = "http://web.archive.org/web/20190711235958/https://www.google.com/"


def test_new_wbe_object_date_type():
    with pytest.raises(WrongArticleDateInputException) as excep:
        WayBackWebEntry(article_date=datestring, url=faulty_url)
    assert "<class 'str'>" in str(excep.value)


def test_new_wbe_object_wrong_url():
    dto = datetime.strptime(datestring, "%d/%m/%Y")
    with pytest.raises(WrongURLFormatInputException) as excep:
        WayBackWebEntry(article_date=dto, url=faulty_url)
    assert f"The URL {faulty_url} is in the wrong format. Must be one of http[s]://sub.example.com" == str(excep.value)


def test_date_to_wbtimestamp():
    dto = datetime.strptime(datestring, "%d/%m/%Y")
    test_obj = WayBackWebEntry(url=good_http_url, article_date=dto)
    assert test_obj.date_as_wb_timestamp == "20190712"

    # We should be able to change the date.
    test_obj.request_date = datetime.strptime(other_datestring, "%d/%m/%Y")
    assert test_obj.date_as_wb_timestamp == "20191207"


def test_get_snapshots_from_wayback():
    dto = datetime.strptime(datestring, "%d/%m/%Y")
    test_obj = WayBackWebEntry(url=existing_archive_link, article_date=dto)
    assert "closest" in test_obj.snapshots


def test_get_snapshots_inexistant_from_wayback():
    dto = datetime.strptime(datestring, "%d/%m/%Y")
    test_obj = WayBackWebEntry(url=inexistant_archive_link, article_date=dto)
    assert len(test_obj.snapshots) == 0
    assert type(test_obj.snapshots) == dict


def test_has_snapshots_prop():
    dto = datetime.strptime(datestring, "%d/%m/%Y")
    test_obj = WayBackWebEntry(url=inexistant_archive_link, article_date=dto)
    assert test_obj.has_snapshots is False
    test_obj = WayBackWebEntry(url=existing_archive_link, article_date=dto)
    assert test_obj.has_snapshots is True


def test_get_snapshot_url_prop():
    dto = datetime.strptime(datestring, "%d/%m/%Y")
    test_obj = WayBackWebEntry(url=inexistant_archive_link, article_date=dto)
    with pytest.raises(NoWaybackSnapShotsError) as excep:
        no_url = test_obj.get_snapshot_url
    assert "You asked something that relies on existing snapshots but none were found!" == str(excep.value)

    test_obj = WayBackWebEntry(url=existing_archive_link, article_date=dto)
    assert test_obj.get_snapshot_url == expected_urlprop_example
