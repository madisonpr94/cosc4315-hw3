
# -*- coding: utf-8 -*-

import re, sys, math

def StrToInfInt(s, n):
    """Strings are read into "infnite integer" lists by starting from the end
    of the string and reading n characters back recursively until fewer than n
    characters remain (where n represents the digits per node). Each returning
    step of the recursion then adds its n ending characters to the resulting
    list of the previous step until the full integer is built. This solution
    naturally "aligns" digits such that any non-full nodes are shifted to the
    most signicant digits."""
    if(len(s) <= n):
        return [int(s)]
    else:
        si = int(s[-n:])
        t = StrToInfInt(s[:-n], n)
        t.append(si)
        return t

def InfIntToStr(s, i, n):
    """Accepts a list of numbers as an infinite integer and converts it to a
    string."""
    if i == len(s):
        return ""
    elif i == 0:
        result = str(s[i]) + InfIntToStr(s, i + 1, n)
    else:
        result = str(s[i]).zfill(n) + InfIntToStr(s, i + 1, n)
    return result

def AddInfInt(a, b, c, n):
    """Two infnite integers are given to be added together. Starting from the
    least signi- cant digits, nodes are added together (similarly to how
    addition by hand is performed, but using multiple digits at a time). If the
    sum exceeds 10n , we will carry a 1 in the next recursive step and reduce
    the sum for the current step by 10n . The last elements in both lists are
    removed and addition continues towards the most signicant digits. Each
    recursive step returns the full infinite integer list for the addition
    performed so far."""
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
    return (AddInfInt(a, b, carry, n) or []) + [sum]

def MultiplyAcross(a, b, i, n):
    # TODO: Documnentation
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
    """This operation is performed similarly to multiplication by hand. The
    algorithm multiplies groups of digits together and sums the result.
    Mathematically, this can be represented by the following:

     n   n    d(i+j)
     Σ   Σ  10      b a
    i=0 j=0          i j

    (1) n: total nodes in b, m: total nodes in a, d: digits per node; indices
    move right to left

    However, using list-represented integers introduces some challenges.
    Instead of multiplying the nodes by 10d(i+j) , it is best to create an
    infinite integer with (i+j) zero-value nodes to the right. It is also
    important to be mindful of carry-out values; while the equation above does
    not need to respect carry-out, it must be ensured that the algorithm
    respects the specific digits per node requirement. Therefore, each step of
    the recursion should produce an infnite integer of the form
    [carry][product] (i+j)*[0] to be added to each successive step."""
    if i == len(b):
        return [0]
    else:
        resultnext = MultiplyInfInt(a, b, i + 1, n)
        result = MultiplyAcross(a, b[i], 0, n)
        result = result + [0] * (len(b) - i - 1)
        return AddInfInt(result, resultnext, 0, n)


def SolveLine(s, n):
    """The goal is to take a single line of input in the form of an expression,
    and produce an infinite integer result. As with prior algorithms, this will
    be a recursive approach. All input provided to this algorithm will be in
    the form [function name] followed by either an integer constant or another
    [function name] (...). Function calls should be recursively evaluated and
    reduced to infinite integer constants, which can be operated upon. Regular
    expressions will be used to identify sections of the input string in the
    form [function name]([constant], [constant]). These subexpressions will be
    solved and their results re-inserted into the input expression until the
    entire expression is solved."""
    s = s.replace(' ', '')
    find = re.search('((add|multiply)\(\d+,\d+\))', s)
    if not find:
        return None
    else:
        if find.group(1) == s:
            si = s.split('(')
            numResults = re.match("([0-9]+),([0-9]+)", si[1])
            nums = [StrToInfInt(numResults.group(1), n),
                    StrToInfInt(numResults.group(2), n)]
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

# def SolveInput(s, n):
#     """Parses a list of lines using s and prints out every evaluated line or
#     an error message for every malformed line."""
#     if len(s) == 0:
#         return
#     if re.search('(.+)', s[0]):
#         result = SolveLine(s[0], n)
#         if result != [-1]:
#             resultStr = InfIntToStr(result, 0, n)
#             # print(s[0], "=", resultStr, " ", TestInput(s[0], resultStr))
#             print(s[0], "=", resultStr)
#         else:
#             print("Invalid expression: ", s[0])
#     SolveInput(s[1:], n)

def SolveInput(s, n):
    """Parses a single line using s and prints out the evalutated line or
    or an error message if the line is malformed."""
    # TODO: Documentation
    if re.search('(.+)', s):
        result = SolveLine(s, n)
        if result:
            resultStr = InfIntToStr(result, 0, n)
            print s, "=", resultStr
        else:
            print "Invalid expression: ", s

def TestInput(s, n):
    """DEBUGGING PURPOSES ONLY:

    Using the python interpreter itself via eval(), evaluate an input
    function call and compare it against our result."""
    def multiply(a, b):
        return a * b
    def add(a, b):
        return a + b
    return int(eval(s)) == int(n)


if len(sys.argv) < 2:
    print ("Usage: python2 infinitearithmetic.py \"" +
           "input=<file name>;digitsPerNode=<number>\"")

else:
    args = re.match("input=(.*);digitsPerNode=(\d+)", sys.argv[1])

    if not args:
        print "Malformed input on command line."
        quit(-1)

    inputFilename = args.group(1)
    digitsPerNode = int(args.group(2))

    infile = open(inputFilename, 'r')
    lines = infile.read().split("\n")

    # SolveInput(lines, digitsPerNode)
    map(lambda x: SolveInput(x, digitsPerNode), lines)
