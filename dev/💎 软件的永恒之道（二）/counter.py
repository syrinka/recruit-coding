from typing import List, Generic, TypeVar
from collections import deque
from threading import Thread, Lock


T = TypeVar('T')

class Pipe(Generic[T]):
    """生产者-消费者 模型中的管道部分"""

    # 毒丸
    STOP = StopIteration

    def __init__(self, size: int) -> None:
        self.pipe = deque()
        self.use = Lock() # 队列锁
        self.putable = size # 可存标记
        self.getable = 0 # 可取标记


    def put(self, item: T):
        """存"""
        self.putable -= 1
        with self.use:
            self.pipe.append(item)
            # print('put', item)
        self.getable += 1

        
    def get(self) -> T:
        """取"""
        self.getable -= 1
        with self.use:
            item = self.pipe.popleft()
            # print('get', item)
        self.putable += 1
        
        return item


class Producer(Thread):
    def __init__(self, pipe: Pipe, msg: str):
        super().__init__()
        self.pipe = pipe
        self.msg = msg

    def run(self):
        i = 0
        while i < len(self.msg):
            if self.pipe.putable:
                self.pipe.put(self.msg[i])
                i += 1
        self.pipe.put(self.pipe.STOP)


class Consumer(Thread):
    def __init__(self, pipe: Pipe):
        super().__init__()
        self.pipe = pipe
        self.counter = {}

    def run(self):
        while True:
            if self.pipe.getable:
                char = self.pipe.get()
                if char == self.pipe.STOP:
                    break
                try:
                    self.counter[char] += 1
                except:
                    self.counter[char] = 1


if __name__ == '__main__':
    msg = '''背景
建筑学是软件工程的源头之一。
在上世纪六十年代，软件的重要性日益突出，软件飞快地朝着大型化、复杂化演进，然而当时的开发方法却令开发举步维艰，是为“软件危机”。
在全球性“软件危机”肆虐的二三十年间，软件开发往往以失败告终：无效的计划、惨烈的质量、混乱的代码，乃至程序本身根本无法运行，最为严重的事件 曾造成多人伤亡。
在这种背景之下，软件工程应运而生。它旨在总结一套行之有效的方法论，设计技术、管理等多个层次，为软件的开发提供指引。发展至今日，软件工程已足以指导诸如大型操作系统、大规模分布式运算之类的应用。
软件工程的使命是要指导开发软件，这一人类历史上从未有之事物，因此软件工程从众多学科汲取了理论，其中建筑学对软件工程的基础之一——设计模式，有着直接的启发。
美国著名的建筑学家 C. 亚历山大在其系列书籍“建筑的永恒之道”中，认为古往今来所有经典的建筑都有其蕴含的模式，若将其加以提炼、组合，结合环境付诸实施，便能够造出一样美妙的建筑。他的理论直接导致了软件工程中设计模式的诞生，因此亚历山大也被称为“设计模式之父”。
'''

    # 因为用毒丸作为停止信号所以消费者必须和生产者一样多（
    # 不管了
    pipe: Pipe[str] = Pipe(20)
    jobs: List[Thread] = [
        Consumer(pipe),
        Producer(pipe, msg),
    ]

    for job in jobs:
        job.start()
    for job in jobs:
        job.join()

    # 获得消费者里的 counter
    print(jobs[0].counter)
