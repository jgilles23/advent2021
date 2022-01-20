from collections import OrderedDict

with open("day24_input.txt") as file:
    instructions = [line[:-1].split(" ") for line in file]
# print(instructions)

# state = {"w":{0:set()}, "x":{0:set()}, "y":{0:set()}, "z":{0:set()}}
# inputs = [x for x in "abcdefghijklmnopqrst"]


# #dict {currentValue:(input number, starting value)}

# def cross_combine(A,B,func):
#     #Cross combine dics via the provided function
#     res = {}
#     for a in A:
#         for b in B:
#             c = func(a,b)
#             if c is None:
#                 continue
#             if c in res:
#                 res[c].update(A[a])
#                 res[c].update(B[b])
#             else:
#                 res[c] = A[a]
#                 res[c].update(B[b])
#             if len(res[c]) >= 9:
#                 res[c] = {0,}
#     return res

# def lambda_divide(x,y): #Division rounding is not working correctly here FLAG FLAG FLAG
#     if y == 0: 
#         return None
#     return x//y

# def lambda_mod(x,y):
#     if y == 0:
#         return None
#     return x%y

# def lambda_equal(x,y):
#     if x == y:
#         return 1
#     return 0

# def find_best(input_of_interest):
#     input_count = -1
#     for i, instruction in enumerate(instructions[:]):
#         cmd = instruction[0]
#         print(i, instruction)
#         var0 = instruction[1]
#         val0 = state[var0]
#         if len(instruction) <= 2:
#             val1 = None
#         else:
#             try:
#                 val1 = {int(instruction[2]):{}}
#             except:
#                 val1 = state[instruction[2]]
#         #Iterate through the instructions
#         if cmd == "inp":
#             input_count += 1
#             if input_count == input_of_interest:
#                 res = {i:{i,} for i in range(1,10)}
#             else:
#                 res = {i:set() for i in range(1,10)}
#         elif cmd == "add":
#             res = cross_combine(val0, val1, lambda x,y: x+y)
#         elif cmd == "mul":
#             res = cross_combine(val0, val1, lambda x,y: x*y)
#         elif cmd == "div":
#             res = cross_combine(val0, val1, lambda_divide)
#         elif cmd == "mod":
#             res = cross_combine(val0, val1, lambda_mod)
#         elif cmd == "eql":
#             res = cross_combine(val0, val1, lambda_equal)
#         state[var0] = res
#     return state["z"][0]

# q = find_best(1)
# print(q)

def join_command(val0, type0, val1, type1, character):
    if type1 == "integer" or len(val1)<=1:
        return str(val0) + character + str(val1)
    else:
        if len(str(val0)) > 2:
            val0 = "(" + str(val0) + ")"
        if len(str(val1)) > 2:
            val1 = "(" + str(val1) +")"
        return str(val0) + character + str(val1)



#B = a+b+c+d+15%26-7
#((((A*26)+(c+10)*26)+(d+2)/26)*(25*(B=e=0)+1))+((e+15)*(B=e=0))%26+10=f

