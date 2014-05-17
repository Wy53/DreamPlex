# -*- coding: utf-8 -*-
"""
DreamPlex Plugin by DonDavici, 2012
 
https://github.com/DonDavici/DreamPlex

Some of the code is from other plugins:
all credits to the coders :-)

DreamPlex Plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

DreamPlex Plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
"""
#===============================================================================
# IMPORT
#===============================================================================
import cPickle as pickle

from Components.config import config

from DP_LibMain import DP_LibMain

from DPH_Singleton import Singleton

from __common__ import printl2 as printl

#===============================================================================
# 
#===============================================================================
class DP_LibShows(DP_LibMain):

	g_url = None
	
	#===========================================================================
	# 
	#===========================================================================
	def __init__(self, session, entryData):
		"""
		we use showEpisodesDirectly for the onDeck functions that forces us to jump directly to episodes
		"""
		printl ("", self, "S")

		self.entryData = entryData

		if self.entryData["showEpisodesDirectly"]:
			DP_LibMain.__init__(self, session, "episodes")
		else:
			DP_LibMain.__init__(self, session, "tvshows")

		printl ("", self, "C")

	#===============================================================================
	# 
	#===============================================================================
	def loadLibrary(self, params):
		printl ("", self, "S")
		printl("params: " + str(params), self, "D")
		printl("entryData: " + str(self.entryData), self, "D")

		returnTo = None

		if self.entryData["showEpisodesDirectly"]:
			printl("show episodes directly ...", self, "D")
			
			url = self.entryData["contentUrl"]
			printl("url: " + str(url), self, "D")
			
			library, mediaContainer = Singleton().getPlexInstance().getEpisodesOfSeason(url, directMode=True)

		else:
			# Diplay all TVShows
			if params["viewMode"] is None:
				printl("show TV shows ...", self, "D")

				url = self.entryData["contentUrl"]
				printl("url: " + str(url), self, "D")
				library, mediaContainer = Singleton().getPlexInstance().getShowsFromSection(url)

			# Display the Seasons Menu
			elif params["viewMode"] == "ShowSeasons":
				printl("show seasons of TV show ...", self, "D")
				
				url = params["contentUrl"]
				library, mediaContainer = Singleton().getPlexInstance().getSeasonsOfShow(url)
				returnTo = "backToShows"

			# Display the Episodes Menu
			elif params["viewMode"] == "ShowEpisodes":
				printl("show episodes of season ...", self, "D")
				
				url = params["contentUrl"]
				library, mediaContainer = Singleton().getPlexInstance().getEpisodesOfSeason(url)
				returnTo = "backToSeasons"

		printl ("", self, "C")
		return library, returnTo, mediaContainer
