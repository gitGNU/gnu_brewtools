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
from wndIngredientAdd import*
import ingredient

class IngredientWindow(object):
	
	def __init__(self):
		"""
		Stores glade gui file for ingredient dialog window
		creates and stores a indexer for manipulating objects
		"""

		self.gladefile = 'gui/recipe.glade'
		self.indexer = Indexer()

	def run(self, TempNewRecipe, edit = None):
		"""
		Takes a recipe object to store ingredients
		Edits a recipe object if True is passed to edit
		"""

		self.wTree = gtk.glade.XML(self.gladefile, 'wndAddIngredients')
	
		#object to be passed to be worked on
		self.Ingredients = TempNewRecipe
		#Save true or None
		self.Editing = edit

		#dictionary of Handlers for events in procedure GUI window
		#including the method function to support that handle
	
		# dic = {"Button Handler Name": sef.CorresondingFunctionTitle}
		dic = {
			"btnAddIgredient_clicked_cb" : self.AddIngredients,
			"btnDeleteIngredient_clicked_cb" : self.DeleteIngredients,
			"btnNewIngredient_clicked_cb" : self.NewIngredient,
			"ClearForm_button_clicked_cb" : self.clearFields,
			"btnFinishIngredients_clicked_cb" : self.Exit,
			"wndAddIngredients_destroy_cb" : self.Exit,
			}

		self.wTree.signal_autoconnect(dic)
		#send dictionary of hanles to GUI
		
		#set window GUI for Recipe and open
		self.wind = self.wTree.get_widget('wndAddIngredients')
		
		self.setTrees()
		self.PopulateTrees()
		
		self.wind.run()

	def setTrees(self, callback=None):
		"""
		creates a tree list to hold all New Recipe Ingredients
		creates a tree list to hold all New recipe Procedures
		"""
		
		self.tre_Ingredients = self.wTree.get_widget('tre_IngredientsFile')
		self.tre_IngredientsFiles = setupList(self.tre_Ingredients,
						['Ingredient Name', 'Stock', 'Type'], (str,str,str))
		self.tre_Recipe = self.wTree.get_widget('tre_IngredientsRecipe')
		self.tre_IngredientsRecipe = setupList(self.tre_Recipe,
						['Ingredient', 'Amount', 'Type'], (str, str, str))
		
		
	def PopulateTrees(self):
		"""
		Populate all the ingredient objects into the Ingredient Tree view
		Uses a function in object_manager: getall(ObjClass). Returns
		all the objects of that class stored on the system.

		If editing populate the recipe ingredient fields in Reicpe ingredient tree
		"""
	
		self.tre_IngredientsFiles.clear()
		ingredients = self.indexer.getAll(ingredient.Ingredient)
		grains = self.indexer.getAll(ingredient.Grain)
		hops = self.indexer.getAll(ingredient.Hops)
		adjuncts = self.indexer.getAll(ingredient.Adjunct)
		yeast = self.indexer.getAll(ingredient.Yeast)
		allIngredients = ingredients + grains + hops + adjuncts + yeast

		for i in allIngredients:
			self.tre_IngredientsFiles.append([i.name,"%s %s" % (i.stock, i.stockUnit),i.__class__.__name__])

		#if editing populate recipe ingredient tree	
		if self.Editing:
			for i in self.Ingredients.RecipeIngredients:
				self.tre_IngredientsRecipe.append([i.name, 
								"%s %s" % (i.recipeAmount, i.stockUnit), i.__class__.__name__])

	def Finish(self, callback):
		"""
		Function that supports the Finish Button. The variable ingredientList stored
		in self holds all the ingredient objects needing to be saved to the new
		recipe object. Pass the list to the recipe.py file to handle the swap.
		"""
		self.exit()

	def AddIngredients(self, callback):
		
		"""
		Function that supports the add ingredient button.
		Pulls an ingredient from the tree that is populated with
		all ingredients on file. Adds the ingredient selected to the
		Recipe ingredient tree and calls Add_ingredient in recipe.py to store
		"""

		try:
			#select ingredient from tree
			Model, selected = self.tre_Ingredients.get_selection().get_selected()
			selection = Model[selected]
		
			selectedIngredient = selection[0]
			type = selection[2]
			type = translateIngredientObjName(type)
			#create object of ingredient selected
			obj = self.indexer.get(type, selectedIngredient)
			obj.recipeAmount = self.wTree.get_widget('amntEntry').get_text()

			self.tre_IngredientsRecipe.append([selectedIngredient, 
							"%s %s" % (obj.recipeAmount, obj.stockUnit), obj.__class__.__name__])
			#Add to ingredientList list by calling recipe.py
			self.Ingredients.Add_ingredient(obj)

			print 'Reach Add Ingredients'
			print "%s %s %s" % (selectedIngredient, type, obj)
		except:
			print 'No Selection, Try Again!'


	def DeleteIngredients(self, callback):
		"""
		Function that supports the delete ingredient button.
		Deletes the selected ingredient in the Recipe Ingredient tree.
		Finds the object and creates it to delete from the list of ingredients stored in self
		"""
		
		try:
			Model, selected = self.tre_Recipe.get_selection().get_selected()
			selection = Model[selected]

			print selection[0]

			#retreive object to delete from the ingredient list
			selectedIngredient = selection[0]
			type = selection[2]
			type = translateIngredientObjName(type)
			obj = self.indexer.get(type, selectedIngredient)

			self.Ingredients.Delete_ingredient(obj)
			self.tre_IngredientsRecipe.remove(selected)

			print 'Reach Delete Ingredients'
			print "%s %s %s" % (selectedIngredient, type, obj)
		except:
			print ' no selection try again'

	def NewIngredient(self, callback):
		"""
		Function that subclasses the Ingredient.py. Ingredient.py creates
		ingredient objects. Returns the object. Re-populate the ingredients on 
		file. Select that ingredient to add to the recipe list.
		"""

		self.Ingredientobj = IngredientAddWindow()
		self.ingredientobj = self.Ingredientobj.run()
		#re-populate the ingredient list
		self.PopulateTrees()
		
		print 'Reach New Igredient'
	
	def clearFields(self, callback):
		"""
		Function that supports the Clear Form button.
		Clears all tree fields in the Ingredient Recipe Form
		"""
		print 'Reach Clear All Fields for Ingredients for New Recipe'
		#clear the ingredient list tree		
		self.PopulateTrees()
		if self.Editing:
			print 'Editing delete the ingredients you do not want'
		else:
			self.tre_IngredientsRecipe.clear()
		self.wTree.get_widget('amntEntry').set_text('')


	def Exit(self, callback=None):
		"""
		Function to handle quit
		"""
		self.wind.destroy()
		print 'exit Recipe Ingredients'