def run_on(inputs, subs, instructions, verbose=True):
    state = OrderedDict({"w":0, "x":0, "y":0, "z":0})
    count = 0
    for instruction in instructions:
        cmd = instruction[0]
        var0 = instruction[1]
        val0 = state[var0]
        if isinstance(val0, str):
            type0 = "string"
        else:
            type0 = "integer"
        if len(instruction) <= 2:
            val1 = None
            type1 = None
        else:
            try:
                val1 = int(instruction[2])
                type1 = "integer"
            except:
                var1 = instruction[2]
                val1 = state[var1]
                if isinstance(val1, str):
                    type1 = "string"
                    if len(val1) > 8:
                        count += 1
                        moniker = "_" +str(count)
                        state[moniker] = state[var1]
                        state[var1] = moniker
                        val1 = moniker
                else:
                    type1 = "integer"
        #Parse the input
        if cmd == "inp":
            res = inputs.pop(0)
        elif cmd == "add":
            if type0 == "integer" and type1 == "integer":
                res = val0 + val1
            elif val0 == 0:
                res = val1
            elif val1 == 0:
                res = val0
            else:
                res = join_command(val0, type0, val1, type1, "+")
        elif cmd == "mul":
            if type0 == "integer" and type1 == "integer":
                res = val0 * val1
            elif val0 == 0 or val1 == 0:
                res = 0
            elif val0 == 1:
                res = val1
            elif val1 == 1:
                res = val0
            else:
                res = join_command(val0, type0, val1, type1, "*")
        elif cmd == "div":
            if val1 == 0:
                raise Exception("Divide by 0")
            elif type0 == "integer" and type1 == "integer":
                if val0//val1 >= 0:
                    res = val0 // val1
                else:
                    res = -1*val0//val1*-1
            elif val0 == 0:
                res = 0
            elif val1 == 1:
                res = val0
            else:
                res = join_command(val0, type0, val1, type1, "/")
        elif cmd == "mod":
            if val1 == 0:
                raise Exception("Modulus by 0")
            elif type0 == "integer" and type1 == "integer":
                res = val0 % val1
            elif val1 == 1:
                res = val0
            else:
                res = join_command(val0, type0, val1, type1, "%")
        elif cmd == "eql":
            if type0 == "integer" and type1 == "integer":
                if val0 == val1:
                    res = 1
                else:
                    res = 0
            elif type0 == "string" and len(val0) == 1 and type1 == "integer":
                if val1 > 9:
                    res = 0
            elif type0 == "integer" and type1 == "string" and len(val1) == 1:
                if val0 > 9:
                    res = 0
            else:
                res = join_command(val0, type0, val1, type1, "=")
        state[var0] = res
        #Check substitutions
        for k in state:
            for sub in subs:
                if sub[0] == "=":
                    if sub in str(state[k]):
                        state[k] = subs[sub]
                if sub in str(state[k]):
                    if isinstance(subs[sub], int) and len(sub)==len(state[k]):
                        state[k] = subs[sub]
                    else:
                        i = state[k].find(sub)
                        state[k] = state[k][:i] + str(subs[sub]) + state[k][i+len(sub):]
    if verbose:
        print()
        for k in state:
            print(k, ":", state[k])
    return state

def get_num(string):
    i = 0
    num = ""
    while i < len(string) and string[i] in "-0123456789":
        num += string[i]
        i += 1
    num = int(num)
    # print("get_num", string, "num", num, "i", i)
    return num, i

def get_value(inputs_dict, state, string):
    # print("get_value", string)
    if string[0] == "(":
        a, i = run_on_special(inputs_dict, state, string=string[1:])
        i += 1
    elif string[0] == "_":
        sub_var, i = get_num(string[1:])
        sub_var = "_" + str(sub_var)
        i += 1
        a, _ = run_on_special(inputs_dict, state, string=state[sub_var])
        state[sub_var] = a 
    elif string[0] in "-0123456789":
        a, i = get_num(string)
    else:
        a,_ = run_on_special(inputs_dict, state, inputs_dict[string[0]])
        state[string[0]] = a
        i = 1
    return a, i

def run_on_special(inputs_dict, state, string):
    if isinstance(string, int):
        return string, len(str(string))
    if string is None:
        for c in "wxyz":
             a, _= run_on_special(inputs_dict, state, state[c])
             state[c] = a
        return state
    string = str(string)
    #Interate through the string
    a, i = get_value(inputs_dict, state, string)
    while i < len(string):
        # print("i", i)
        #Return if bracket is closed
        if string[i] == ")":
            return a, i+1
        #Get the operand
        operand = string[i]
        i += 1
        #Get the next number, repeat until end of string
        b, j = get_value(inputs_dict, state, string[i:])
        # print("j", j)
        i += j
        #Perform the operation
        if operand == "+":
            a += b
        elif operand == "*":
            a = a*b
        elif operand == "/":
            if a//b < 0:
                a = -1*a//b*-1
            else:
                a = a//b
        elif operand == "%":
            a = a%b
        elif operand == "=":
            if a == b:
                a = 1
            else:
                a=0
        else:
            raise Exception("Unrecognized operand: " + str(operand))
    if string is None:
        return state
    else:
        return a, i

