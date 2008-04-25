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
"""
Utils

Any odd functions needed in multiple modules
"""

import gtk
import ingredient


RECIPE_INDEX = 0
def Recipe_Get_New_index():
	++RECIPE_INDEX
	return RECIPE_INDEX

takeInput = lambda text: raw_input(text)
ti = takeInput

def dictToList(dict):
	"""
	Utility function to convert dict to a list object
	
	dict: any dict object
	"""
	return map(lambda x: x[0], dict.iterkeys())
	# [x[0] for x in dict.iterkeys()]

def setupList(tree, colNames, colTypes):
	def addListColumn(tree, title, columnId):
		col = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
		col.set_resizeable = False
		col.set_sort_column_id(columnId)
		tree.append_column(col)
	valueList = gtk.ListStore(*colTypes)
	tree.set_model(valueList)
	for i in xrange(colNames.__len__()): addListColumn(tree, colNames[i], i)
	return valueList

def translateIngredientObjName(type):
	if type == 'Yeast': type = ingredient.Yeast
	elif type == 'Grain': type = ingredient.Grain
	elif type == 'Hops': type = ingredient.Hops
	elif type == 'Adjunct': type = ingredient.Adjunct
	return type

def getSelected(tree):
	selection = None
	try:
		model, selected = tree.get_selection().get_selected()
		selection = model[selected]
	except: pass
	return selection, selected

