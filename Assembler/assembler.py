import sys
import csv

# instruction sets grouped by the type
inst_data = {}

# arg types
argList = {'inp_file': '', 'out_file': ''}
# arg keywords
argKeys = {'-i': 'inp_file', '-o': 'out_file'}

# array to load the instructions
Instructions = []

def format(numOfDigits, num):
    return str(num).zfill(numOfDigits)

# instruction formatting structure
# loop through the instructions and do the nessary stuff
def formatInstructions(Instructions):
    for ins in Instructions:
        formatInstruction(ins)

# format the different types of instructions
def formatInstruction(ins):
    # final instruction
    finalIns = []
    tmp_split = ins.split()
    instruction_name = tmp_split.pop(0)
    finalIns.append(instruction_name.upper())
    # spliting by the ','
    for tmp in tmp_split:
        # splitting by comma
        tmp_split_2 = tmp.split(',')
        tmp_split_2 = list(filter(lambda a: a != '', tmp_split_2))

        # segmented list before putting together
        segmented_list = []

        for item in tmp_split_2:
            # removing letter x 
            item = item.replace('x', '')
            # identifyng the sections with brackets
            if '(' and ')' in item:
                # removing ) from the string
                item = item.replace(')', '')
                tmp_split_3 = item.split('(')
                segmented_list.extend(tmp_split_3)
            else:
                segmented_list.append(item)

        finalIns.extend(segmented_list)

    #print(instruction_name, finalIns)
    handleInstruction(finalIns)

# read the csv and create the instruction data dictionary
def read_csv():
    # reading the csv file
    with open('RV32IM.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            opcode = format(7, row[0])
            funct3 = format(3, row[1])
            funct7 = format(7, row[2])
            inst = row[3]
            _type = row[4]
            inst_data[inst] = {'opcode': opcode,
                               'funct3': funct3, 'funct7': funct7, 'type': _type}

# handling the separated instructions
def handleInstruction(separatedIns):
    Instruction = None
    space = ' ' # used to visualize the space in instruction in debug mode

    # handle R-Type instructions
    if(inst_data[separatedIns[0]]['type'] == "R-Type"):
        Instruction = inst_data[separatedIns[0]]['funct7'] + toBin(5, separatedIns[3]) + toBin(
            5, separatedIns[2]) + inst_data[separatedIns[0]]['funct3'] + toBin(5, separatedIns[1]) + inst_data[separatedIns[0]]['opcode']
        
    elif(inst_data[separatedIns[0]]['type'] == "I - Type "):
        Instruction = toBin(12, separatedIns[3]) + space + toBin(5, separatedIns[2]) + space + inst_data[separatedIns[0]]['funct3'] + space + toBin(5, separatedIns[1]) + space + inst_data[separatedIns[0]]['opcode']
        
        
    elif(inst_data[separatedIns[0]]['type'] == "S-Type"):
        # sw rs2:value, immediate, rs1:base
        immediate = toBin(12, separatedIns[2])[::-1]
        Instruction = immediate[5:] + space + toBin(5, separatedIns[1]) + space + toBin(5, separatedIns[3])+ space + inst_data[separatedIns[0]]['funct3']+ space + immediate[:5] + space + inst_data[separatedIns[0]]['opcode']
    
    elif(inst_data[separatedIns[0]]['type'] == "B-Type"):
        # beq rs1, rs2, label
        immediate = toBin(13, separatedIns[3])[::-1]
        Instruction = immediate[12]+ space + immediate[5:10] + space + toBin(5, separatedIns[2])+ space + toBin(5, separatedIns[1]) + space + inst_data[separatedIns[0]]['funct3'] + space + immediate[1:4] + space + immediate[11] + space + inst_data[separatedIns[0]]['opcode'] 
    
    elif(inst_data[separatedIns[0]]['type'] == "U -Type"):
        # lui rd, immediate
        immediate = toBin(32, separatedIns[2])[::-1]
        Instruction = immediate[12:31] + space + toBin(5, separatedIns[1]) + space + inst_data[separatedIns[0]]['opcode']

    elif(inst_data[separatedIns[0]]['type'] == "J-Type"):
        #jal rd, immediate
        immediate = toBin(21, separatedIns[2])[::-1]
        Instruction = immediate[20] + immediate[1:10]+ immediate[11] + immediate[12:19] + space + toBin(5, separatedIns[1]) + space + inst_data[separatedIns[0]]['opcode']
        

    print(separatedIns[0], Instruction)

# taking the file name if passed as an argument
def handleArgs():
    n = len(sys.argv)
    for i in range(1, n):
        if (sys.argv[i].strip() in argKeys):
            argList[argKeys[sys.argv[i]]] = sys.argv[i+1]


# opening the assemblyfile and reading through the file
def handleInpFile():
    if argList['inp_file'] == '':
        print('Input file not found')
        sys.exit(1)

    # opening the assembly file
    f = open(argList['inp_file'], "r")
    # loop through the file and handle the instrctions separately
    for ins in f:
        Instructions.append(ins)
        # handleInstruction(ins)

    # start the instruction formatting
    formatInstructions(Instructions)

# convert a given number to binary according to a given format
def toBin(numOfDigits, num):
    return format(numOfDigits, "{0:b}".format(int(num)))

# saving data to a .bin file
def saveToFile(line):
    file = argList['inp_file'].split('.')[0] + '.bin'
    if not (argList['out_file'] == ''):
        file = argList['out_file']
    # saving the new line to the output file
    f = open(file, "a")
    f.write("Now the file has more content!")
    f.close()


if __name__ == "__main__":
    #create the instruction disctionary
    read_csv()
    # handdle the argments
    handleArgs()
    # input file reding sequence
    handleInpFile()