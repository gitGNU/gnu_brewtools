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

class wndEditRecipe:

#Global Varialbles
	Ammountlbl = ""
	NewRecipe = None

	"""
	create indexer to communicate with recipe.py
	self.'NAME' = Indexer()----creates an indexer
	"""
	def __init__(self):
		"""
		
		"""
		self.gladefile = 'gui/recipe.glade'
		self.index = Indexer()
		self.EditRecipe = self.indexer.get(Recipe, 'George')

	def run(self):
		self.wTree = gtk.glade.XML(self.gladefile, 'wndRecipe')

		#dictionary of Handlers for events in EditRecipe GUI window
		#including the method function to support that handle
	
		# dic = {"Button Handler Name": sef.CorresondingFunctionTitle}
		dic = { #"wndRecipe_close_cb" : self.ObjectDelete,
			"btnFinish_click_cb" : self.lookAtFields,
			"btnCancelForm_click_cb" : self.Exit,
			"btnClearForm_click_cb" : self.clearAllFields,
			"btnEdit_Ingredients_clicked_cb" : self.Ingredients,
			"btnEditProcedures_clicked_cb" : self.Procedures,
			#"wndRecipe_destroy_cb" : self.Exit,
			}
		
		#send dictionary of hanles to GUI
		self.wTree.signal_autoconnect(dic)
		
		#set window GUI for Recipe and open
		self.wind = self.wTree.get_widget('wndRecipe')
		self.setTrees(self)
		self.PopulateWindow(self)
		self.wind.show_now()
		#return self.NewRecipe

	def setTrees(self, callback):

		#create a tree list to hold ingredients
		self.treRecipe_Ingredients = self.wTree.get_widget('treRecipe_Ingredients')
		self.Recipe_Ingredient_List = setupList(self.treRecipe_Ingredients, ['Name','Type', 'Amount'], (str,str,str))
		self.treRecipe_Procedures = self.wTree.get_widget('treRecipe_Procedures')
		self.Recipe_Procedures_List = setupList(self.treRecipe_Procedures, ['Name', 'Time'], (str,str,))
	
	def PopulateWindow(self, callback):
		"""
		Populate all the fields of the Recipe.
		"""
		self.wTree.get_widget('txtRecipeName').set_text(self.EditRecipe.name)
		self.wTree.get_widget('txtRecipeStyle').set_text(self.EditRecipe.style)
		self.wTree.get_widget('txtBatchSize').set_text(self.EditRecipe.batch_size)
		self.wTree.get_widget('txtBoilTime').set_text(self.EditRecipe.boil_time)

		for i in self.EditRecipe.RecipeIngredients:
			self.Recipe_Ingredient_List.append([i.name, i.__class__.__name__, "%s %s" % (i.recipeAmount, i.stockUnit)])
		print 'Ingredients are populated'
		

	def Procedures(self, callback):
		"""
		Call Procedures() sub-class. 
		"""
		#call Procedures class
		self.procedure = ProcedureWindow(self.TempNewRecipe)
		self.procedure.run()
		
		print 'Procedures are added to List in window'

	def Ingredients(self, callback):
		
		self.ingredients = IngredientWindow(self.TempNewRecipe)
		self.ingredients.run()
		
		for i in self.TempNewRecipe.RecipeIngredients:
			self.Recipe_Ingredient_List.append([i.name, i.__class__.__name__, "%s %s" % (i.recipeAmount, i.stockUnit)])
		print 'Ingredients are added to List in window'

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

		self.NewRecipe = self.indexer.get(Recipe, self.TempNewRecipe.name)
		self.NewRecipe.swapRecipeObjects(self.TempNewRecipe)

		self.Exit()

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
		

		print 'reach clear all fields'
	
	def ObjectDelete(self, callback = None):
		"""
		Delete Recipe Object
		"""
		self.indexer.deleteObject(Recipe, 'New Recipe')
		self.TempNewRecipe = None
		print 'Object Deleted'

	def Exit(self, callback = None):
		"""
		Function to handle quit
		"""
		self.ObjectDelete()
		self.wind.destroy()
		print 'exit Recipe'
