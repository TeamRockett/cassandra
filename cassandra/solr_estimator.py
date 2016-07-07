class SolrEstimator(object):
    def __init__(self, solr):
        self.solr = solr

    def find_best_dialogue(self, input):
        q = input
        self.solr.addDialogue({'question': q, 'response': q, 'is_tmp': True})
        res = self.solr.getBestDialogues('question')
        self.solr.deleteTemp()
        if len(res) > 0:
            return 'Cassandra: ' + res[0]['response']
        else:
            return "I don't know that duty."

