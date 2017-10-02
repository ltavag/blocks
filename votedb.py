import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import httpclient
from tornado.options import define, options
import json
import os
from jinja2 import Environment, FileSystemLoader
import urllib

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(
    loader=FileSystemLoader(os.path.join(THIS_DIR, 'templates'))
)

from election import Election, InvalidVoteException
from chain import VoteChain
from transaction import RegistrationTransaction, VoteTransaction
from block import BlockMiner
import texter

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


class ChainDumpHandler(tornado.web.RequestHandler):
    def get(self):
        global chain
        self.write(json.dumps(chain, indent=2))

class UnminedTransactionHandler(tornado.web.RequestHandler):
    def get(self):
        global current_transactions
        self.write(json.dumps(current_transactions, indent=2))


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


class MiningHandler(tornado.web.RequestHandler):
    def post(self):
        global current_transactions
        global chain
        self.write(json.dumps(current_transactions))
        if len(current_transactions) > 0:
            chain.append(
                BlockMiner(
                    current_transactions,
                    chain[-1]['hash']
                ).mine_for(chain)
            )
        # Reset our current transactions array, since these have been confirmed
        current_transactions = []


class WebRegistrationHandler(tornado.web.RequestHandler):
    def get(self):
        template = env.get_template('register.html')
        self.write(template.render())

    def post(self):
        form_args = {x.split('=')[0]: x.split('=')[1]
                     for x in self.request.body.split('&')}
        name = form_args['name']
        phone = form_args['phone']
        phone.replace('-', '').replace('(', '').replace(')', '')
        phone = '+1' + phone

        # Create the new registration transaction
        r = RegistrationTransaction()
        r.finalize()

        # Send the signature by text to the voter
        texter.send_message(r.signed_data, phone)

        def handle_request(response):
            if response.error:
                print 'ERROR', response.error
            else:
                print 'SUCCESS', response.body

        # Push the registration transaction into our DB via HTTP call
        http = httpclient.AsyncHTTPClient()
        data = json.dumps(r)
        http.fetch("http://127.0.0.1:8080/registration",
                   handle_request, method='POST', body=data)

        # Re-direct to the vote page
        self.redirect('voter/' + r['hash'])


class WebVotingHandler(tornado.web.RequestHandler):
    def get(self):
        global ballot_conf
        template = env.get_template('vote.html')
        self.write(template.render(ballot = ballot_conf, rg_tx = self.request.uri.split('/')[-1]))

    def post(self):
        global chain
        form_args = {x.split('=')[0]: x.split('=')[1]
                     for x in self.request.body.split('&')}

        #Construct the vote from post body
        ballot_votes = [ {k:int(v) for k,v in form_args.iteritems() if k in chain.ballot[0].options and v.isdigit()},
                    {v:1 for k,v in form_args.iteritems() if k == 'DairyQueenSecondTerm'},
                    {k:1 for k,v in form_args.iteritems() if k in chain.ballot[2].options},
                    {v:1 for k,v in form_args.iteritems() if k == 'CountyVanilla'}
        ]

        try:
            for i, election in enumerate(chain.ballot):
                election.validate_vote(ballot_votes[i])
        except InvalidVoteException as e:
            self.write(repr(e))
            self.write(repr(e.message))
        else:
            t = VoteTransaction(input={
                "reg_tx_hash": form_args['register_tx'],
                "signature": form_args['signature'],
            },
            ballot_votes=ballot_votes)
            t.finalize()

            def handle_request(response):
                if response.error:
                    print 'ERROR', response.error
                else:
                    print 'SUCCESS', response.body

            # Push the registration transaction into our DB via HTTP call
            http = httpclient.AsyncHTTPClient()
            data = json.dumps(t)
            http.fetch("http://127.0.0.1:8080/vote",
                       handle_request, method='POST', body=data)
            self.write('YOUR VOTE HAS BEEN SUBMITTED')
        

def main():
    """
        Iniitialize the election here, and then start up 
        our webapp
    """

    global chain
    global ballot_conf 
    ballot_conf = json.load(open('ballot.json'))
    ballot = []
    for x in ballot_conf:
        ballot.append(Election(x['name'], x['type'], [y['name'] for y in x['options']]))
    chain = VoteChain(ballot)

    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/results", ElectionResultHandler),
        (r"/registration", RegistrationHandler),
        (r"/vote", VoteHandler),
        (r"/mine", MiningHandler),
        (r"/chain", ChainDumpHandler),
        (r"/trans", UnminedTransactionHandler),
        (r"/webregister", WebRegistrationHandler),
        (r"/voter.*", WebVotingHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
