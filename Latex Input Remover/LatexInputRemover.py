#Open a latex file and replace the \input{...} with the content of that input

import os


def findInputContent(s):
    strLen = len(s)
    currentPos = 0
    generatedString = ""
    for i in range(len(s)):
        generatedString += s[i]
        currentPos += 1
        
        if '\\input{' in generatedString:
            
            bracketPos = -1

            while s[bracketPos] != '}':
                bracketPos -=1
            return s[currentPos:bracketPos]

        
            
        
    print("ERROR: '\\input{' not found in given string!")


def splitFileAndPath(input):
    print(f"input to splitFileAndPath: {input}")
    file = ''
    loc = -1
    while input[loc] != "\\" and input[loc] != "/":
        #TODO FIGURE OUT LOC GOING OUT OF RANGE!!!
        # print(f"loc: {loc}, with input[loc]: {input[loc]}")
        # print(input[loc] != "\\" or input[loc] != "/")
        file = input[loc] + file
        loc -= 1

    

    return file, input[:loc]

def genLatexFile(inputLatexPath, file):
    initialPath = os.path.join(os.getcwd(), inputLatexPath)
    os.chdir(inputLatexPath)
    # print(f"CurrentDir: {os.getcwd()}")
    latex = open(file).readlines()
    # print(latex)
    outputLatex = []
    for line in latex:
        if "\\input{" in line:
            # print(line)
            inputContent = findInputContent(line)
            fileAdd, path = splitFileAndPath(inputContent)

            outputLatex.append(genLatexFile(path, fileAdd))
            print(f"Initial Path: {initialPath}")
            os.chdir(initialPath)

        else:
            outputLatex.append(line)

    return outputLatex






if __name__ == "__main__":
    inputLatexPath = "Latex\\quiz2\\"

    # cwd = os.getcwd()

    # os.chdir(os.path.join(cwd, inputLatexPath))

    # print(f"cwd: {os.getcwd()}")
    # os.chdir('../shared_quiz')

    # print(f"cwd: {os.getcwd()}")
    # # genLatexFile(inputLatexPath)
    # file, path = splitFileAndPath('C:\\Users\\dpbird\\Documents\\Useful Systems\\Latex Input Remover\\Latex\\shared_quiz\\instruction.tex')
    # print(f"file: {file}, path: {path}")
    # for (root,dirs,files) in os.walk("Latex",topdown=True):
    #       print("Directory path: %s"%root)
    #       print("Directory Names: %s"%dirs)
    #       print("Files Names: %s"%files)

    # cwd = os.getcwd()
    # print(cwd)
    genLatexFile(inputLatexPath, 'main.tex')





    # a = findInputContent("       \\input{Example.tex}")
    # print(a)
