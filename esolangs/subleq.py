import sys

def to_byte(x:int):
    while x > 0xFF:
        x -= 0x100
    while x < 0x00:
        x += 0x100
    return x

def main():
    if len(sys.argv) > 1 and sys.argv[1].endswith('.bin'):
        print()
        memory = []
        buffer = []
        addr = 0x00
        with open(sys.argv[1], 'rb') as f:
            b = f.read(0x100)
            memory = bytearray(b)
        while addr < 0xFF:
            a = memory[addr]
            addr += 1
            b = memory[addr]
            addr += 1
            if addr < 0xFE:
                c = memory[addr]
            else:
                c = 0x00
            addr += 1
            if a == 0xFD:
                if len(buffer) == 0:
                    [buffer.append(to_byte(ord(i))) for i in list(input())]
                    buffer.append(0x00)
                memory[a] = buffer.pop(0)
            memory[b] = to_byte(memory[b] - memory[a])
            if a == 0xFD:
                memory[a] = 0x00
            if b == 0xFE:
                print(chr(memory[b]), end='')
                memory[b] = 0x00
            if memory[b] > 0x7F or memory[b] == 0x00:
                addr = c
            memory[0xFF] = 0x00
        print()
        sys.exit(0)
    print('Booting error: no binary file\nCan\'t find .bin file!')
    sys.exit(-1)

if __name__ == '__main__':
    main()
