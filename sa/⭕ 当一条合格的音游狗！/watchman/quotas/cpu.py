import psutil
import platform as platform_


__all__ = [
    'cpu_count',
    'cpu_times',
    'cpu_percent',
    'cpu_load',
]


def platform(plt):
    return platform_.platform().startswith(plt)

# ----- #
            
def cpu_count() -> int:
    return psutil.cpu_count(logical=False)


def cpu_times():
    data = psutil.cpu_times()
    stat = {
        'user': data.user,
        'sys': data.system,
        'idle': data.idle,
    }
    if platform('Linux'):
        stat.update({
        'iowait': data.iowait,
        'irq': data.irq,
        'softirq': data.softirq
    })
    return stat


def cpu_percent() -> float:
    return psutil.cpu_percent()


def cpu_load():
    data = psutil.getloadavg()
    return {
        1: data[0],
        5: data[1],
        15: data[2],
    }
