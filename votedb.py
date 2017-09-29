import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json

from election import Election
from chain import VoteChain
from transaction import RegistrationTransaction, VoteTransaction

tornado.options.define("port",
                        default=8080,
                        help="Webapp runs on this port",
                        type=int)

current_transactions = []

class ElectionResultHandler(tornado.web.RequestHandler):
    def get(self):
        global chain
        results = {}
        for election in chain.ballot:
            results[election.position] = election.results()
        self.write(json.dumps(results, indent=2))

class RegistrationHandler(tornado.web.RequestHandler):
    def post(self):
        global current_transactions
        if self.request.body:
            t = RegistrationTransaction.from_json(self.request.body)
            current_transactions.append(t)
            self.write(json.dumps(t['hash']))

class VoteHandler(tornado.web.RequestHandler):
    def post(self):
        global current_transactions
        if self.request.body:
            t = VoteTransaction.from_json(self.request.body)
            current_transactions.append(t)
            self.write(json.dumps(t['hash']))

def main():
    """
        Iniitialize the election here, and then start up 
        our webapp
    """

    global chain
    # Initialize the election
    CommanderInIceCream = Election('CommanderInIceCream',
                                    'RANK',
                                    ['ReeseWithoutASpoon', 'ChocoChipDough', 'MagicBrowny'])

    DairyQueenSecondTerm = Election('DairyQueenSecondTerm',
                                    'MAJORITY',
                                    ['yes', 'no'])

    StateDistrictMM = Election('StateDistrictMM',
                                'PICKTWO',
                                ['PnutButter', 'CreamCKol', 'MarshMallow'])

    CountyVanilla = Election('CountyVanilla',
                            'MAJORITY',
                            ['yes', 'no'])
    ballot = [
        CommanderInIceCream,
        DairyQueenSecondTerm,
        StateDistrictMM,
        CountyVanilla
    ]
    chain = VoteChain(ballot)

    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/results", ElectionResultHandler),
        (r"/registration", RegistrationHandler),
        (r"/vote", VoteHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == '__main__':
    main()
