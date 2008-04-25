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
import pickle, os
import sys

class Indexer(object):
	"""
	Manage objects created in such a way that they can
	automagically be saved and retrieved from disk.
	"""

	objects = {}
	"""
	Object Jar
	
	This is a double dictionary, in theory. It stores objects in the format of objects[objType][objName]. Thus objects[Recipe]['15B'] is the Recipe object named '15B'.
	"""
	objectNames = []

	def encodeName(self,objName,objClass):
		"""
		encodeName

		name: Name of the file to encode (something like the prefix)

		This function is to nicen up the names of files (eventually) from the r.<class 'recipe.Recipe'>.brw format to something that doesn't have brackets, quotes, and spaces.
		"""
		return "%s.%s" % (objName, objClass.__name__)

	def __init__(self):
		self.objectNames = [] # not sure if I'm using this anymore?
		self.datadir = os.path.expanduser("~")+"/.brewtools" # needs to be settable
		if not os.path.exists(self.datadir):
			os.mkdir(self.datadir)
		self.getIndex()

	def getIndex(self):
		if os.path.exists(self.datadir+'/index.brw'):
			self.objectNames = pickle.load( open( self.datadir+'/index.brw' ) )
		else:
			self.dumpIndex()


	def dumpIndex(self):
		"""
		Save the index off to disk

		TODO: Add empty key filter per checkObjs
		"""
		pickle.dump( self.objectNames, open( self.datadir+'/index.brw', 'w') )

	def checkObjs(self,objClass):
		"""
		Creates keys in the index dictionary for objClass

		This has the potential to put a lot of cruft in our index. It may be worth adding some sort of cleaner to dumpIndex to filter out keys without any children.

		objClass: Class object of desired object
		"""
		if not self.objects.has_key(objClass):
			self.objects[objClass] = {}
	
	def requestNew(self,objClass,objName,**kwargs):
		"""
		Create a new object instance
		
		objClass: Class object of desired object
		objName: Reference name for object in index
		**kwargs: Optional named keywords to the __init__

		Example of using **kwargs available in ingredients:
		grain = indexer.requestNew(Grain, 'grain', name='somename', efficiency=5.5)
		"""
		self.checkObjs(objClass)
		self.objects[objClass][objName] = objClass(self,**kwargs) # now that's just fancy
		self.objectNames.append((objClass,objName))
		self.dumpIndex() # We have an object, save the information
		self.save(objClass,objName)
		return self.objects[objClass][objName]
	
	def get(self,objClass,objName,**kwargs):
		"""
		Return object from cache or jar
		
		Dirty hack: If an object is given, gracefully find a key to match or provide a new object.
		"""
		# if self.objects.has_key # Check for key in the index
		self.checkObjs(objClass)
		if self.objects.has_key(objClass) and self.objects[objClass].has_key(objName):
			sys.stderr.write("Already have (%s, %s). Returning...\n" % (str(objClass),objName))
			object = self.objects[objClass][objName]
		elif self.objectNames.count( (objClass, objName) ):
			sys.stderr.write("(%s, %s) on disk. Loading...\n" % (str(objClass),objName))
			self.load(objClass,objName)
			object = self.objects[objClass][objName]
		else:
			sys.stderr.write("(%s, %s) does not exist. Creating...\n" % (str(objClass),objName))
			object = self.requestNew(objClass, objName,**kwargs)
		return object
	
	def getAll(self, objClass):
		"""
		Return list of all objects with class objClass
		"""
		self.getIndex()
		objects = []
		for i in self.objectNames:
			if i[0] == objClass:
				objects.append(self.get(objClass, i[1]))
		return objects

	def deleteObject(self, objClass, objName):
		"""
		Remove object from datastore.

		This is actually somewhat complicated and possibly somewhat false since Python uses garbage collection.
		"""
		self.checkObjs(objClass)
		self.objects[objClass][objName] = None
		self.objects[objClass].pop(objName)
		try:
			self.objectNames.remove( (objClass, objName) )
		except: print "Couldn't remove (%s, %s)" % (objClass, objName)
		self.dumpIndex()
		os.unlink("%s/%s.brw" % (self.datadir, self.encodeName(objName, objClass)))

	def save(self,objClass,objName):
		"""Put an object in a pickle jar"""
		if objName.__class__ != str: objName = self.lookupByObj(objClass,objName)
		if not self.objects[objClass].has_key(objName): raise Exception("Object mising")
		pickle.dump( self.objects[objClass][objName], open( self.datadir+'/' + self.encodeName(objName, objClass) +".brw", "w" ) )
	
	def load(self,objClass,objName):
		"""
		Get an object out of the pickle jar. Ought not be called directly.
		
		objName: string name of index key
		"""
		self.checkObjs(objClass)
		self.objects[objClass][objName] = pickle.load( open( self.datadir+'/' + self.encodeName(objName, objClass)+".brw" ) )
	
	def saveAll(self):
		"""
		Write all objects to disk
		"""
		map(lambda x: self.save(x[0]), self.objects.iterkeys())
		# [self.save(x[0]) for x in self.objects.iterkeys()]
	
	def lookupByObj(self,objClass,obj):
		"""
		Dirty hack to get the first key out of objects for a given object
		
		obj: any object that IS in the index
		"""
		
		d = dict((v,k) for k,v in self.objects[objClass].items())
		if d.has_key(obj): return d[obj]
		else: return None
