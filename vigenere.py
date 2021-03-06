wordFreq = [0.08166999999999999, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406,
            0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06326999999999999, 0.09055999999999999, 0.02758, 0.00978, 0.0236, 0.0015, 0.01974, 0.00074]


def processLine(Line, CharaterCounts):
    # mian function to process charater
    for character in Line:
        if ord(character) in range(97, 123):
            CharaterCounts[character] += 1


def createCharaterCounts(CharaterCounts):
    # initial count array
    for i in range(97, 123):
        CharaterCounts[chr(i)] = 0


def charaterCounts(Line):
    # countCharater main >charaterCounts(<message>,<counterContainer>)
    # return charaterCountItems:{"character": num,"character": num...}
    charaterCounts = {}
    createCharaterCounts(charaterCounts)
    processLine(Line.lower(), charaterCounts)
    pairs = list(charaterCounts.items())
    charaterCountItems = [[x, y] for (x, y) in pairs]
    return charaterCountItems


def printCharatercounts(charaterCountItems):
    for i in range(len(charaterCountItems)):
        print(charaterCountItems[i][0]+":"+str(charaterCountItems[i][1]))


def devideMessage(message, divnum):
    # devideMessage
    # eg. >devideMessage("dasdas",2)
    out = {}
    for m in range(0, divnum):
        out[m] = ""

    for i in range(0, divnum):
        for j in range(0, len(message)):
            if(j % divnum == i):
                out[i] += message[j]

    '''  
    for i in range(0, divnum):
        print(out[i])
    '''

    return out


def vigenere_enc(message, key="abc"):
    message = message.lower()
    encMessage = ""
    for i in range(0, len(message)):
        encMessage += chr(((ord(message[i])-97) + (ord(key[i % len(key)])-97)) % 26+97)
    return encMessage


def vigenere_dec(message, key=""):
    message = message.lower()
    decMessage = ""
    for i in range(0, len(message)):
        decMessage += chr(((ord(message[i])-97) - (ord(key[i % len(key)])-97)) % 26+97)
    return decMessage


def vigenere_enc_Ic(charaterCountItems):
    sum = 0
    charaterIc = 0
    for i in range(0, len(charaterCountItems)):
        sum += charaterCountItems[i][1]
    for i in range(0, len(charaterCountItems)):
        charaterIc = charaterIc + \
            (charaterCountItems[i][1] *
             (charaterCountItems[i][1]-1))/(sum*(sum-1))
    return charaterIc


def vigenere_enc_MIc(charaterCountItems, m=0):
    sum = 0
    charaterMIc = 0

    for i in range(0, len(charaterCountItems)):
        sum += charaterCountItems[i][1]
    for i in range(0, len(charaterCountItems)):
        charaterMIc = charaterMIc + \
            wordFreq[i]*((charaterCountItems[(i+m) % 26][1])/sum)
    return charaterMIc


def caculateBestLength(line):
    probKeyLength = []
    for keyLength in range(0, 16):
        out = devideMessage(line, keyLength)
        for i in range(0, len(out)):
            charaterIc = vigenere_enc_Ic(charaterCounts(out[i]))
            if charaterIc > 0.065:
                probKeyLength.append(keyLength)
                for i in range(0, len(out)):
                    charaterIc = vigenere_enc_Ic(charaterCounts(out[i]))
                    print(str(keyLength)+" "+str(charaterIc))
                print("")
                break
    return probKeyLength

# def vigenere_crack(message,length):


def test_vigenere_Dec(key="crypto"):
    a = ""
    infile = open("message.txt", "r")
    for line in infile:
        a = vigenere_dec(line, key)
        print(a)


def crackKey(line, keyLehgth=6):
    bestMIc = 0
    keyOffset = []
    key = []
    for i in range(0, keyLehgth):
        keyOffset.append(0)
        key.append("")
    out = devideMessage(line, keyLehgth)
    for i in range(0, keyLehgth):
        for j in range(0, 26):
            charaterMIc = vigenere_enc_MIc(charaterCounts(out[i]), j)
            if charaterMIc > bestMIc:
                bestMIc = charaterMIc
                keyOffset[i] = j
            #print(str(j)+ " " +str(charaterMIc))
        #print("Best" + " "+str(keyOffset[i])+ " " + str(bestMIc))
        bestMIc = 0
        # print("")

    for i in range(0, keyLehgth):
        key[i] = chr(keyOffset[i]+97)
    # print(key)
    return key


def main():
    filename = "message.txt"
    infile = open(filename, "r")
    for line in infile:
        probKeyLength = caculateBestLength(line)
        for i in range(0, len(probKeyLength)):
            key = crackKey(line, probKeyLength[i])
            print(key)


if __name__ == '__main__':
    main()
