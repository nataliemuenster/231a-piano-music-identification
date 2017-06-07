def totalError(video_name, detected):
    true_file_name = video_name + "_solution.txt"
    true_keys = []
    detected_keys = []
    with open(true_file_name) as true_file:
        for line in true_file:
            #if file formatted wrong, return error
            line = line.replace(" \n", "")
            line = line.replace("\n", "")
            true_keys.extend(line.split(", "))
    for pressed in detected:
        detected_keys.extend(pressed)

    print "correct length vs our length:", len(true_keys), len(detected_keys)
    print "correct:", true_keys
    print "ours:", detected_keys


# you may also want to remove whitespace characters like `\n` at the end of each line
#content = [x.strip() for x in content] 
#need to strip ""? spaces too


#def calculateDist(true, detected):

#Process minimum edit distance using Levenshtein Distance between quote inputs and one title for spellchecking
#Limits edit distance to 4 before it automatically fails
'''def calculateDistance(true, detected):
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
'''


