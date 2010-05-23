#!/usr/bin/env python
#
#    Greek New Testament
#    Copyright (C) 2010  Honza Pokorny <honza@honzapokorny.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
import config
import lookup
import sys
import os
import gtk
import pango

class MainWindow(gtk.Window):
    __gtype_name__ = 'MainWindow'
    
    def __init__(self):
        if not os.path.exists(config.ui_mainwindow):
            # raise some error
            pass
        self.builder = gtk.Builder()
        self.builder.add_from_file(config.ui_mainwindow)
        self.builder.connect_signals(self)
        self.db = lookup.LookUp()
        
    def new_window(self):
        window = self.builder.get_object("main_window")
        return window

    def lookup_clicked(self, widget, data=None):
        passage = self.builder.get_object("passage")
        reference = passage.get_text()
        self.db.set_passage(reference)
        text = self.db.get_verse()
        self.push_to_screen(text)

    def show_hint_clicked(self, widget, data=None):
        print 'show hint'
        hint = self.builder.get_object("textview_hint")
        buffer = gtk.TextBuffer()
        buffer.set_text(self.db.get_hint())
        hint.set_buffer(buffer)
    
    def hide_hint_clicked(self, widget, data=None):
        print 'hide hint'
        hint = self.builder.get_object("textview_hint")
        buffer = gtk.TextBuffer()
        buffer.set_text('')
        hint.set_buffer(buffer)

    def push_to_screen(self, passage):
        verse = self.builder.get_object("textview_verse")
        verse.modify_font(pango.FontDescription('sans 16'))
        buffer = gtk.TextBuffer()
        buffer.set_text(passage)
        verse.set_buffer(buffer)

    def on_destroy(self, widget, data=None):
        """on_destroy - called when the MmmWindow is close. """
        #clean up code for saving application state should be added here

        gtk.main_quit()
        

if __name__ == "__main__":
    w = MainWindow()
    window = w.new_window()
    window.show()
    gtk.main()

