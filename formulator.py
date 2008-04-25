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
from brewobject import *
import util, copy

class Formulator(object):
	batchSizeGal = 5.0 # Gallons
	styleProfile = None
	desiredOGGU = 0 # Desired OG, get from profile?
					# = self.styleProfile.GUPerGallon * self.batchSizeGal

	def __init__(self,styleProfile,batchSizeGal=5.0):
		self.styleProfile = styleProfile
		self.desiredOGGU = styleProfile.GUPerGallon * batchSizeGal

	def getIBU(self):
		return None

	def getPotABV(self):
		return desiredOGGU / 7.5

	def getHopProfile(self):
		return None

	def getGrainBill(self):
		return None

	def getHopBoilTime(self):
		return None

	def getGrainAdditions(self):
		return None

	def getIngredientGravity(self,ingredient):
		"""
		Calculate the Gravity Units per one gallon of a particular ingredient.

		ingredient: formulator.Ingredient object
		"""
		return ingredient.efficiencyPerc * ingredient.yieldGUlb

	def getPoundsIngredient(self,ingredient):
		"""
		Calculate pounds of malt needed for current formulator settings.

		ingredient: formulator.Ingredient object
		"""
		return self.getIngredientGravity(ingredient) / ingredient.yieldGUlb

class StyleProfile(BrewObject):
	name = ''
	grains = []
	hops = {'bittering': [], 'finishing': []}
	GUPerGallon = 0

	#def setGUlb(self, ingredient, percentage):
	#	ingredient.yieldGU = self.GUPerGallon * percentage
	
	def addGrain(self,grain,percentage, incidence):
		grainDict = {
				'grain': grain,
				'percentage': percentage,
				'incidence': incidence,
				'yieldGU': self.GUPerGallon * percentage
				}
		grains = [i for i in self.grains]
		grains.append( grainDict )
		self.grains = grains
