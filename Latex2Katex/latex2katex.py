import os

def latexToKatex(input: str, mathsty: str = None) -> str:
    output = input.replace("$", "$$")
    output = output.replace("$$$$", "$$")

    if mathsty != None:
        output = mathstyReplace(output, mathsty)

    print(output)

def mathstyReplace(input, mathsty):
    lines = mathsty.splitlines()
    
    for line in lines:
        if "\\newcommand" in line:
            toReplace, replace = parseBrackets(line)
            input = input.replace(toReplace, replace)
    return input
            
            


def parseBrackets(input):
    openBracketCount = 0
    output = list()
    pos = 0
    currString = ""
    while pos < len(input):
        if input[pos] == "}":
            openBracketCount -= 1
            if openBracketCount == 0:
                output.append(currString)
                currString = ""
        
        if openBracketCount > 0:
            currString += input[pos]

        
        if input[pos] == "{":
            openBracketCount += 1

        pos += 1

    return output[0], output[1]

        
        
    



if __name__ == "__main__":
    input = open("latex.txt", "r").read()
    
    print(parseBrackets("\\newcommand{\\Jc}{\\mathcal{J}}"))
    print(parseBrackets("\\newcommand{\\Kc}{\\mathcal{K}}"))
    print(parseBrackets("\\newcommand{\\Hc}{\\mathcal{H}}"))
    if os.path.isfile("math.sty"):
        print("math.sty found! We will use this file to update your Latex to Katex!")
        mathsty = open("math.sty", "r").read()
        latexToKatex(input, mathsty)
    else:
        print("math.sty not found! Running code without file")
        latexToKatex(input)
        
