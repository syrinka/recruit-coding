import psutil
import platform as platform_


__all__ = [
    'memory'
]


def platform(plt):
    return platform_.platform().startswith(plt)

# ----- #

def memory():
    data = psutil.virtual_memory()
    stat =  {
        'total': data.total,
        'used': data.used,
        'available': data.available,
        'free': data.free,
        'percent': data.percent
    }
    if platform('Linux'):
        stat.update({
            'active': data.active,
            'inactive': data.inactive,
            'buffers': data.buffers,
            'cached': data.cached,
        })
    return stat
