
# -*- coding: utf-8 -*-

import re, sys, math

def StrToInfInt(s, n):
    """Strings are read into "infnite integer" lists by starting from the end
    of the string and reading n characters back recursively until fewer than n
    characters remain (where n represents the digits per node). Each returning
    step of the recursion then adds its n ending characters to the resulting
    list of the previous step until the full integer is built. This solution
    naturally "aligns" digits such that any non-full nodes are shifted to the
    most signicant digits.

    Precondition:
        s is a string representing a number, n is the digits per node
    Postcondition:
        Returns a list of integers representing the number in the input string
    """

    if type(s) == list: # Inf int was provided as input
        return s

    if(len(s) <= n):
        return [int(s)]

    else:
        return StrToInfInt(s[:-n], n) + [int(s[-n:])]

def InfIntToStr(s, i, n):
    """Accepts a list of numbers as an infinite integer and converts it to a
    string.

    Precondition:
        s is an integer list, i is an index into that list, and n is the digits
        per node
    Postcondition:
        returns a string representing s
    """
    if i == len(s):
        return ""
    elif i == 0:
        return str(int(s[i])) + InfIntToStr(s, i + 1, n)
    else:
        return str(int(s[i])).zfill(n) + InfIntToStr(s, i + 1, n)

def AddInfInt(a, b, c, n):
    """Two infnite integers are given to be added together. Starting from the
    least signicant digits, nodes are added together (similarly to how addition
    by hand is performed, but using multiple digits at a time). If the sum
    exceeds 10n, we will carry a 1 in the next recursive step and reduce the
    sum for the current step by 10n . The last elements in both lists are
    removed and addition continues towards the most signicant digits. Each
    recursive step returns the full infinite integer list for the addition
    performed so far.

    Precondition:
        a and b are integer lists, c is the carry-in
        value (must start at 0), n is the digits per node
    Postcondition:
        returns a + b
    """
    if a == None or b == None:
        return None

    if a == b == []:
        if c != 0:
            return [c]
        else:
            return

    sum = (c + (a[-1] if len(a) > 0 else 0) + (b[-1] if len(b) > 0 else 0))
    return (AddInfInt(a[:-1], b[:-1],
                      math.floor(sum / 10 ** n), n) or []) + [sum % (10 ** n)]

