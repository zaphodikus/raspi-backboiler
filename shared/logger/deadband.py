# logger deadbanding class
#
from datetime import datetime, timedelta


class DeadbandBase(object):
    """
    Deadband base class
    """
    def __init__(self, interval, deadband):
        """
        Sets the following deadbands
        :param interval: the max elapsed timedelta  object or a string representation of one in HH:MM:SS format
        :param deadband: max deviation from last logged sample
        """
        self.value_delta = deadband
        if isinstance(interval, str):
            tm = datetime.strptime(interval, '%H:%M:%S')
            self.time_delta = timedelta(hours=tm.hour, minutes=tm.minute, seconds=tm.second)
        else:
            self.time_delta = interval
        self.last_value_logged = None
        self.last_time_logged = None

    def exceeded(self, new_time, new_value):
        """
        returns False if the last logged value is still inside the deadbands. Will always return True on the first call
        :param self:
        :param new_time:
        :param new_value:
        :return: bool
        """
        if self.last_value_logged is None or self.last_time_logged is None:
            log = True
        else:
            log = abs(new_value - self.last_value_logged) > self.value_delta
            if abs((new_time - self.last_time_logged).total_seconds() > self.time_delta.total_seconds()):
                log = True
        if log:
            self.last_value_logged = new_value
            self.last_time_logged = new_time
        return log
