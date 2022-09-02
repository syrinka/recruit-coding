import time
import argparse
from Levenshtein import distance # pip install python-Levenshtein


msg = '''The lovers and the empress,
The lovers and temperance.
The chariot and the empress,
The chariot and the empress.
The chariot and justice!
The lovers and the hermit,
The emperor and the hanged man,
The empress and the fool.
The chariot and the lovers,
The empress and the empress. 
The chariot and the hermit,
The emperor and the devil.
The hierophant and the hierophant,
the chariot and death.'''


class SpeedTyper(object):
    def __init__(self, msg, opt):
        self.msg = msg
        self.opt = opt


    def segments(self):
        segs = []
        for i in self.msg.split('\n'):
            segs.append(i.strip())
        return segs


    def run(self):
        _green = '\033[32m'
        _yellow = '\033[93m'
        _gray = '\033[90m'
        _cyan = '\033[36m'
        _b = '\033[01m'
        _rst = '\033[00m'

        chars = 0
        mistake = 0
        lines = 0
        combo = 0
        start = time.time()
        for seg in self.segments():
            print(f'{_green}· {seg}{_rst}')
            typed = input('❯ ')

            if self.opt.case_insensitive:
                dist = distance(seg.lower(), typed.lower())
            else:
                dist = distance(seg, typed)
            
            now = time.time()
            lines += 1
            chars += len(seg)

            if dist == 0:
                combo += 1
                print(f'{_yellow}Perfect{_rst}', end='')
                
            else:
                combo = 0
                mistake += dist
                print(f'{_cyan}miss   {_rst}', end='')

            acc = (chars - mistake) / chars
            kps = chars / (now - start)

            print(f'{_gray}  {kps:.1f}kps  {acc:.2%}{_rst}')

        print('\n ====== \n')
        print(f'Elapsed Time: {_b}{now-start:.1f}s{_rst}')
        print(f'KPS: {_b}{kps:.1f}{_rst}')
        print(f'Accuracy: {_b}{acc:.2%}{_rst}')
        if combo == lines:
            print(f'\n{_b}{_cyan} - FULL  COMBO - {_rst}')
        else:
            print(f'\n{_b} - {combo}  COMBO - {_rst}')
        if mistake == 0:
            print(f'\n{_b}{_yellow} < ALL·PERFECT > {_rst}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SpeedTyper!!!')
    parser.add_argument(
        '-i', '--case-insensitive',
        default=False,
        required=False,
        action='store_true',
        help='对英文文段是否大小写敏感'
    )
    parser.add_argument(
        '-f', '--file',
        required=False,
        help='自定义测试文段'
    )
    args = parser.parse_args()

    if args.file:
        msg = open(args.file, encoding='utf-8').read()

    SpeedTyper(msg, args).run()
