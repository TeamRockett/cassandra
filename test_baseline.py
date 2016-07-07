import re, math
from collections import Counter

from cassandra.solr_service import SolrService
from cassandra.solr_estimator import SolrEstimator

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
                # dialogue = [text1, text2, text3]
                dialogues.append([text1, text2])
                dialogues.append([text2, text3])

                # print("==========")
                # print("A:", text1)
                # print("B:", text2)
                # print("A:", text3)

    # print(dialogues)

    return dialogues


conv = get_all_conversations()
dial = get_dialogues(conv)

solr = SolrService('cassandra')
# for d in dial:
#     solr.addDialogue({'question': d[0], 'response': d[1]})

# q = "How are you?"
# print(solr.addDialogue({'question': q, 'response': q, 'next_response': q, 'is_tmp': True}))
# res = solr.getSimilarDialogues("f12ded89-49c6-4935-b658-fba8aa2749ab", 'question,response')
# for r in res:
#     print('id:' + r['id'])
#     print('question:' + r['question'])
#     print('response:' + r['response'])
#     print('next_response:' + r['next_response'])


print("\n\n\n")
print("Hello! Cassandra is listening to you...")
user_input = input("You: ")

est = SolrEstimator(solr)
while user_input != "Bye":
    res = est.find_best_dialogue(user_input)
    print(res)
    user_input = input("You: ")

print("Cassandra is going to sleep now...")
print("\n\n\n")
