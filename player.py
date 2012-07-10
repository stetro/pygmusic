#!/usr/bin/python2.7

import sys
import signal
import gtk

import pygst
pygst.require("0.10")
import gst

from getpass import getpass
from gmusicapi.api import Api

class Player(Api):
	def __init__(self, arg):
		super(Player, self).__init__()
		self.api = arg
		playerGuiPath = "guis/player.glade"
		self.builder = gtk.Builder()
		self.builder.add_from_file(playerGuiPath)
		self.builder.connect_signals(self)
		self.builder.get_object("playerGUI").show_all()
		self.builder.get_object("playerGUI").connect("delete_event", self.delete_event)
		self.builder.get_object("imagemenuitem5").connect("button_release_event", self.delete_event)
		self.player = None
		self.builder.get_object("play").connect("button_release_event",self.play_song)
		self.fill_playlist()
		self.fill_albumlist()

	def delete_event(self, widget, event, data=None):
		gtk.main_quit()
		return False

	def play_song(self,windget,event,data=None):
		songlist = self.gtklist.get_selection()
		if songlist:
			song = songlist[0]
		else:
			song = None
		if song:
			self.play(self.api.get_stream_url(self.playlist[self.gtklist.child_position(song)]["id"]), self.playlist[self.gtklist.child_position(song)]["title"]+" - "+self.playlist[self.gtklist.child_position(song)]["artist"])

	def play(self, url, title):
		if(self.player != None):
			self.player.set_state(gst.STATE_NULL)
			self.player.set_property("uri", url)
			self.player.set_state(gst.STATE_PLAYING)
			self.builder.get_object("progressbar").push(1,title)
		else:
			self.player = gst.element_factory_make("playbin2", "player")
			bus = self.player.get_bus()
			bus.add_signal_watch()
			bus.connect("message", self.on_message)
			self.player.set_property("uri", url)
			self.player.set_state(gst.STATE_PLAYING)
			self.builder.get_object("progressbar").push(1,title)

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS or t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			self.builder.get_object("progressbar").push(1,err)
			self.player.set_state(gst.STATE_NONE)

	def fill_albumlist(self):
		self.builder.get_object("progressbar").push(1,"Alben werden geladen ...")
		scrolledalbumlist = self.builder.get_object("scrolledalbumlist")
		self.gtkalbumlist = gtk.List()
		scrolledalbumlist.add_with_viewport(self.gtkalbumlist)
		self.gtkalbumlist.show()
		self.albumlist = []
		for i in range(len(self.playlist)):
			try:
				self.albumlist.index(self.playlist[i]["album"])
			except:
				self.albumlist.append(self.playlist[i]["album"])

		for i in range(len(self.albumlist)):
			label = gtk.Label(self.albumlist[i])
			label.set_alignment(0,0)
			list_item = gtk.ListItem()
			list_item.add(label)
			label.show()
			self.gtkalbumlist.add(list_item)
			list_item.show()

	def fill_playlist(self):
		self.builder.get_object("progressbar").push(1,"Songs werden geladen ...")
		scrolledplaylist = self.builder.get_object("scrolledplaylist")
		self.gtklist = gtk.List()
		scrolledplaylist.add_with_viewport(self.gtklist)
		self.gtklist.show()
		self.playlist = self.api.get_all_songs()
		for i in range(len(self.playlist)):
			buffer = self.playlist[i]["title"].strip()+" - "+self.playlist[i]["artist"].strip()+" - "+self.playlist[i]["album"].strip()
			label = gtk.Label(buffer)
			label.set_alignment(0,0)
			list_item = gtk.ListItem()
			list_item.add(label)
			label.show()
			self.gtklist.add(list_item)
			list_item.show()
		self.builder.get_object("progressbar").push(1,str(len(self.playlist))+" Songs wurden geladen !")

if __name__ == "__main__":
	from login import Login
	login = Login()
	gtk.main()