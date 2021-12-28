#VVVTTTL(11 or 15 bits)(sub packets)
#T4 (100)= literal, bin number of 1 (continue) or 0 (end) + 4 bits
#L length type ID 0 - 15 bits indicating length of subpackets, 1 - 11 bits number of subpackets

hex2bin = {hex(i)[2].upper():bin(i)[2:].rjust(4,"0") for i in range(16)}
def convert_hex(hex_string):
    return "".join([hex2bin[x] for x in hex_string])

with open("day16_input.txt") as file:
    mcode = convert_hex(file.readline()[:-1])

#print(mcode)

version_total = 0

def process(mcode, pointer):
    #Given an mcode location and a pointer value
    packet_version = int(mcode[pointer:pointer+3], 2)
    pointer += 3
    global version_total 
    version_total += packet_version
    packet_type = int(mcode[pointer:pointer+3], 2)
    pointer += 3
    #print("packet_start", pointer-6, "version", packet_version, "type", packet_type)
    if packet_type == 4:
        #Literal
        literal_bin = ""
        while True:
            indicator = int(mcode[pointer], 2)
            pointer += 1
            literal_bin += mcode[pointer:pointer+4]
            pointer += 4
            if indicator == 0:
                break
        literal = int(literal_bin, 2)
        #print("literal", literal)
        return pointer, literal
    else: #operator packet
        #Subpackets
        subpacket_values = []
        indicator = int(mcode[pointer],2)
        pointer += 1
        if indicator == 0:
            #15 bits indicating length of subpackets
            len_subpackets = int(mcode[pointer:pointer+15], 2)
            pointer += 15
            end_pointer = pointer + len_subpackets
            while pointer < end_pointer:
                pointer, v = process(mcode, pointer)
                subpacket_values.append(v)
        else: #indicator == 1
            #11 bits indicating number of subpackets
            num_subpackets = int(mcode[pointer:pointer+11], 2)
            pointer += 11
            for _ in range(num_subpackets):
                pointer, v = process(mcode, pointer)
                subpacket_values.append(v)
        #Process the operator aganist the subpacket values
        if packet_type == 0:
            #sum packets
            packet_value = sum(subpacket_values)
        elif packet_type == 1:
            #product packets
            packet_value = 1
            for v in subpacket_values:
                packet_value = packet_value * v
        elif packet_type == 2:
            #minimum
            packet_value = min(subpacket_values)
        elif packet_type == 3:
            #maximum
            packet_value = max(subpacket_values)
        elif packet_type == 5:
            #greater than
            if subpacket_values[0] > subpacket_values[1]:
                packet_value = 1
            else:
                packet_value = 0
        elif packet_type == 6:
            #less than
            if subpacket_values[0] < subpacket_values[1]:
                packet_value = 1
            else: 
                packet_value = 0
        elif packet_type == 7:
            #equal to
            if subpacket_values[0] == subpacket_values[1]:
                packet_value = 1
            else:
                packet_value = 0
        else:
            raise Exception("unrecognized type")
        #Return the pointer and the value
        return pointer, packet_value


p, v = process(mcode, 0)
print("part1",version_total)
print("part2", v)