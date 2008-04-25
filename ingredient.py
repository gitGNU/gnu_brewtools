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
from util import *

class Ingredient(BrewObject):


	name  = ""
	stock = 0.0
	stockUnit = ''
	recipeAmount = ''
	
	def __init__(self,indexer,**kwargs):
		"""
		Represents ingredients in brew. Should be subclassed.

		Arg's required - all
			name - str
			stock - float
			stockUnit - str

		Description of Arg's
			name - what the ingredient is called
			stock - a number the represents the amount of the ingredient on hand
			stockUnit - the unit of measurement that is being used
		"""
		try:
			self.name = kwargs['name']
			self.stock = kwargs['stock']
			self.stockUnit = kwargs['stockUnit']
		except:
			raise Exception('This field cannot be left blank, dude!')

		super(Ingredient, self).__init__(indexer,**kwargs)

	
	def inStock():
		"""
		Returns bool
		if stock is zero returns false
		if stock is greater then zero returns true
		"""

		return stock != 0
		

class Hops(Ingredient):

	alphaAcids = 0.0
	purpose = []

	def __init__(self,indexer,**kwargs):
		"""
		Represents hops in brew.

		Arg's required
			alphaAcids - float
			purpose - list of str
		"""

		try:
			self.name = kwargs['name']
			self.alphaAcids = kwargs['alphaAcids']
			self.purpose = kwargs['purpose']
		except:
			raise Exception('This field cannot be left blank, dude!')

		super(Hops, self).__init__(indexer,**kwargs)

class Grain(Ingredient):


	efficiencyPerc = 0.68
	yieldGUlb = 0 # This is GU per recipe
	colorSRM = 0.0

	def __init__(self,indexer,**kwargs):

		"""
		Represents grains in brew.
		
		Arg's required
			yieldGUlb - int
			colorSRM - float

		Arg's NOT required
			efficiencyPerc - float

		Definitions of Arg's
		efficiencyPerc - represents how much sugars from grain, for example malt = 100%, mash = 67%
		yieldGUlb - gravity units per pound that are yielded from the grain. 
			used to calcualte the total grain bill needed for the recipe.
		colorSRM - used to calculate the color the grains will give to the wort
		"""
		try:
			self.yieldGUlb = kwargs['yieldGUlb']
			self.colorSRM = kwargs['colorSRM']
		except:
			raise Exception('This field cannot be left blank, dude!')
		try:
			self.efficiencyPerc = kwargs['efficiency']	
		except:
			pass

		super(Grain, self).__init__(indexer,**kwargs)

class Adjunct(Ingredient):


	
	purposeAdjunct = []
	description = ""
	
	def __init__(self,indexer,**kwargs):
		"""
		Represents adjunct in brew.

		Arg's required
			description - str

		Arg's NOT required
			purposeAdjunct - list of str
		"""
		try:
			self.description = kwargs['description']
		except:
			raise Exception('This field cannot be left blank, dude!')
		try:	
			self.purposeAdjunct = kwargs['purposeAdjunct']
		except:
			pass
	
		super(Adjunct, self).__init__(indexer,**kwargs)

class Yeast(Ingredient):
	potentialAlcoholPer = 0.0
	purposeYeast = []
	pitchingTemp = 0.0

	def __init__(self,indexer,**kwargs):
		"""
		Represents Yeast in brew.

		Arg's required
			none that are apecific to this object

		Arg's NOT required
			pitchingTemp - int
			purposeYeast - list of str
			potentialAlcoholPercent - float
		"""

		try:
			pitchingTemp = kwargs['pitchingTemp']
			potentialAlcoholPer = kwargs['potentialAlcoholPer']
			purposeYeast = kwargs['purposeYeast']
		except:
			pass

		super(Yeast, self).__init__(indexer,**kwargs)
