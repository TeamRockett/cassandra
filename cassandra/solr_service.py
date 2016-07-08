import pysolr
from cassandra.dialogue import Dialogue

class SolrService(object):
    def __init__(self, core):
        self.conn = pysolr.Solr('http://localhost:8983/solr/' + core, timeout=10)

    def getConnection(self):
        return self.conn

    def getDialogue(self, dialogue_id):
        results = self.conn.search('id:'+dialogue_id)
        for result in results:
            return result

    def getSimilarDialogues(self, dialogue_id, cols, tf=1, df = 1, count = 10):
        similar = self.conn.more_like_this(q='id:'+dialogue_id, mltfl=cols, **{'mlt.mindf': df, 'mlt.mintf' : tf, 'mlt.count' : count})
        dialogues = []
        for dialogue in similar:
            dialogues.append(dialogue)

        return dialogues

    def getBestDialogues(self, cols, tf=1, df = 1, count = 1):
        similar = self.conn.more_like_this(q='is_tmp:true', mltfl=cols, **{'mlt.mindf': df, 'mlt.mintf' : tf, 'mlt.count' : count})
        dialogues = []
        for dialogue in similar:
            dialogues.append(dialogue)

        return dialogues


    def getAllDialogues(self):
        results = self.conn.search('*:*')
        dialogues = []
        for dialogue in results:
            dialogues.append(dialogue)

        return dialogues


    def addDialogue(self, dialogueDict):
        toAdd = []
        toAdd.append(dialogueDict)

        self.conn.add(toAdd)

    def deleteTemp(self):
        self.conn.delete(q='is_tmp:true')

    def load_dialogues(self, dialogues):
        for d in dialogues:
            self.addDialogue({'question': d[0], 'response': d[1]})