#_44 ~e = not d=e+5
#_3 E : (((a+6*26)+(b+7)*26)+(c+10)*26)+(d+2) = E
#   try as small as possible a,b,c,d=1 : (((1+6*26)+(1+7)*26)+(1+10)*26)+(1+2) : 128729
#   (((7*26)+(8)*26)+(11)*26)+(3) = 128729
#_8 H = ((((E/26)*(25*~e+1))+((e+15)*~e)*26)+(f+8)*26)+(g+1)
#   try as small as possible abcdefg=1 : ((((E/26)*(25*~e+1))+((e+15)*~e)*26)+(f+8)*26)+(g+1)
#   ~e = 0
#       (4951*26)+(9*26)+2 = 3347112 MIN H
#   ~e = 1
#       (((4951/26)*26)+(16)*26)+(1+8)*26)+(1+1) = 3350490
#_9 ~h = ((((E/26)*(25*~e+1))+((e+15)*~e)*26)+(f+8)*26)+(g+1)%26+-5=h=0
#   not g=h+4
#_12 J : (((H/26)*(25*~h+1))+((h+10)*~h)*26)+(i+5)
#   try for min : ~h=0 : (((3347112/26)*(25*0+1))+((1+10)*0)*26)+(1+5) : 3347116
#_13 ~j : not i+2=j
#_16 K : ((J/26)*(25*(~j)+1))+((j+3)*(~j))
#   try for min : ~j=0 : ((3347116/26)*(25*(0)+1))+((1+3)*(0)) : 128735
#_17 ~k : ((J/26)*(25*(~j)+1))+((j+3)*(~j))%26=k=0
#   try ~j=0 : J/26%26=k=0
#   try ~j=1 : not j+3=k
#_20 L : ((K/26)*(25*(~k)+1))+((k+5)*(~k))
#   try for min : ((128735/26)*(25*(0)+1))+((1+5)*(0)) : 4951
#_21 ~l : ((K/26)*(25*(~k)+1))+((k+5)*(~k))%26+-5=l=0
#   try ~k=0 : K/26%26+-5=l=0
#   try ~k=1 : not k=l
#_24 M : ((L/26)*(25*(~l)+1))+((l+11)*(~l))
#   try for min : ((4951/26)*(25*(0)+1))+((1+11)*(0)) : 190
#_25 ~m : ((L/26)*(25*(~l)+1))+((l+11)*(~l))%26+-9=m=0
#   try ~l=0 : L/26%26+-9=m=0
#   try ~l=1 : not l+2=m
#_28 N : ((M/26)*(25*(~m)+1))+((m+12)*(~m))
#   try for min : ((190/26)*(25*(0)+1))+((1+12)*(0)) : 7
#_29 ~n : ((M/26)*(25*(~m)+1))+((m+12)*(~m))%26=n=0
#   try ~m=0 : M/26%26=n=0
#   try ~m=1 : m+12%26=n=0
#z : ((N/26)*(25*(~n)+1))+((n+10)*(~n))
#   try ~n=0 : N/26=0
#   try ~n=1 : (N/26*26)+n+10=0 -< This will never be 0; therefore ~n must be 0 AND N/26 = 0
#
#N/26=0

def process(equn, style, X):
    if style == "up":
        z = "9"
        y = "1"
    else:
        z = "1"
        y = "0"
    q = [z if x in "abcdefghijklmn" else x for x in equn]
    q = [str(X) if x in "ABCDEFGHIJKLMN" else x for x in q]
    q = "".join(q)
    while "~" in q:
        i = q.find("~")
        q = q[:i] + y + q[i+2:]
    return q

equn = process("((((E/26)*(25*~e+1))+((e+15)*~e)*26)+(f+8)*26)+(g+1)", "down", 128729)

#_3 E : (((a+6*26)+(b+7)*26)+(c+10)*26)+(d+2) : 128729, 274961
#_8 H : ((((E/26)*(25*~e+1))+((e+15)*~e)*26)+(f+8)*26)+(g+1) : 3347112, 3403089908
#_12 J : (((H/26)*(25*~h+1))+((h+10)*~h)*26)+(i+5) : 3347116, 1619870800848
#_16 K : ((J/26)*(25*(~j)+1))+((j+3)*(~j)) : 128735, 29656096200112
#_20 L : ((K/26)*(25*(~k)+1))+((k+5)*(~k)) : 4951, 
#_24 M : ((L/26)*(25*(~l)+1))+((l+11)*(~l)) : 190, 
#_28 N : ((M/26)*(25*(~m)+1))+((m+12)*(~m)) : 7, 
#z : ((N/26)*(25*(~n)+1))+((n+10)*(~n)) ; 0, 

