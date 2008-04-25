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
from brewobject import BrewObject
from util import *

class Recipe(BrewObject):
	"""
	#########################################################################
	#			Author: Reuben Otero				#
	#			Created: March 26, 2008				#
	#			Modified: April 10, 2008			#
	#-----------------------------------------------------------------------#
	#			Class: Recipe					#
	#	Creates the Recipe object that holds the recipe name,  		#
	#	style, batch size, boil time; recipe ingredients; 		#
	#	recipe procedures.  Class wndRecipe.py subclasses here.		#
	#-----------------------------------------------------------------------#
	#			Sub-Class: Procedure				#
	#	Procedure is called when a new procedure is created in		#
	#	wndRecipe.py. An object is created that stores name		#
	#	description, timing_delta, time_unit of that new procedure.	#
	#	Returns the object and stores in a list called Procedure	#
	#	stored in the Recipe object.					#
	#-----------------------------------------------------------------------#
	#			Sub-Class: Ingredient				#
	#	Ingredient is called when a new ingredient was created		#
	#	during begining testing phases of brewers kit application.	#
	#	Returns a generic Ingredient object.				#
	#-----------------------------------------------------------------------#
	#		Support Classes:					#
	#	Imports from brewobject.py					#
	#	Imports util.py							#
	#									#
	#-----------------------------------------------------------------------#
	"""
	
	#global variables
	name = ""
	style = ""
	batch_size = ""
	boil_time = ""

	crudAttributes = []
	
	def __init__(self,indexer):
		#self.crudAttributes = ['name','style', 'batch_size', 'boil_time',					  					('ingredients', 'txt_add_ingredient'),('steps', 'txt_add_step')]]	

		#RecipeIngredients is a list to hold new ingredient objects created from the Ingredient class
		#Procedures is a list to hold new procedure objects created in Procedure class.
		self.RecipeIngredients = []
		self.Procedures = []
		super(Recipe, self).__init__(indexer)

	def swapRecipeObjects(self, RecipeObject):
		"""
		Swap the two Recipe object attributes. wndRecipe & Brew.py sub-class this constructor
		"""

		self.name = RecipeObject.name
		self.style = RecipeObject.style
		self.batch_size = RecipeObject.batch_size
		self.boil_time = RecipeObject.boil_time
		self.RecipeIngredients = RecipeObject.RecipeIngredients
		self.Procedures = RecipeObject.Procedures
		
	def txt_add_step(self):
		
		while True:
			input = takeInput('Name a step (! to stop): ')
			if input == '!': break
			else:
				description = takeInput('Description: ')
				while True:
					unit = takeInput('Unit of time after start (hr,min,day,month,year): ')
					if unit in ['hr','min','day','month','year']: break
				timing_delta = takeInput('How long after start: ')
				self.steps.append(Procedure(name,description,timing_delta,unit))
			print 'break'

	def Add_procedure(self, name, time, description, unit):
		"""
		Method to add procedures to New Recipe
		Function takes 4 parameters for procedures: Name of Procedure, Time Delta(time between last procedure and
		this next), Time Delta unit, Procedure description.
		Stores the 4 variables into an object by calling the sub-class Procedure(). Stores Procedure object 
		into the new Recipe object list variable Procedures.
		"""
		procedure = Procedure(name, time, description, unit)
		self.Procedures.append(procedure)

	def Delete_Procedure(self, n, d):

		for i in self.Procedures:
			if i.name == n:
				if i.description == d:
					print self.Procedures
					self.Procedures.remove(i)
					print self.Procedures
	
	def txt_add_ingredient(self):
		""" 
		Method for testing in terminal window
		For actual method use for appliction see 
		Add_ingredient(self, igrdName, igrdType, igrdAmmount, igrdUnit)
		"""
		while True:
			name = takeInput('Enter an ingredient name (! to stop): ')
			if name == '!': break
			else:
				amount = takeInput('Amount: ')
				unit = takeInput('Unit: ')
				self.ingredients.append(Ingredient(name,amount,unit))

	def Add_ingredient(self, NewIngredientobj):
		"""
		Method recieves an Ingredient object created in the Ingredient.py class file.  
		Stores the object ingredient in the new Recipe ojbects RecipeIngredients list.
		"""
		self.RecipeIngredients.append(NewIngredientobj)
		print 'Ingredient List =', self.RecipeIngredients

	def Delete_ingredient(self, NewIngredientobj):
		"""
		Method recieves an Ingredient object created in the Ingredient.py class file.  
		Deletes the object ingredient in the new Recipe ojbects RecipeIngredients list.
		"""
		print 'Ingredient List =', self.RecipeIngredients
		self.RecipeIngredients.remove(NewIngredientobj)
		print 'Ingredient List =', self.RecipeIngredients

class Procedure(object):
	"""
	Procedure class creates an object to store the information about the single procedure.
	"""
	name = ""
	description = ""
	timing_delta = ""
	time_unit = ""

	def __init__(self, name, time, description, unit):
		self.name = name
		self.description = description
		self.timing_delta = time
		self.time_unit = unit


class Ingredient():
	"""
	Temporary class for testing in early development stages of this application
	"""
	Item = ""
	Type = ""
	Amout = ""
	Unit = ""

	def __init__(self):
		self.Item = 'Booby'
		self.Type = 'Tittie'
		self.Amount = 'DD'
		self.Unit = 'All of it'
	
	def run(self):
		return self

	def __str__(self):
		return self.name+" "+str(self.amount)+" "+self.unit
