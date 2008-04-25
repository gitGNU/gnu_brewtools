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

import pygtk
pygtk.require("2.0")
import gtk, gtk.glade

from recipe import*
from obj_manager import*
from util import*
from wndRecipeProcedure import*


class RecipeWindow:
	"""
	#########################################################################
	#			Author: Reuben Otero				#
	#			Created: March 26, 2008				#
	#			Modified: April 10, 2008			#
	#-----------------------------------------------------------------------#
	#		Class: RecipeWindow					#
	#	Opens the GUI window to create and store a new			#
	#	Recipe into the application. Creates the button			#
	#	handlers and has the functions to support them.			#
	#-----------------------------------------------------------------------#
	#		Sub-Class: ProcedureWindow				#
	#	Opens the GUI window to create and store a new			#
	#	Procedures into the new Recipe Object. Creates the button	#
	#	handlers and has the functions to support them.			#
	#-----------------------------------------------------------------------#
	#		Support Classes:					#
	#	Imports recipe.py						#
	#		creates and stores new recipe information		#
	#	Imports obj_manager						#
	#		class file to handle all objects created		#
	#		sub-classed with Indexer.py				#
	#-----------------------------------------------------------------------#
	#		Indexer:						#
	#	Uses Indexer class sub-class through ojb_manager		#
	#	Uses include createing and destroying objects			#
	#									#
	#	'Create an object'						#
	#	Variable = self.indexer.get(ObjectClass, 'NameofObject)		#
	#									#
	#	'Delete an oject'						#
	#		Variable = None						#
	#		self.indexer.deleteObject(ObjectClass, 'NameofObject')	#
	#-----------------------------------------------------------------------#
	"""
	
	#Global Varialbles
	Ammountlbl = ""
	NewRecipe = None

	"""
	create indexer to communicate with recipe.py
	self.'NAME' = Indexer()----creates an indexer
	"""
	def __init__(self):
		"""
		Constructor saves the recipe.glade file
		Creates an indexer to use for creating and saving a recipe object
		"""
		self.gladefile = 'gui/recipe.glade'
		#Global Varialbles
		#IndexRecipe may be used to store an index number for Recipe objects
		self.IndexRecipe = Recipe_Get_New_index()

		#create new Recipe object to hold recipe. Unique key is name of
		#object. Object is created as soon as the window opens
		#Currently just using the name 'Test Recipe' input for name of
		#recipe by user. Possibly will change to use an automated system So only
		#creates one recipe object that is reuse every time the program is ran.
		self.indexer = Indexer()


	def run(self, Edit):
		self.wTree = gtk.glade.XML(self.gladefile, 'wndRecipe')

		#dictionary of Handlers for events in Recipe GUI window
		#including the method function to support that handle
	
		# dic = {"Button Handler Name": sef.CorresondingFunctionTitle}
		dic = { #"wndRecipe_close_cb" : self.ObjectDelete,
			"btnFinish_click_cb" : self.lookAtFields,
			"btnCancelForm_click_cb" : self.Exit,
			"btnClearForm_click_cb" : self.clearAllFields,
			"btnAddIngrd_clicked_cb" : self.Ingredients,
			"btnProcedures_clicked_cb" : self.Procedures,
			#"btnEdit_Ingredients_clicked_cb" : self.EditIngredients,
			#"btnEditProcedures_clicked_cb" : self.EditProcedures,
			#"wndRecipe_destroy_cb" : self.Exit,
			}
		
		#send dictionary of hanles to GUI
		self.wTree.signal_autoconnect(dic)

		#set window GUI for Recipe and open
		self.wind = self.wTree.get_widget('wndRecipe')
		self.setTrees()

		#check to see if an ojbect was sent to be edit
		if Edit:
			self.TempNewRecipe = Edit
			self.Editing = True
			self.PopulateRecipe()
			self.PopulateTrees(True, True)
			print 'Recieve Recipe Object to edit'
		else:
			self.TempNewRecipe = self.indexer.get(Recipe, 'New Recipe')
			self.Editing = False
			print 'No Recipe Object passed to edit'
		
		self.wind.show_now()

#-----------------------------------------------------------------------------------------------------------------------------
#Function to support the trees for ingredients and procedures
	def setTrees(self, callback=None):

		#create a tree list to hold ingredients
		self.treRecipe_Ingredients = self.wTree.get_widget('treRecipe_Ingredients')
		self.Recipe_Ingredient_List = setupList(self.treRecipe_Ingredients, ['Name','Type', 'Amount'], (str,str,str))
		self.treRecipe_Procedures = self.wTree.get_widget('treRecipe_Procedures')
		self.Recipe_Procedures_List = setupList(self.treRecipe_Procedures, ['Name', 'Time'], (str,str,))

	def PopulateRecipe(self):
		"""
		Populate all the fields of the Recipe.
		"""
		self.wTree.get_widget('txtRecipeName').set_text(self.TempNewRecipe.name)
		self.wTree.get_widget('txtRecipeStyle').set_text(self.TempNewRecipe.style)
		self.wTree.get_widget('txtBatchSize').set_text(self.TempNewRecipe.batch_size)
		self.wTree.get_widget('txtBoilTime').set_text(self.TempNewRecipe.boil_time)
		self.PopulateTrees(True, True)

	def PopulateTrees(self, Ingd, Proc):

		if Proc:
			self.Recipe_Procedures_List.clear()
			for i in self.TempNewRecipe.Procedures:
				self.Recipe_Procedures_List.insert(0,[i.name, "%s %s" % (i.timing_delta, i.time_unit)])	
		if Ingd:
			self.Recipe_Ingredient_List.clear()
			for i in self.TempNewRecipe.RecipeIngredients:
				self.Recipe_Ingredient_List.append([i.name, i.__class__.__name__, 
										"%s %s" % (i.recipeAmount, i.stockUnit)])

