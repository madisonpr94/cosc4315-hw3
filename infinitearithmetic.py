import re, sys, math

def StrToInfInt(s, n):
    if(len(s) <= n):
        return [int(s)]
    else:
        si = int(s[-n:])
        t = StrToInfInt(s[:-n], n)
        t.append(si)
        return t
		

def InfIntToStr(s, i, n):
    if i == len(s):
        return ""
    elif i == 0:
        result = str(s[i]) + InfIntToStr(s, i + 1, n)
    else:
        result = str(s[i]).zfill(n) + InfIntToStr(s, i + 1, n)
    return result
	
	
def AddInfInt(a, b, c, n):
    if a == b == []:
        if c != 0:
            return [c]
        else:
            return
    if len(a) > 0:
        ai = a[-1]
    else:
        ai = 0
    if len(b) > 0:
        bi = b[-1]
    else:
        bi = 0
    sum = c + ai + bi
    if sum >= 10 ** n:
        sum -= 10 ** n
        carry = 1
    else:
        carry = 0
    a = a[:-1]
    b = b[:-1]
    result = AddInfInt(a, b, carry, n) or []
    result += [sum]
    return result
	
	
def MultiplyAcross(a, b, i, n):
    if i == len(a):
        return [0]
    else:
        pnext = MultiplyAcross(a, b, i + 1, n)
        product = b * a[i]
        carry = 0
        if product >= 10 ** n:
            carry = math.floor(product / 10 ** n)
            product = product % (10 ** n)
        product = [product] + [0] * (len(a) - i - 1)
        if carry > 0:
            product = [carry] + product
    return AddInfInt(product, pnext, 0, n)
    
def MultiplyInfInt(a, b, i, n):
    if i == len(b):
        return [0]
    else:
        resultnext = MultiplyInfInt(a, b, i + 1, n)
        result = MultiplyAcross(a, b[i], 0, n)
        result = result + [0] * (len(b) - i - 1)
        return AddInfInt(result, resultnext, 0, n)	

	
def SolveLine(s, n):
    find = re.search('((add|multiply)\(\d+,\d+\))', s)
    if not find:
        return [-1]
    else:
        if find.group(1) == s:
            si = s.split('(')
            numResults = re.match("([0-9]+),([0-9]+)", si[1])
            nums = [StrToInfInt(numResults.group(1), n), StrToInfInt(numResults.group(2), n)]
            if si[0] == "add":
                x = AddInfInt(nums[0], nums[1], 0, n)
            elif si[0] == "multiply":
                x = MultiplyInfInt(nums[0], nums[1], 0, n)
            return x
        else:
            s1 = s[find.start(1):find.end(1)]
            x = SolveLine(s1, n)
            s = s.replace(s1, InfIntToStr(x, 0, n))
            return SolveLine(s, n)
			
	
def SolveInput(s, n):
    if len(s) == 0:
        return
    result = SolveLine(s[0], n)
    if result != [-1]:
        print(s[0], "=", InfIntToStr(result, 0, n))
    else:
        print("Invalid expression: ", s[0])
    SolveInput(s[1:], n)
	

if len(sys.argv) < 2:
    print("Usage: 'python3 infinitearithmetic.py \"input=<file name>;digitsPerNode=<number>\"")

else:
    args = re.match("input=(.*);digitsPerNode=(\d+)", sys.argv[1])
	
    inputFilename = args.group(1)
    digitsPerNode = int(args.group(2))

    infile = open(inputFilename, 'r')
    lines = infile.read().split("\n")

    SolveInput(lines, digitsPerNode)