bigs = {
    "E":"(((a+6*26)+(b+7)*26)+(c+10)*26)+(d+2)",
    "H":"((((E/26)*(25*~e+1))+((e+15)*~e)*26)+(f+8)*26)+(g+1)",
    }

#_4 : (a+b+c+d+25)%26+-7=e=0
#e, h, j, k, l, m, n : relevant comparisons

#z : ((_28/26)*(_30))+(_31)
#   ~n can be 0 or 1, either way _28/26 = 0
#   _31=0 : _29=0 : n comparison : ~n=0
#   AND
#   (_28/26)=0 : _28<26 : ((_24/26)*(_26))+(_27) < 26
#   or
#   _30=0 <- never 0
#
#((_24/26)*(25*~m+1))+(m+12*~m) < 26
#   ((_20/26)*(_22))+(_23)%26+-9=m=0
#   ~m is 0
#       _24 < 26*26
#   ~m is 1
#       (_24/26*26)+m < 14 : _24 < 26
#_24 = ((_20/26)*(25*(~l)+1))+((l+11)*(~l)) < 26 or 26*26 depending on ~m
#   let _24%26=0 : ((_20/26)*(25*(~l)+1))+((l+11)*(~l))%26 = 0 
#       ~l = 0 : (_20/26)%26 = 0 : 0<=_20<0+26 or 26*26<=_20<26*26+26 or v*26*26<=_20<v*26*26+26 for v in (0,1,2,3,...)
#       ~l = 1 : _20/26+l+11%26 = 0 
#   ~l is 0
#       _20 < 26^2 or 26^3 based on ~m&~l
#   ~l is 1
#       (_20/26*26)+l < 15 or 26^2-11 : _20/26 < 0.9 or 25.1
#       _20 < 26 or _20 < 25*26 based on ~m&~l
#   let X be the value that _20 must be less than based on ~m ~l
#_20 = ((_16/26)*(25*(~k)+1))+((k+5)*(~k)) < X
#   _16%26=k




subs = OrderedDict([
    ("a+6%26+15=b", 0),
    ("_1%26+15=c", 0),
    ("_2%26+11=d", 0),
    ("_6%26+10=f", 0),
    ("_7%26+10=g", 0),
    ("_11%26+15=i", 0),
    #Comparison checks
    # ("_28", 9),
    # ("_28", 144),
])

N = None
#Find the reduced state
inputs = [x for x in "abcdefghijklmnopqrst"]
reduced_state = run_on(inputs, subs, instructions[:N])

def test_reduced_state(reduced_state):
    inputs_saved = [9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    #Run the real code to get the actual answer
    real_answer = run_on([x for x in inputs_saved], {}, instructions[:N], verbose=False)
    #Run the reuduced code to see if the same answer is given
    inputs = {"abcdefghijklmnopqrst"[i]:inputs_saved[i] for i in range(len(inputs_saved))}
    new_answer = run_on_special(inputs, {k:v for k,v in reduced_state.items()}, string=None)
    #Print some testing data
    print()
    print("TEST RESULTS")
    error_found = False
    for k in "wxyz":
        if real_answer[k] == new_answer[k]:
            print(k, ":", real_answer[k])
        else:
            print(k, ":", real_answer[k], "ERROR", new_answer[k])
            error_found = True
    if error_found:
        for k in real_answer:
            if k in "wxyz":
                continue
            if real_answer[k] == new_answer[k]:
                print(k, ":", real_answer[k])
            else:
                print(k, ":", real_answer[k], "ERROR", new_answer[k])
    # print(real_answer)
    # print(new_answer)



test_reduced_state(reduced_state)

print("Run equation: ", equn, "RESULT", run_on_special({}, {}, equn))