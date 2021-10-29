import io
import os

psutil_exist = False
try:
    import psutil

    psutil_exist = True
except:
    pass


def is_raspberrypi():
    if os.name != 'posix':
        return False
    chips = ('BCM2708', 'BCM2709', 'BCM2711', 'BCM2835', 'BCM2836')
    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    _, value = line.strip().split(':', 1)
                    value = value.strip()
                    if value in chips:
                        return True
    except Exception:
        pass
    return False


class Stats(object):
    @staticmethod
    def get_cpu():
        if psutil_exist: # raspberry
            return psutil.cpu_percent()
        return 42

    @staticmethod
    def get_free_memory():
        if psutil_exist:
            memory = psutil.virtual_memory()
            return memory
        return 42

    @staticmethod
    def get_system():
        if is_raspberrypi():
            return "raspberrypi"
        return "not-raspberrypi"

    @staticmethod
    def get_disk_space():
        if psutil_exist:
            disk = psutil.disk_usage('/')
            return disk.free, disk.total
        return 42, 42

    @staticmethod
    def get_average_cpu():
        try:
            from gpiozero import LoadAverage
            ave = int(LoadAverage(minutes=1).load_average * 100)
            return ave
        except:
            pass
        return 42

if __name__ == "__main__":
    cpu = Stats.get_cpu()
    system = Stats.get_system()
    free, used = Stats.get_disk_space()
    memory = Stats.get_free_memory()
    print(cpu)
