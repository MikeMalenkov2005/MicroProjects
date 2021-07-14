import sys

def to_byte(x:int):
    while x > 0xFF:
        x -= 0x100
    while x < 0x00:
        x += 0x100
    return x

def run(code:str):
    if len(code) <= 0:
        print('No code error!')
        sys.exit(-1)
    mem:list[int] = [0]
    buf = []
    ptr = 0
    cmd = 0
    loops = []
    skip = 0
    while cmd < len(code):
        if ptr < 0:
            ptr = 0
            mem.insert(0, 0)
        elif ptr >= len(mem):
            ptr = len(mem)
            mem.append(0)
        c = code[cmd]
        if c == '[':
            if mem[ptr] == 0:
                skip += 1
            else:
                loops.append(cmd-1)
        elif c == ']':
            if skip > 0:
                skip -= 1
            else:
                cmd = loops.pop(len(loops)-1)
        elif c == '<' and skip == 0:
            ptr -= 1
        elif c == '>' and skip == 0:
            ptr += 1
        elif c == '-' and skip == 0:
            mem[ptr] = to_byte(mem[ptr] - 1)
        elif c == '+' and skip == 0:
            mem[ptr] = to_byte(mem[ptr] + 1)
        elif c == ',' and skip == 0:
            if len(buf) == 0:
                [buf.append(to_byte(ord(i))) for i in list(input())]
                buf.append(0x00)
            if len(buf) > 0:
                mem[ptr] = buf.pop(0)
        elif c == '.' and skip == 0:
            print(chr(mem[ptr]), end='')
        cmd += 1

def main():
    code = ''
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            while True:
                c = file.read(1)
                if not c:break
                if c in '+-<>[],.':code += c
    while True:
        text = input('>>> ')
        if len(text) == 0:break
        for c in text:
            if c in '+-<>[],.':code += c
    run(code)
    sys.exit(0)

if __name__ == '__main__':
    main()