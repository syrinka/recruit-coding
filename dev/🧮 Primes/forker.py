import os

# 数据对齐宽度
width = 3

def main():
    r, w = os.pipe()
    if os.fork():
        # 子
        os.close(w) # 关掉自己的 w，让父可写
        sub(r)
        
    else:
        # 父
        os.close(r) # 关掉自己的 r，让子可读
        for i in range(2, 100):
            os.write(w, str(i).rjust(width).encode())
        os.close(w)
        

def sub(ir):
    # 读第一个输入作为筛选基数
    base = os.read(ir, width).decode()
    if not base:
        # 不再有输入了，此为最后一个 fork，终止
        print('TheEnd')
        exit()

    base = int(base)
    print(base)
    
    r, w = os.pipe()
    if os.fork():
        # 子
        os.close(w)
        sub(r)

    else:
        # 父
        os.close(r)
        while True:
            next = os.read(ir, width).decode()
            if not next:
                # 不再有输入了，此为终止
                break
            if (int(next) % base != 0):
                # 此关通过，传向下一层
                os.write(w, next.rjust(width).encode())
        os.close(w)


if __name__ == '__main__':
    main()