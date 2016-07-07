import re, math
from collections import Counter

WORD = re.compile(r'\w+')

class CustomEstimator(object):
    def get_cosine(self, vec1, vec2):
         intersection = set(vec1.keys()) & set(vec2.keys())
         numerator = sum([vec1[x] * vec2[x] for x in intersection])

         sum1 = sum([vec1[x]**2 for x in vec1.keys()])
         sum2 = sum([vec2[x]**2 for x in vec2.keys()])
         denominator = math.sqrt(sum1) * math.sqrt(sum2)

         if not denominator:
            return 0.0
         else:
            return float(numerator) / denominator

    def text_to_vector(self, text):
         words = WORD.findall(text)
         return Counter(words)

    def find_best_dialogue(self, input, dialogues):
        all = list(map(lambda x: [self.get_cosine(self.text_to_vector(input), self.text_to_vector(x[0])), self.get_cosine(self.text_to_vector(input), self.text_to_vector(x[1]))], dialogues))
        a = list(map(lambda x: max(self.get_cosine(self.text_to_vector(input), self.text_to_vector(x[0])), self.get_cosine(self.text_to_vector(input), self.text_to_vector(x[1]))), dialogues))

        max_index = a.index(max(a))
        ind = all[max_index].index(max(all[max_index]))

        # print("=========")
        # print(all[max_index])
        # print(dialogues[max_index])
        # print(ind)
        # print(dialogues[max_index][ind])
        # print("=========")

        print("Cassandra:", dialogues[max_index][ind+1])

        # print(self.text_to_vector(input))
        # print(self.text_to_vector(dialogues[max_index][ind]))
        # print(self.get_cosine(self.text_to_vector(input), self.text_to_vector(dialogues[max_index][ind])))

