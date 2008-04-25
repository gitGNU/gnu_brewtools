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

import sys
import wndFormulator, wndExample, wndRecipe, wndIngredientAdd
from util import *
from obj_manager import Indexer
import recipe, brew, ingredient

class Gui:
	def __init__(self):
		self.indexer = Indexer()
		self.gladefile = 'gui/main.glade'
		self.wTree = gtk.glade.XML(self.gladefile, "wndMain")
		dic = {
				"mnuRecipeNew_activate_cb": self.newRecipe,
				"btnDasFormulator_clicked_cb" : self.dasFormulator,
				"mnuExample_activate_cb" : self.exampleMenu,
				"mnuIngredientNew_activate_cb": self.newIngredient,
				"wndMain_destroy_cb" : gtk.main_quit,
				"mnuPrintSelected_activate_cb": self.printSelected,
				"mnuRecipeEdit_activate_cb": self.editRecipe,
				"mnuIngredientEdit_activate_cb": self.editIngredient,
				"mnuRecipeDelete_activate_cb": self.deleteRecipe,
				"mnuIngredientDelete_activate_cb": self.deleteIngredient,
				"wndMain_activate_focus_cb": self.populateTrees,
				}
		self.wTree.signal_autoconnect(dic)

		self.setupTrees()
	
	def deleteRecipe(self,callback):
		sys.stderr.write('delete\n')
		selected, selectedIter = getSelected(self.treRecipes)
		if selected: self.indexer.deleteObject(recipe.Recipe, selected[0])
		self.populateTrees()

	def deleteIngredient(self,callback):
		selected, selectedIter = getSelected(self.treIngredients)
		type = translateIngredientObjName(selected[2])
		if selected: self.indexer.deleteObject(type, selected[0])
		self.populateTrees()

	def editRecipe(self, callback):
		selected, selectedIter = getSelected(self.treRecipes)
		if selected:
			obj = self.indexer.get(recipe.Recipe, selected[0])
			self.newRecipe(None, obj)

		else:
			sys.stderr.write("no row selected\n")

	def editIngredient(self, callback):
		selected, selectedIter = getSelected(self.treIngredients)
		if selected:
			selectedIngredient = selected[0]
			type = selected[2]
			type = translateIngredientObjName(type)
			obj = self.indexer.get(type, selectedIngredient)
			print "%s %s %s" % (selectedIngredient, type, obj)
		else:
			sys.stderr.write("no row selected\n")

	def printSelected(self, callback):
		selection, selectedIter = getSelected(self.treIngredients)
		if selection: print selection[0]
		else:
			sys.stderr.write("no row selected\n")
 

	def setupTrees(self):
		self.treRecipes = self.wTree.get_widget('treRecipes')
		self.recipeList = setupList(self.treRecipes, ['Name','Style'], (str,str))


		self.treIngredients = self.wTree.get_widget('treIngredients')
		self.ingredientList = setupList(self.treIngredients, ['Name','Stock','Type'], (str,str,str))

		self.populateTrees()

	def populateTrees(self,callback=None,someobj=None):
		recipes = self.indexer.getAll(recipe.Recipe)
		self.recipeList.clear()
		for r in recipes:
			self.recipeList.append([r.name,r.style])


		ingredients = self.indexer.getAll(ingredient.Ingredient)
		grains = self.indexer.getAll(ingredient.Grain)
		hops = self.indexer.getAll(ingredient.Hops)
		adjuncts = self.indexer.getAll(ingredient.Adjunct)
		yeast = self.indexer.getAll(ingredient.Yeast)
		allIngredients = ingredients + grains + hops + adjuncts + yeast
		self.ingredientList.clear()
		for i in allIngredients:
			self.ingredientList.append([i.name,"%s %s" % (i.stock, i.stockUnit),i.__class__.__name__])

		# handle a listview
		# self.recipeView = self.wTree.get_widget("treRecipes")
		# column = gtk.TreeViewColumn('Recipe', gtk.CellRendererText())
		# column.set_resizable(False)		
		# column.set_sort_column_id('Recipe')
		# self.recipeView.append_column(column)
	
	def newRecipe(self,callback,obj=None):
		print "%s clicked" % str(callback)
		print obj
		nrecipe = wndRecipe.RecipeWindow()
		result = nrecipe.run(obj)
		self.populateTrees()

	def newIngredient(self,callback,obj=None):
		print "%s clicked" % str(callback)
		nrecipe = wndIngredientAdd.IngredientAddWindow()
		nrecipe.run(obj)
		self.populateTrees()

	def exampleMenu(self,callback):
		print "%s clicked" % str(callback)
		example = wndExample.ExampleWindow()
		result = example.run()
		self.populateTrees()

	def quit(self,callback):
		gtk.main_quit()
	
	def dasFormulator(self,callback):
		f = wndFormulator.Formulator()
		f.run()
		self.populateTrees()

def runIt():
	win = Gui()
	gtk.main()
