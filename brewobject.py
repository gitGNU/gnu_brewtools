"""
* Copyright (c) 2008, Flagon Slayer Brewery
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above copyright
*       notice, this list of conditions and the following disclaimer in the
*       documentation and/or other materials provided with the distribution.
*     * Neither the name of the Flagon Slayer Brewery nor the
*       names of its contributors may be used to endorse or promote products
*       derived from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY Flagon Slayer Brewery ``AS IS'' AND ANY
* EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL Flagon Slayer Brewery BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from util import *
import sys

class BrewObject(object):
	"""
	Generic for system objects.
	
	Do not use, inherit.
	"""

	crudAttributes = ['name']
	name = ""
	indexer = None

	def __str__(self):
		return self.name

	def __setattr__(self,name,value):
		super(BrewObject, self).__setattr__(name,value)
		sys.stdout.write("setting attribute %s\n" % name)
		try: self.save()
		except: sys.stderr.write("couldn't save %s\n" % name)
	
	def __init__(self,indexer,**kwargs):
		"""
		Creates brewobject

		indexer: Indexer that calls me.
		**kwargs: Optional named arguments
		"""
		self.setindexer(indexer)
	
	def setindexer(self,indexer):
		self.indexer = indexer

	def save(self):
		"""
		Auto-save current object
		"""
		sys.stderr.write("Saving %s\n" % str(self))
		self.indexer.save(self.__class__, self)
	
	def load(self):
		"""
		Ask for disk version of current object
		
		Currently dangerous.
		"""
		self.indexer.load(self)

def crudMaker(obj):
	for field in obj.crudAttributes:
		if field.__class__ == tuple:
			""" Assume we have an 'object' with a setter """
			obj.__getattribute__(field[1])()
		elif obj.__getattribute__(field).__class__ in [str,int,float]:
			""" It's easy to handle strings, ints, and floats """
			input = takeInput('Please enter field "'+field+'":')
			# Cool hack: preserve the class type:
			obj.__setattr__(field,obj.__getattribute__(field).__class__(input))
		elif obj.__getattribute__(field).__class__ == list:
			""" List of strings? Use an object instead please """
			while True:
				input = takeInput('Add another item to "'+field+'" (! to stop):')
				if input == '!': break
				else : obj.__getattribute__(field).append(input)
		else:
			""" WTF did you try to feed me? """
			sys.stderr.write("No match for object %s\n" % field)
