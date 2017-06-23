#!/usr/bin/env python
#Boa:App:BoaApp
""" Main executable for the Nessus Compliance Generator program.

This program will generate .audit files to use with nessus in their compliance
program.  Currently supported are Oracle SQL audits, Windows Group Membership, 
and Windows file contents.  This application supplies a config generator,
editor, and combiner.  Individual documentation for those modes is supplied 
with the respective modules

GUI Created using Boa Constructor and wxWidgets.
"""

__author__ = "thompsonm@anl.gov (Mike Thompson)"

import wx
import ncg_selector
import ncg_file_generator

modules = { 	
    u'ncg_combiner' :
        [0, u'NCG: Audit File Combiner', u'ncg_combiner.py'],
    u'ncg_editor' : 
        [0, u'NCG: Audit File Editor', u'ncg_editor.py'],
    u'ncg_file_generator': 
        [0,
            u'NCG: Audit File Generator',
            u'ncg_file_generator.py'
         ],
        'ncg_selector': 
        [1, u'NCG: Mode Selector', 'ncg_selector.py']}


class BoaApp(wx.App):
    """Main class for a Boa App"""
    def OnInit(self):
        """Initialization Method -- creates main selector window"""
        self.main = ncg_selector.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


def main():
    """Our main loop"""
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
