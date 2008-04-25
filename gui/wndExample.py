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

from util import *

class ExampleWindow:
	def __init__(self):
		self.gladefile = 'gui/example.glade'
	
	def run(self):
		self.wTree = gtk.glade.XML(self.gladefile, 'wndExample')
		
		dic = {
				"btnDone_clicked_cb" : self.lookAtFields,
				"btnPopulate_clicked_cb": self.populateTree,
				"wndExample_destroy_cb" : self.lookAtFields,
				}
		self.wTree.signal_autoconnect(dic)

		self.wind = self.wTree.get_widget('wndExample')
		self.treExample = self.wTree.get_widget('treExample')
		self.nameList = setupList(self.treExample, ['Name','Title'], (str,str))

		self.populateFields()
		self.wind.run()
		self.wind.destroy()
		return 42

	def populateFields(self):
		firstNameBox = self.wTree.get_widget('txtFirstName')
		lastNameBox = self.wTree.get_widget('txtLastName')
		firstNameBox.set_text('Bob')
		lastNameBox.set_text('Newhart')

	def populateTree(self,callback):
		self.nameList.append(['test1','test2'])
	
	def lookAtFields(self,callback):
		firstNameBox = self.wTree.get_widget('txtFirstName')
		lastNameBox = self.wTree.get_widget('txtLastName')
		print "%s %s" % (firstNameBox.get_text(), lastNameBox.get_text())
		self.wind.destroy()
