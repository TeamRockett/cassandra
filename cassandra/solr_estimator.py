from nltk import pos_tag
from nltk.tokenize import word_tokenize

class SolrEstimator(object):
    def __init__(self, solr):
        self.solr = solr

    def replace_names(self, string, replace_with = 'this person'):
        text = string.split(' ')

        words = [x for (pre,x) in zip(['.']+text, text+[' '])
                if (x[0].isupper()) and (pre[-1] != '.') and (pre[-1] != ':') and (len(x) > 1)]

        for word in words:
            if(word[-1] == '.'):
                replace_with = replace_with + '.'

            string = string.replace(word, replace_with)

        return string

    def replace_names_with_pos(self, string, replace_with = 'this person'):
        text = word_tokenize(string)
        pos  = pos_tag(text)

        words = []
        for word, tag in pos:
            if(tag == 'NNP' and len(word) > 3):
                words.append(word)

        for word in words:
            string = string.replace(word, replace_with)

        return string

    def find_best_dialogue(self, input):
        q = input
        self.solr.addDialogue({'question': q, 'response': "-", 'is_tmp': True})
        res = self.solr.getBestDialogues('question_full')
        self.solr.deleteTemp()
        if len(res) > 0:
            # print('Cassandra: ' + self.replace_names(res[0]['response']))
            return 'Cassandra: ' + self.replace_names_with_pos(res[0]['response'])
        else:
            return "I don't know that duty."

