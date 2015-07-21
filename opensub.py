#!/usr/bin/env python
import xmlrpclib

class OpenSubtitle:

	url = 'http://api.opensubtitles.org/xml-rpc'
	language = 'es'
	server = xmlrpclib.Server(url)

	#def __init__(self):
	
	def serverInfo(self):
		return self.server.ServerInfo()

	def login(self):
		print 'LOGIN Opensubtitles.org'
		resp = self.server.LogIn('','',self.language,'MyAPP V1')
		self.token = str(resp['token'])
		return (resp)

	def logout(self):
		self.server.LogOut(self.token)
		print 'LOGOUT Opensubtitles.org'

	def search_subs(self, params):
		data = self.server.SearchSubtitles(self.token, params)
		return data
