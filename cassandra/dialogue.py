class Dialogue(object):
    def __init__(self,
            id,
            question,
            response,
            next_response,
            is_tmp):
        self.id = id
        self.question =  question
        self.response =  response
        self.is_tmp =  is_tmp

        def __str__(self):
            return "Id: {id},\nQuestion: {question},\nResponse: {response},\nNext response: {next_response},\nIs temporary: {is_tmp}".format(id=self.id,
                    question=sel.question, response=self.response,next_response=self.next_response,is_tmp=self.is_tmp)

        @property
        def id(self):
            return self.id

        @property
        def question(self):
            return self.question

        @property
        def response(self):
            return self.response

        @property
        def next_response(self):
            return self.next_response

        @property
        def is_tmp(self):
            return self.is_tmp
