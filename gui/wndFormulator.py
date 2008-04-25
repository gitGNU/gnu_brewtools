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
import gtk, gtk.glade, sys
from obj_manager import *
import ingredient, brew, recipe, util, formulator

class Formulator:
	def __init__(self):
		self.gladefile = 'gui/formulator.glade'
		self.indexer = Indexer()
	
	def run(self):
		self.data()
		self.wTree = gtk.glade.XML(self.gladefile, 'assFormulator')
		self.wind = self.wTree.get_widget('assFormulator')

		dic = {
				"assFormulator_apply_cb" : self.apply,
				"assFormulator_cancel_cb" : self.cancel,
				"assFormulator_close_cb" : self.cancel,
				"cboStyle_changed_cb": self.onStyleChange,
				"btnAddGrain_clicked_cb": self.addToSelectedGrains,
				"btnRemoveGrain_clicked_cb": self.removeFromSelectedGrains,
				"treGrainRefine_row_activated_cb": self.refineSelected,
				"treGrainRefine_row_activated_cb": self.refineChange,
				}
		self.wTree.signal_autoconnect(dic)

		self.setupLists()

		self.hscGrainPerc = self.wTree.get_widget('hscGrainPerc')
		
		n_pages = self.wind.get_n_pages()
		for i in xrange(n_pages):
			self.wind.set_page_complete(self.wind.get_nth_page(i), True)
		
		self.wind.show_now()
	
	def data(self):
		indexer = Indexer()
	
	def apply(self, callback):
		print "Apply"
		self.wind.destroy()

	def cancel(self, callback):
		print "Cancel"
		self.wind.destroy()

	def onStyleChange(self,callback):
		sys.stderr.write("style changed")
		styleName = self.wTree.get_widget('cboStyle').get_active_text() #'Porter' # cboStyle.get_text()
		self.styleProfile = self.indexer.get(formulator.StyleProfile, styleName)
		self.formultaor = formulator.Formulator(self.styleProfile)
		self.populateStyleGrain()
	
	def setupLists(self):
		sys.stderr.write("setupLists\n")
		self.treAllGrains = self.wTree.get_widget('treAllGrains')
		self.treSelGrains = self.wTree.get_widget('treSelGrains')
		self.treGrainRefine = self.wTree.get_widget('treGrainRefine')

		self.allGrainList = util.setupList(self.treAllGrains, ['Name','Percentage'], (str,str))
		self.selGrainList = util.setupList(self.treSelGrains, ['Name','Percentage'], (str,str))
		self.grainRefineList = util.setupList(self.treGrainRefine, ['Name','Percentage'], (str,str))

	def populateStyleGrain(self):
		self.allGrainList.clear()
		self.selGrainList.clear()
		for i in self.styleProfile.grains: self.allGrainList.append([i['grain'].name,i['percentage']])
	
	def removeFromSelectedGrains(self,callback):
		selection, selectedIter = util.getSelected(self.treSelGrains)
		self.allGrainList.append([selection[0], selection[1]])
		grainiter = self.grainRefineList.get_iter(0)
		while (grainiter):
			#sys.stderr.write("%s, %s\n" % (selection[0], grainiter[0]))
			grain = self.grainRefineList[grainiter]
			print grain
			if grain[0] == selection[0]:
				self.grainRefineList.remove(grainiter)
			grainiter = self.grainRefineList.iter_next(grainiter)
		self.selGrainList.remove(selectedIter)

	def addToSelectedGrains(self,callback):
		selection, selectedIter = util.getSelected(self.treAllGrains)
		self.selGrainList.append([selection[0], selection[1]])
		self.grainRefineList.append([selection[0], selection[1]])
		self.allGrainList.remove(selectedIter)

	def onGrainFineTuneChange(self,callback):
		scroller = self.wTree.get_widget('hscPercSlider')
	
	def refineSelected(self,callback):
		sys.stderr.write("selected grain\n")
		selection, selectedIter = util.getSelected(self.treGrainRefine)
		percentage = selection[1]
		self.hscGrainPerc.set_value(percentage)
	
	def refineChange(self,callback):
		sys.stderr.write("changing value\n")
		selection, selectedIter = util.getSelected(self.treGrainRefine)
		percentage = self.hscGrainPerc.get_value()
		selection[1] = percentage
