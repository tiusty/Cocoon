# Third Party modules
from datetime import date, timedelta, datetime
import holidays
from dateutil import tz

# Cocoon Modules
from .constants import COMMUTE_TIME_WITHOUT_TRAFFIC, COMMUTE_TIME_WITH_TRAFFIC


def compute_departure_time_with_traffic():
    """
    Computes the departure time with traffic. Takes the desired date and adds the time
        that is used that has traffic
    :return: (int) -> The unix timestamp for the departure time
    """
    d = compute_departure_time_base_date()
    nyc = tz.gettz('America/New_York')
    return datetime.combine(d, COMMUTE_TIME_WITH_TRAFFIC).replace(tzinfo=nyc).timestamp()


def compute_departure_time_without_traffic():
    """
    Computes the departure time with out traffic. Takes the desired date and adds the time
        that is used that has traffic
    :return: (int) -> The unix timestamp for the departure time
    """
    d = compute_departure_time_base_date()
    nyc = tz.gettz('America/New_York')
    return datetime.combine(d, COMMUTE_TIME_WITHOUT_TRAFFIC).replace(tzinfo=nyc).timestamp()


def compute_departure_time_base_date():
    """
    Computes the date that should be used for computing the distance matrix. This
        function makes sures that the date is not a holiday
    :return: (datetime.date) -> The date that is used for the traffic estimation
    """
    # Retrieves the next Wednesday
    d = date.today() + timedelta(weeks=1, days=-date.today().weekday()+2)
    # Keeps adding weeks until a Wednesday that is not a holiday is found
    while d in holidays.US():
        d = d + timedelta(weeks=1)
    return d
