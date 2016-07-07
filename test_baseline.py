import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

def get_all_conversations(file = 'friends_test'):
    with open(file, 'r') as myfile:
        data = myfile.read().replace('\n', '')
        data = data.strip()
        data = re.sub(r'\([^)]*\)', '', data)

    conversatios = data.split("<br>")
    conversatios = [s for s in conversatios if s]

    return conversatios

def get_dialogues(conversatios):
    dialogues = []
    for index in range(len(conversatios)):
        if(index+2 < len(conversatios)):
            name1 = re.findall(r'^[A-Z]*:', conversatios[index])
            name3 = re.findall(r'^[A-Z]*:', conversatios[index+2])
            if name1 and name3 and name1 == name3:
                text1 = re.sub(r"^[A-Z]*:", "", conversatios[index])
                text2 = re.sub(r"^[A-Z]*:", "", conversatios[index+1])
                text3 = re.sub(r"^[A-Z]*:", "", conversatios[index+2])
                text1 = text1.strip()
                text2 = text2.strip()
                text3 = text3.strip()
                dialogue = [text1, text2, text3]
                dialogues.append(dialogue)

                # print("==========")
                # print("A:", text1)
                # print("B:", text2)
                # print("A:", text3)

    # print(dialogues)

    return dialogues

def find_best_dialogue(input, dialogues):
    all = list(map(lambda x: [get_cosine(text_to_vector(input), text_to_vector(x[0])), get_cosine(text_to_vector(input), text_to_vector(x[1]))], dialogues))
    a = list(map(lambda x: max(get_cosine(text_to_vector(input), text_to_vector(x[0])), get_cosine(text_to_vector(input), text_to_vector(x[1]))), dialogues))

    max_index = a.index(max(a))
    ind = all[max_index].index(max(all[max_index]))

    # print("=========")
    # print(all[max_index])
    # print(dialogues[max_index])
    # print(ind)
    # print(dialogues[max_index][ind])
    # print("=========")

    print("Cassandra:", dialogues[max_index][ind+1])

    # print(text_to_vector(input))
    # print(text_to_vector(dialogues[max_index][ind]))
    # print(get_cosine(text_to_vector(input), text_to_vector(dialogues[max_index][ind])))

conv = get_all_conversations()
dial = get_dialogues(conv)

print("\n\n\n")
print("Hello! Cassandra is listening to you...")
user_input = input("You: ")

while user_input != "Bye":
    find_best_dialogue(user_input, dial)
    user_input = input("You: ")

print("Cassandra is going to sleep now...")
print("\n\n\n")
