#!/usr/bin/python2.7

import pygtk
import gtk
import gtk.glade

from player import Player

import sys
import signal
from gmusicapi.api import Api

class Login:

	def __init__(self):
		loginGuiPath = "guis/logingui.glade"
		self.builder = gtk.Builder()
		self.builder.add_from_file(loginGuiPath)
		self.builder.connect_signals(self)
		self.builder.get_object("loginGUI").show_all()
		self.builder.get_object("loginGUI").connect("delete_event", self.delete_event)

	def delete_event(self, widget, event, data=None):
		gtk.main_quit()
		return False

	def on_loginButton_clicked(self, widget):
		self.api = Api()
		logged_in = False
		attempts = 0

		email = self.builder.get_object("user").get_text()
		password = self.builder.get_object("password").get_text()

		logged_in = self.api.login(email, password)
		attempts += 1

		if(logged_in):
			self.builder.get_object("loginGUI").destroy()
			player = Player(self.api)
			pass
		else:
			diag = gtk.Dialog(title="Login Fehler !", parent=self.builder.get_object("loginGUI"), flags= gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			label = gtk.Label("Login Fehler !")
			diag.vbox.pack_start(label)
			label.show()
			diag.run()
			diag.destroy()

if __name__ == "__main__":
	login = Login()
	gtk.main()
