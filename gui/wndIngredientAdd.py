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

import ingredient, recipe, brew
from obj_manager import *
from util import *

class IngredientAddWindow:
	tmpIngredient=None
	
	def __init__(self):
		"""
		Contructor for the Ingredient Window
		gets glade file
		creates an instance of hte indexer object for saving hte ingredient that is bing added
		"""

		self.gladefile = 'gui/ingredientAdd.glade'
		self.indexer = Indexer()
		#self.tempNewIngredient = self.indexer.get(Recipe,'New Ingredient')

	def run(self,editObject=None):
		self.wTree = gtk.glade.XML(self.gladefile, 'wndIngredientAdd')
		dic = {"btnSave_clicked_cb" : self.save,"btnCancel_clicked_cb" : self.exit}

		self.wTree.signal_autoconnect(dic)

		self.wind = self.wTree.get_widget('wndIngredientAdd')

		self.wind.run()
		return self.tmpIngredient

	def save(self,callback=None):
		"""
		btnSave supporting function
		tmpIngreident is created to hold the information the End User has entered in the entry boxes
		"""

		print 'made it to the save function'

		#required fields for all ingredients, creating variable to hold the data inputed into thier repective fileds
		nameTemp = self.wTree.get_widget('entName')
		stockTemp = self.wTree.get_widget('entStkAmt')
		stockUnitTemp = self.wTree.get_widget('cmbEntStkUnit')
		#fields associated with the ingredient type Hops
		alphaAcidsTemp = self.wTree.get_widget('entHopAphAcid')
		purposeTemp = self.wTree.get_widget('entPurpose')
		#fields associated with the ingredient type Grain
		yieldGulbTemp = self.wTree.get_widget('entGrainYieldGulb')
		colorSRMTemp = self.wTree.get_widget('entGrainColor')
		efficiencyTemp = self.wTree.get_widget('entGrainEff')
		#fields associated with the ingredient type Adjunct
		descriptionTemp = self.wTree.get_widget('entAdjunctDescription')
		purposeAdjTemp = self.wTree.get_widget('entAdjunctPurpose')
		#fields associated with the ingredient type Yeast
		potentialAlcoholPercentTemp = self.wTree.get_widget('entYeastAlcoholPercent')
		purposeYeastTemp = self.wTree.get_widget('entYeastPurpose')
		pitchingTempTemp = self.wTree.get_widget('entPitchTemp')
		
		cbxTypeActive = self.wTree.get_widget('cbxType')
		cbxTypeFlag = cbxTypeActive.get_active_text()

		cbxStockUnit = self.wTree.get_widget('cbxStkUnit')
		cbxStockUnitFlag = cbxStockUnit.get_active_text()

		print cbxTypeFlag
		print cbxStockUnitFlag

		if cbxTypeFlag == 'Hops':	
			self.tmpIngredient = self.indexer.get(ingredient.Hops,nameTemp.get_text(),name=nameTemp.get_text(),stock=stockTemp.get_text(),stockUnit=cbxStockUnitFlag,alphaAcids=alphaAcidsTemp.get_text(),purpose=purposeTemp.get_text())
		elif cbxTypeFlag == 'Grains':
			self.tmpIngredient = self.indexer.get(ingredient.Grain,nameTemp.get_text(),name=nameTemp.get_text(),stock=stockTemp.get_text(),stockUnit=cbxStockUnitFlag,yieldGUlb=yieldGulbTemp.get_text(),colorSRM=colorSRMTemp.get_text(),efficiencyPerc=efficiencyTemp.get_text())
		elif cbxTypeFlag == 'Adjunct':
			self.tmpIngredient = self.indexer.get(ingredient.Adjunct,nameTemp.get_text(),name=nameTemp.get_text(),stock=stockTemp.get_text(),stockUnit=cbxStockUnitFlag,purposeAdjunct=purposeAdjTemp.get_text(),description=descriptionTemp.get_text())
		elif cbxTypeFlag == 'Yeast':
			self.tmpIngredient = self.indexer.get(ingredient.Yeast,nameTemp.get_text(),name=nameTemp.get_text(),stock=stockTemp.get_text(),stockUnit=cbxStockUnitFlag,potentialAlcoholPer=potentialAlcoholPercentTemp.get_text(),purposeYeast=purposeYeastTemp.get_text(),pitchingTemp=pitchingTempTemp.get_text())

			
		#	print self.tmpIngredient
		"""
		try:
			
			#required fields for all ingredients are captured from thier repective fileds
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,nameTemp,name=nameTemp.get_text())
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,stockTemp,stock=stockTemp.get_text())
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,stockUnitTemp,stockUnit=stockUnitTemp.get_text())
			#fields associated with the ingredient type Hops
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,alphaAcidsTemp,alphaAcidsPerc=alphaAcidsTemp.get_text())
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,purposeTemp,purpose=purposeTemp.get_text())
			#fields associated with the ingredient type Grain
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,yieldGulbTemp,yieldGUlb=yieldGulbTemp.get_text())
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,colorSRMTemp,colorSRM=colorSRMTemp.get_text())
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,efficiencyTemp,efficiencyPerc=efficiencyTemp.get_text())
			#fields associated with the ingredient type Adjunct
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,descriptionTemp,description=descriptionTemp.get_text())
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,purposeTemp,purpose=purposeTemp.get_text())
			#fields associated with the ingredient type Yeast
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,potentialAlcoholPercentTemp,potentialAlcoholPer=potentialAlcoholPercentTemp.get_text())
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,purposeTemp,purpose=purposeTemp.get_text())
			self.tmpIngredient = self.indexer.get(ingredient.Ingredient,pitchingTempTemp,pitchingTemp=pitchingTempTemp.get_text())
			
		except:
			pass # 'Please fill all required fields'#dialog goes here
		"""
		print 'made it to the end of the save function'
		self.exit()

	def cancel(self,callback=None):
		"""
		btnCancel supporting function
		??? delete tmpIngredient object ???
		"""
		self.exit()

	def exit(self, callback=None):
		"""
		Destroys the window when close is clicked
		"""
		self.wind.destroy()
		print 'exit Recipe'
