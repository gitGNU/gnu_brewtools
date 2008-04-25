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
from wndRecipeIngredients import*

class ProcedureWindow(object):
	
	"""
#########################################################################
#		Sub-Class: ProcedureWindow				#
#	Opens the GUI window to create and store a new			#
#	Procedures into the new Recipe Object. Creates the button	#
#	handlers and has the functions to support them.			#
#-----------------------------------------------------------------------#

	"""
	def __init__(self):
		self.gladefile = 'gui/recipe.glade'

	def run(self, TempNewRecipe, Edit=None):
		self.wTree = gtk.glade.XML(self.gladefile, 'wndAddProcedures')
		#store the new recipe object passed to here
		self.procedures = TempNewRecipe
		#store editing
		self.Editing = Edit

		#dictionary of Handlers for events in procedure GUI window
		#including the method function to support that handle
	
		# dic = {"Button Handler Name": sef.CorresondingFunctionTitle}
		dic = {
			"btnAddProcedures_clicked_cb" : self.AddProcedures,
			"btnDelete_clicked_cb" : self.DeleteProcedures,
			"wndAddProcedures_destory_cb" : self.exit,
			"btnFinish_clicked_cb" : self.exit,
			"btnClearForm_clicked_cb" : self.clearFields,
			}

		self.wTree.signal_autoconnect(dic)
		#send dictionary of hanles to GUI
		
		#set window GUI for Recipe and open
		self.wind = self.wTree.get_widget('wndAddProcedures')

		self.setTrees()
		self.PopulateTrees()

		self.wind.run()

	def setTrees(self, callback=None):
		"""
		creates a tree list to hold all New Recipe Procedures
		"""
		
		self.tre_Procedure = self.wTree.get_widget('tre_Procedure')
		self.tre_Procedures_List = setupList(self.tre_Procedure, ['Name', 'Time', 'Description'], (str,str,str))

	def PopulateTrees(self, callback=None):
		"""
		Populate the procedures if any stored
		"""

		for i in self.procedures.Procedures:
			self.tre_Procedures_List.append([i.name, "%s %s" % (i.timing_delta, i.time_unit), i.description])


	def AddProcedures(self, callback):
		
		"""
		Function that supports the Add Procedure button.
		Function stores each single procedure created into 
		a procedure object that is stored in a list of procedeures
		stored in the new Recipe object
		"""

		#create variable to hold text input fro GUI text boxes		
		ProcedureName = self.wTree.get_widget('Name_text')
		Time = self.wTree.get_widget('Time_txt')
		Description = self.wTree.get_widget('Description_txt')
		Unit = self.wTree.get_widget('TimeUnit').get_active_text()		

		#call the Add_procedure function in recipe.py
		#creates an object for each single procedure
		#then stores them in a procedures list
		self.procedures.Add_procedure(ProcedureName.get_text(), Time.get_text(), Description.get_text(), Unit)
		self.tre_Procedures_List.insert(0,[ProcedureName.get_text(), "%s %s" % (Time.get_text(),Unit), Description.get_text()])
		
		#test purposes to see if inputs are correct and stored
		print 'reach look at fields procedure'
		print ProcedureName.get_text(), Description.get_text(), Time.get_text(), Unit
		
		self.clearFields(self)

	def DeleteProcedures(self, callback):
		"""
		Function that supports the delete procedure button.
		Deletes the selected procedure in the Recipe procedure tree.
		"""
		
		#try:
		Model, selected = self.tre_Procedure.get_selection().get_selected()
		selection = Model[selected]

		#retreive object to delete from the ingredient list
		name = selection[0]
		description = selection[2]

		self.procedures.Delete_Procedure(name, description)
		self.tre_Procedures_List.remove(selected)

		print 'Reach Delete Procedures'
		print "%s" % (selected)
		#except:
		#print ' no selection try again'

	def clearFields(self, callback):
		"""
		Function that supports the Clear All Procedures Form button.
		Clears all text fields in the Procedures Form
		"""
		print 'Reach Clear All Fields for Procedure'
		self.wTree.get_widget('Name_text').set_text('')
		self.wTree.get_widget('Description_txt').set_text('')
		self.wTree.get_widget('Time_txt').set_text('')
		self.wTree.get_widget('TimeUnit').set_active(-1)		

	def exit(self, callback):
		"""
		Function to handle quit
		"""
		self.wind.destroy()
		print 'exit procedure'
