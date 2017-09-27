#! /usr/bin/python

from collections import defaultdict
VOTE_TYPES = ['PICKTWO','MAJORITY','RANK']

class InvalidVoteException(Exception):
	def __init__(self, message):
		self.message = message

class Election(defaultdict):
	def __init__(self, vote_type, options):
		self.options = options	
		self.vote_type = vote_type
		defaultdict.__init__(self, int)

	def validate_vote(self, vote):
		write_ins = [k for k in vote if k not in self.options]
	
		if len(write_ins) > 1:
			raise InvalidVoteException, 'Only one write in is allowed'
			
		if self.vote_type == 'PICKTWO':
			if len(vote) != 2:
				raise InvalidVoteException, 'Must pick two candidates'		
	
			if not all(v==1 for v in vote.values()):
				raise InvalidVoteException, 'Can only increment each candidates votes by 1'
		
		if self.vote_type == 'MAJORITY':
			if len(vote) !=1:
				raise InvalidVoteException, 'Can only vote a single way'


		if self.vote_type == 'RANK':
			"""
				This is the only tricky vote type where
				the vote object contains the inverse of the points
				allocated to the candidate. (Rank)
			"""
			if len(vote.values()) != len(set(vote.values())):
				raise InvalidVoteException, "Can't rank two candidates the same"
		
		return True

	def include_vote(self, vote):
		if self.vote_type == 'RANK':
			rank_to_points = {i:len(self.options)+1-i 
							 for i in xrange(1,len(self.options)+1)}
			
			corrected_vote = {k:rank_to_points[v] for k,v in vote.iteritems()}
			vote = corrected_vote
			
		for k, v in vote.iteritems():
			self[k] += v
		
	def __add__(self, vote):
		if not isinstance(vote,dict):
			raise InvalidVoteException, 'Vote needs to be a dict'

		if self.validate_vote(vote):
			self.include_vote(vote)

		return self

	def results(self):
		return dict(self)


if __name__ == '__main__':
	import random
	import pprint

	issue9 = Election('RANK',['yes','no','maybe'])

	vote = {'yes':1}
	issue9 += vote
	pprint.pprint(issue9.results())

	vote = {'no':1,'maybe':2}
	issue9 += vote
	pprint.pprint(issue9.results())
