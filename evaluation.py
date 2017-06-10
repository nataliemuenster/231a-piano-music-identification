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
    print "detected:", detected_keys
    return detected_keys, true_keys

#Process minimum edit distance using Levenshtein Distance between the true notes and detected ones
def calculateDistance(detected, true):
    if len(detected) > 0 and len(true) == 0: #if no keys actually played
        return len(detected)
    elif len(detected) == 0 and len(true) > 0: #if no keys detected
        return len(true)

    prevRow = range(len(true) + 1)
    for i, m in enumerate(detected):
        currRow = [i + 1]
        for j, n in enumerate(true):
            insertions = prevRow[j + 1] + 1 
            deletions = currRow[j] + 1      
            addSubst = (m != n)
            substitutions = prevRow[j] + addSubst
            currRow.append(min(insertions, deletions, substitutions))
        prevRow = currRow

    return prevRow[-1]



