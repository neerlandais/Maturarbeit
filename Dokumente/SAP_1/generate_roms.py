header = "v3.0 hex words plain\n"

microcode = {
    "Increment PC" : 0,
    "Output PC" : 1,
    "Load PC" : 2,
    "Load MAR" : 3,
    "Load RAM" : 4,
    "Output RAM" : 5,
    "Load Instruction" : 6,
    "Output Instruction Argument" : 7,
    "Load A" : 8,
    "Output A" : 9,
    "Load B" : 10,
    "Load Out" : 11,
    "Subtract" : 12,
    "Output ALU" : 13,
    "Halt" : 14
}

NOP = 0b00101010100010 # = 0xAA2 = 0d2722

fetch = [["Fetch", 
         [["Output PC", "Load MAR"],
          ["Increment PC", "Output RAM", "Load Instruction"]], 
         None]]

instructions = [
    ["ADD", [["Output ALU", "Load A"]], 0],
    ["SUB", [["Subtract", "Output ALU", "Load A"]], 1],
    
    ["LDA_Immediate", [["Output Instruction Argument", "Load A"]], 2],
    ["LDB_Immediate", [["Output Instruction Argument", "Load B"]], 3],
     
    ["LDA_Absolute", [
     ["Output Instruction Argument", "Load MAR"],
     ["Output RAM", "Load A"]], 4],
     
    ["LDB_Absolute", [
     ["Output Instruction Argument", "Load MAR"],
     ["Output RAM", "Load B"]], 5],
     
    
    ["ADD_Immediate", [
     ["Output Instruction Argument", "Load B"],
     ["Output ALU", "Load A"]], 6],
     
    ["SUB_Immediate", [
     ["Output Instruction Argument", "Load B"],
     ["Subtract", "Output ALU", "Load A"]], 7],    
 
    ["ADD_Absolute", [
     ["Output Instruction Argument", "Load MAR"],
     ["Output RAM", "Load B"],
     ["Output ALU", "Load A"]], 8],
     
    ["SUB_Absolute", [
     ["Output Instruction Argument", "Load MAR"],
     ["Output RAM", "Load B"],
     ["Subtract", "Output ALU", "Load A"]], 9],
     
     
    ["OUT", [["Output A", "Load Out"]], 10],
      
    ["MAB", [["Output A", "Load B"]], 11],
    
    ["STA",  [
     ["Output Instruction Argument", "Load MAR"],
     ["Output A", "Load RAM"]], 12],    

    ["JMP", [["Output Instruction Argument", "Load PC"]], 14],

    ["HLT", [["Halt"]], 15]
]

def gen_mi(instructions):
    global NOP
    
    for instruction in instructions:
        for mi in enumerate(instruction[1]):
            flags = 0
            
            for mc in mi[1]:
                flags |= 2**microcode[mc]
            
            instruction[1][mi[0]] = flags
        if instruction[0] != "Fetch" and len(instruction[1]) < 3:
            instruction[1].append(NOP)    
        
    return instructions

def gen_address(instructions):
    global fetch
    
    rom = [0 for i in range(16)]
    address = len(fetch[0][1]) # Account for Fetch before all Instructions
    
    for i in enumerate(instructions):
        rom[i[1][2]] = address
        address += len(i[1][1])
        
    return rom

def gen_control(instructions):
    global fetch
    
    rom = fetch[0][1] [:] # copy fetch microinstructions
    
    for instruction in instructions:
        for mi in instruction[1]: # get microinstructions out of the arrays
            rom.append(mi)
        print(instruction[0])
    
    return rom


def write_to_file(name, byte_array):
    global header
    string = header + ''.join("{:04x} ".format(num) for num in byte_array)[:-1] # cursed
    print(string)
    
    with open(name, "w") as f:
        print(string, file=f)

instructions = gen_mi(instructions)
fetch = gen_mi(fetch)

address = gen_address(instructions)
control = gen_control(instructions)

write_to_file("address.bin", address)
write_to_file("control.bin", control)