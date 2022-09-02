#!/bin/env python3
import os
import json
import time
import importlib
import schedule
from typing import Dict

from .config import config
from .report import report
from .log import logger


def collect() -> Dict:
    # 收集指标模块
    mods = os.listdir(
        os.path.join(os.path.dirname(__file__), 'quotas')
    )
    mods = [ # 剔除 __pycache__ 与 __init__
        mod.removesuffix('.py') for mod in mods if not mod.startswith('_')
    ]
    mods = [ # 检查哪个开启
        mod for mod in mods if config['quotas']['enable'].get(mod)
    ]

    data = {}
    for name in mods:
        data[name] = {}
        mod = importlib.import_module(f'watchman.quotas.{name}')

        for attr in mod.__all__:
            collector = getattr(mod, attr)
            data[name][f'{collector.__name__}'] = collector()
    
    return data


def check_warnings(stat, cmp=None, base='') -> Dict:
    if cmp is None:
        cmp: dict = config['threshold']

    warns = {}
    for key, val in stat.items():
        sub_cmp = cmp.get(str(key), None)
        if not sub_cmp:
            continue

        if isinstance(val, dict):
            warns.update(
                check_warnings(val, sub_cmp, f'{base}.{key}' if base else key)
            )
        else:
            if val > sub_cmp:
                warns[f'{base}.{key}'] = val

    return warns


def check():
    stat = collect()
    logger.bind(stat=True).trace(json.dumps(stat))

    warns = check_warnings(stat)
    if warns:
        msg = '\n'.join(
            f'{k}={v}' for k, v in warns.items()
        )
        logger.warning(msg.replace('\n', ' '))
        report(msg)


if __name__ == '__main__':
    logger.info('start')

    schedule.every(1).minute.do(check)
    logger.info('schedule loaded')

    while True:
        schedule.run_pending()
        time.sleep(60)
