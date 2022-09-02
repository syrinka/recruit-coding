import psutil
import platform as platform_


__all__ = [
    'diskinfo'
]


def platform(plt):
    return platform_.platform().startswith(plt)

# ----- #

def diskinfo():
    data = psutil.disk_partitions()
    stat = {}
    for part in data:
        usage = psutil.disk_usage(part.mountpoint)
        stat[part.device] = {
            'dev': part.device,
            'mountpoint': part.mountpoint,
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent,
        }
    return stat
