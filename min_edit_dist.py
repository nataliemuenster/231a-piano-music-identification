def totalError(true_file_name, detected):
    true_keys = []
    with open(true_file_name) as true_file:
        for line in true_file_name:
            #if file formatted wrong, return error
            true_keys.append(line.split(", "))

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 
#need to strip ""? spaces too

#Process minimum edit distance using Levenshtein Distance between quote inputs and one title for spellchecking
#Limits edit distance to 4 before it automatically fails
def calculateDistance(true, detected):
    if len(quote) > 0 and len(title) == 0:
        return len(quote)
    elif len(quote) == 0 and len(title) > 0:
        return len(title)

    prevRow = range(len(title) + 1)
    for i, m in enumerate(quote):
        currRow = [i + 1]
        for j, n in enumerate(title):
            insertions = prevRow[j + 1] + 1 
            deletions = currRow[j] + 1      
            addSubst = (m != n)
            substitutions = prevRow[j] + addSubst
            currRow.append(min(insertions, deletions, substitutions))
        prevRow = currRow

    return prevRow[-1]

if __name__ == '__main__':
    testArray = [['D'], ['A', 'B'], ['D', 'F', 'G']]
    totalError = totalError("test.file.txt", )