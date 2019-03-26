import random,sys


if (len(sys.argv) > 1):
    filename = sys.argv[1]
else:
    filename = "words.txt"

lines = open('../dataset/'+filename).readlines()
random.shuffle(lines)
file = open('../dataset/'+filename, 'w')
file.writelines(lines)
file.close()

print("File ("+filename+") shuffled successfully")