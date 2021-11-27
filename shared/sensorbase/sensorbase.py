#

class RawSensor(object):
    def __init__(self, address):
        self.address = address
        self.last_known_value = None

    def get_address(self):
        return self.address

    def get_sensor_value(self):
        raise Exception("NotImplementedError")

    @staticmethod
    def get_sensor_units():
        raise Exception("NotImplementedError")


# class NoisySensor(object):
#     """
#     Helper which holds a last known good value which is substituted if a sensor read fails once
#     """
#     def __init__(self):
#         self._last_known_value = None
#
#     def __setattr__(self, key, value):
#         if key == 'last_known_value':
#             if NoisySensor._is_valid(value):
#                 self._last_known_value = value
#             else:
#                 print(f"Bad sensor value {value} for {self.get_address()}, ignored")
#         else:
#             super(NoisySensor, self).__setattr__(key, value)
#
#     def __getattr__(self, item):
#         if item == 'last_known_value':
#             if self._last_known_value is None:
#                 print(f"Sensor {self.get_address()} is offline")
#             value = self._last_known_value
#             self._last_known_value = None
#             return value
#         else:
#             try:
#                 return super(NoisySensor, self).__getattr__(item)
#             except Exception as e:
#                 print(f"ERROR READING FROM {self.device_path} !!!")
#                 #print(f"{e} while accessing property/method {item} of {self.__class__}")
#                 raise e
#
#     @staticmethod
#     def _is_valid(value):
#         if value == 0 or value is None:
#             return False
#         return True


class TempSensor(RawSensor):
    def __init__(self, address):
        super().__init__(address)

    @staticmethod
    def get_sensor_units():
        return r"°C"
