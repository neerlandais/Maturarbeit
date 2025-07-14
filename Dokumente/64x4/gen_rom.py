signals = {'FF': 22, 'FI': 11, 'BI': 9, 'MTP': 17, 'MLI': 14, 'PLI': 19, 'BO': 6, 'MHI': 15, 'PHI': 20, 'MC': 16, 'EC': 2, 'SR': 23, 'II': 10, 'AI': 7, 'EO': 1, 'XE': 0, 'MZ': 18, 'ES': 3, 'AO': 4, 'XI': 8, 'PC': 21, 'XO': 5, 'RI': 13, 'RO': 12}

cword_len = len(signals)
steps = 16
flag_num = 2** 4

fetch_mi = ["RO","II","MC","PC"]

instructions = [
    ["NOP", None,   [["FF"],["FF"],["FF"],["FF"],["FF"],["FF"],["FF"],["FF"],["FF"],["FF"],["FF"],["FF"],["FF"],["FF"],["FF"]]],
    
    ["ADI", None,   [["RO","BI","PC","MC"],["EO","AI","FI","SR"]]],
    ["ADZ", None,   [["RO","MLI","MZ","MHI","PC"],["RO","BI"],["EO","AI","FI","MTP","MLI","MHI","SR"]]],
    ["ADB", None,   [["RO","BI","PC","MC"],["RO","MHI","PC"],["BO","MLI"],["RO","BI"],["EO","AI","FI","MTP","MLI","MHI","SR"]]],
    
    ["SUI", None,   [["RO","BI","PC","MC"],["EO","ES","EC","AI","FI","SR"]]],
    ["SUZ", None,   [["RO","MLI","MZ","MHI","PC"],["RO","BI"],["EO","ES","EC","AI","FI","MTP","MLI","MHI","SR"]]],
    ["SUB", None,   [["RO","BI","PC","MC"],["RO","MHI","PC"],["BO","MLI"],["RO","BI"],["EO","ES","EC","AI","FI","MTP","MLI","MHI","SR"]]],
    
    ["BNZ", None,   [["RO","PLI","MC"],["RO","PHI"],["FF","MTP","MLI","MHI","SR"]]],
    ["BNZ", 0b0010, [["FF","PC","MC","SR"]]]
]

rom = [0 for i in range(256*flag_num*steps)]

def gen_mi(mi):
    out = 0
    for signal in mi:
        out |= 2** signals[signal]
    return out

fetch = gen_mi(fetch_mi)

def generate_rom(IS, rom):
    opcode = 0
    last_name = IS[0][0]
    
    for I in IS:
        name = I[0]
        flag_reqs = I[1]
        mi = I[2]
        
        if last_name != name:
            last_name = name
            opcode += 1
        
        for f in range(flag_num):
            if flag_reqs == None or flag_reqs&f:
                rom[opcode*steps*flag_num + flag_num*f] = fetch
                
                for s in range(len(mi)):
                    rom[opcode*steps*flag_num + flag_num*f + s+1] = gen_mi(mi[s])
                    
                for s in range(len(mi), steps-1):
                    rom[opcode*steps*flag_num + flag_num*f + s+1] = 0
                    
def generate_file(name, rom):
    hex_string = ''.join("{:06x} ".format(num) for num in rom)[:-1] # cursed
    data = bytearray.fromhex(hex_string)
    
    with open(name, "bw") as f:
        f.write(data)

generate_rom(instructions, rom)
generate_file("control.bin", rom)