#-----------------------------------------------------------------------------------------------------------------------------
#Functions to support the new recipe window when creating a new window.
	def Procedures(self, callback):
		"""
		Call Procedures() sub-class. 
		"""
		#call Procedures class
		self.procedure = ProcedureWindow()
		
		if self.Editing:
			self.procedure.run(self.TempNewRecipe, self.Editing)
		else:
			self.procedure.run(self.TempNewRecipe)
		#re-populate the procedure tree
		self.PopulateTrees(False, True)

	def Ingredients(self, callback):
		"""
		Call the Ingredient class to handle adding ingredients to the new recipe
		Call the Ingredient class to handle edits to the ingredients stored in new recipe
		If Editing send the new recipe object and True to the Ingredient class
		Else just send the new recipe object
		"""
		
		self.ingredients = IngredientWindow()
		if self.Editing:
			self.ingredients.run(self.TempNewRecipe, self.Editing)
		else:
			self.ingredients.run(self.TempNewRecipe)
		
		#re-populate the ingredients tree
		self.PopulateTrees(True, False)
		
	def lookAtFields(self,callback):
		
		"""
		Function that supports the Finish button.
		Function stores and creaates new Recipe Object using The indexer
		created in the constructor.
		---------------------------------------------------------------
		See Indexer: above for notes
	
		Use a variable to store index object
		Manipulate object variables or use functions as
			Variable = self.indeser.get.........
			Variable.ObjectClassVariable = such and such
			Variable.ObjectClassFunction()
		"""
		#create variable to hold text input fro GUI text boxes		
		RecipeNameBox = self.wTree.get_widget('txtRecipeName')
		RecipeStyleBox = self.wTree.get_widget('txtRecipeStyle')
		BatchSize = self.wTree.get_widget('txtBatchSize')
		BoilTime = self.wTree.get_widget('txtBoilTime')
		#ListofIngredients = self.Recipe_Ingredient_List.get_selection()

		#Set Created Recipe Object variables to inputs
		self.TempNewRecipe.name = RecipeNameBox.get_text()
		self.TempNewRecipe.style = RecipeStyleBox.get_text()
		self.TempNewRecipe.batch_size = BatchSize.get_text()
		self.TempNewRecipe.boil_time = BoilTime.get_text()
		
		#test purposes to see if function is read and used
		print 'reach look at fields'
		#test purposes to see if inputs are correct and stored
		print self.TempNewRecipe.name, self.TempNewRecipe.style, self.TempNewRecipe.batch_size, self.TempNewRecipe.boil_time
		

		#Create new recipe object to store the new recipe.
		#Delete TempNewRecipe. For a new unique object is created
		#to store the new recipe. 
		#If editing an object do not create a new object and bypass this code

		if self.Editing:
			print 'Not Editing No need to create new recipe object'
		else:
			self.NewRecipe = self.indexer.get(Recipe, self.TempNewRecipe.name)
			self.NewRecipe.swapRecipeObjects(self.TempNewRecipe)

		self.Exit()

#-----------------------------------------------------------------------------------------------------------------------------
#These functions work for both new recipe and edit recipe functionality.
	def clearAllFields(self, callback):
		"""
		Function that supports the Clear All Recipe Form button.
		Clears all text fields in the Recipe Form
		"""
		self.wTree.get_widget('txtRecipeName').set_text('')
		self.wTree.get_widget('txtRecipeStyle').set_text('')
		self.wTree.get_widget('txtBatchSize').set_text('')
		self.wTree.get_widget('txtBoilTime').set_text('')
		#clear the ingredient list tree		
		self.Recipe_Ingredient_List.clear()
		self.Recipe_Procedures_List.clear()

		for i in self.TempNewRecipe.RecipeIngredients:
			self.TempNewRecipe.RecipeIngredients.Remove(i)

		for i in self.TempNewRecipe.Procedures:
			self.TempNewRecipe.Procedures.Remove(i)
		

		print 'reach clear all fields'
	
	def ObjectDelete(self, callback = None):
		"""
		Delete Recipe Object
		"""
		if self.Editing:
			print 'editing an object no deletion necessary'
		else:
			self.indexer.deleteObject(Recipe, 'New Recipe')
			self.TempNewRecipe = None
			print 'Object TempNewRecipe Deleted'

	def Exit(self, callback = None):
		"""
		Function to handle quit
		"""
		self.ObjectDelete()
		self.wind.destroy()
		#return self.TempNewRecipe
		print 'exit Recipe'
