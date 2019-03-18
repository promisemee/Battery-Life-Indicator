import os
import signal
import sys
import gi
import time
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk, AppIndicator3
# from gi.repository import GObject as gobject
from threading import Thread

class Indicator():
	def __init__(self):
		self.app_ID = 'heart-indicator'
		self.battery_status_file = "/sys/class/power_supply/BAT1/capacity"
		self.HEART = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
		iconpath = self.icon_status()
		self.indicator = AppIndicator3.Indicator.new(
            self.app_ID, os.path.abspath(iconpath),
            AppIndicator3.IndicatorCategory.OTHER)
		self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)       
		self.indicator.set_menu(self.build_menu())

        
        # the thread:
		self.update = Thread(target=self.show_icon)
        # daemonize the thread to make the indicator stopable
		self.update.setDaemon(True)
		self.update.start()

	def build_menu(self):
	    menu = gtk.Menu()
	    item_battery = gtk.MenuItem('Brightness')
	    menu.append(item_battery)
	    item_quit = gtk.MenuItem('Quit')
	    item_quit.connect('activate', quit)
	    menu.append(item_quit)
	    menu.show_all()
	    return menu

	def quit(source):
	    gtk.main_quit()

	def icon_status(self):
		stat = self.HEART[10]
		with open(self.battery_status_file) as file:
			tmp = file.read().splitlines()	
			battery = int(tmp[0])
		if battery/10 <=3 :
			bat_stat = 0
		else : 
			bat_stat = int(battery/10)
		stat = self.HEART[bat_stat]
		
		return 'img/'+str(stat)+'.png'

	def show_icon(self):
		while True:
			time.sleep(50)
			icon_path = self.icon_status()
			self.indicator.set_icon(os.path.abspath(icon_path))



Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
gtk.main()