import sys

def parser(texte) :
    print(type(texte))
    s1 = texte.split("\t")
    print(type(s1[0]))
    print(s1)
    s2 = [s1[i] for i in range(1, len(s1), 2)]
    return s2

def function(filePath) :
    text = ""
    with open(filePath) as f :
        text = f.read()
    encoded = text
    
    print(encoded[:100])
    
    pencoded = parser(encoded)

    # print(pencoded[:100])

    return []


def main() :
    filePath = "tmp.txt"
    if len(sys.argv) == 2:
        filePath = sys.argv[1]
    
    function(filePath)
    return 0


main()