def MultiplyAcross(a, b, i, n):
    """This function performs a single multiplication sub-step by multiplying
    one node of b against every node of a and summing the results before returning
    the total value for this sub-step of the multiplication.

    Precondition:
        a is an integer list, b is a single integer,
        i = 0 (index into a), n = digits per node
    Postcondition:
        returned value is a * b
    """
    if i == len(a):
        return [0]
    else:
        # (b * a[i]) % 10 ** n is the subresult for this multiplication sub-step
        # math.floor((b * a[i]) / 10 ** n) is the carry value to the next step
        # (len(a) - i - 1) zeroes are added to the end of the result list to reach
        #       correct significance

        if math.floor((b * a[i]) / 10 ** n) == 0:
            return AddInfInt(
                [(b * a[i]) % (10 ** n)] + [0] * (len(a) - i - 1),
                MultiplyAcross(a, b, i + 1, n), 0, n)
        else:
            return AddInfInt(
                [math.floor((b * a[i]) / 10 ** n)] +
                [(b * a[i]) % (10 ** n)] + [0] * (len(a) - i - 1),
                MultiplyAcross(a, b, i + 1, n), 0, n)

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
    the recursion should produce an infinite integer of the form
    [carry][product] (i+j)*[0] to be added to each successive step.

    Precondition:
        a and b are integer lists, i is 0 (index into b), n is digits per node
    Postcondition:
        returned value is a * b
    """
    if i == len(b):
        return [0]
    else:
        return AddInfInt(MultiplyAcross(a, b[i], 0, n) + [0] * (len(b) - i - 1),
                         MultiplyInfInt(a, b, i + 1, n), 0, n)

def LexLine(s):
    """Uses regular expression matching to extract discrete tokens from lines
    of input and places them into a list

    Precondition:
        s is a string representing a line of input
    Postcondition:
        returns a list of tokens representing the given input (or None, if
        a invalid token is encountered)
    """
    if s == "":
        return []
    if re.match("^(add|multiply|\(|\)|,|\d+)", s):
        token_list = [re.match("^(add|multiply|\(|\)|,|\d+)", s).group(0)]
        return token_list + (LexLine(s[len(token_list[0]):]) or [])
    else:
        # Invalid token encountered
        return None

def SolveLine(s, a, n):
    """Replaces sets of terminal tokens [operator(int, int)] with their results
    in the token list, linearly scanning the token list each time until the list
    of tokens is either a single result or unresolvable (invalid)

    Precondition:
        s is a list of input tokens, a is the index into the token list (must
        start at 0), n is the digits per node

    Postcondition:
        returns the numerical result of the operation on the given line
        (represented by tokens s)
    """

    if len(s) == 1:
        return s[0]
    if (a + 2) >= len(s):
        # Invalid input (No remaining solvable operations)
        return None

    if s[a] in ["add", "multiply"]:
        if type(s[a + 1]) == list or re.search("(\d+)", s[a + 1]):
            if type(s[a + 2]) == list or re.search("(\d+)", s[a + 2]):
                # The next two tokens are numbers [operator(int, int)]
                return SolveLine(
                    s[:a] + [
                        AddInfInt(StrToInfInt(s[a + 1], n),
                                  StrToInfInt(s[a + 2], n),
                                  0, n)
                        if s[a] == "add" else
                        MultiplyInfInt(StrToInfInt(s[a + 1], n),
                                       StrToInfInt(s[a + 2], n),
                                       0, n)
                    ] + s[(a + 3):],
                    0, n)

    return SolveLine(s, a + 1, n)

def SolveInput(s, n):
    """Recursively parses single lines of s, a list of input lines, and prints out the evalutated line or
    or an error message if the line is malformed.

    Precondition:
        s is a list of strings representing lines of input, n is the digits per node
    Postcondition:
        displays the input statement and the corresponding result, or "Invalid
        expression" if the statement was invalid
    """

    if len(s) == 0:
        return
    elif s[0] == "":
        SolveInput(s[1:], n)
    else:
        result = SolveLine(list(filter(lambda a: a not in ['(', ')', ','],
                                LexLine(s[0].replace(' ', '')) or [])), 0, n)
        if result and not type(result) == str:
            # def TestInput(solved, inputString):
            #     """Evaluates input using the python interpreter directly. Used
            #     exclusively for testing/debugging purposes to validate output
            #     correctness.
            #     """
            #     def multiply(a, b):
            #         return a * b
            #     def add(a, b):
            #         return a + b
            #     correctness = solved == str(eval(inputString))
            #     return solved + " " + str(correctness)
            # print (s[0], "=", TestInput(InfIntToStr(result, 0, n), s[0]))
            print (s[0], "=", InfIntToStr(result, 0, n))
        else:
            print ("Invalid expression:", s[0])
        SolveInput(s[1:], n)


if len(sys.argv) < 2:
    print ("Usage: python3 infinitearithmetic.py \"" +
           "input=<file name>;digitsPerNode=<number>\"")

else:
    args = re.match("input=(.*);digitsPerNode=(\d+)", sys.argv[1])

    if not args:
        print ("Usage: python3 infinitearithmetic.py \"" +
            "input=<file name>;digitsPerNode=<number>\"")
        quit(-1)

    inputFilename = args.group(1)
    digitsPerNode = int(args.group(2))

    infile = open(inputFilename, 'r')
    lines  = infile.read().replace("\r","").split("\n")

    SolveInput(lines, digitsPerNode)
