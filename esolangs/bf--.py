import sys

def to_bits(x:int):
    out = []
    i = 1
    while i < 256:
        out.insert(0, 0 != x & i)
        i = i * 2
    return out

def from_bits(x:list[bool]):
    out = 0
    i = 2 ** len(x)
    for p in range(len(x)):
        i = i // 2
        if x[p]:
            out += i
    return out

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
    mem = [False for i in range(32)]
    ptr = 0
    buf = []
    cmd = 0
    loops = []
    skip = 0
    while cmd < len(code):
        if ptr >= 32:ptr = 0
        c = code[cmd]
        if c == '[':
            if not mem[ptr]:
                skip += 1
            else:
                loops.append(cmd-1)
        elif c == ']':
            if skip > 0:
                skip -= 1
            else:
                cmd = loops.pop(len(loops)-1)
        elif c == '.' and skip == 0:
            if not mem[ptr]:
                if len(buf) == 0:[buf.append(to_byte(ord(i))) for i in list(input())]
                if len(buf) > 0:b = to_bits(buf.pop(0))
                else:b = to_bits(0)
                for i in range(8):
                    mem[i] = b[i]
            else:
                out = from_bits([mem[i] for i in range(8)])
                print(chr(out), end='')
        elif c == '>' and skip == 0:ptr += 1
        elif c == '+' and skip == 0:mem[ptr] = not mem[ptr]
        cmd += 1

def main():
    code = ''
    if len(sys.argv) > 1:
        if not sys.argv[1].endswith('.bf'):
            print('File extension must be .bf')
            sys.exit(-1)
        with open(sys.argv[1], 'r') as file:
            while True:
                c = file.read(1)
                if not c:break
                if c in '+>[].':code += c
    else:
        while True:
            text = input('>>> ')
            if len(text) == 0:break
            for c in text:
                if c in '+>[].':code += c
    run(code)
    sys.exit(0)

if __name__ == '__main__':
    main()