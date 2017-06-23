#Boa:Frame:ncg_selector
"""Selector window to choose ncg_* modes."""

__author__ = "thompsonm@anl.gov (Mike Thompson)"

import wx
import ncg_file_generator
import ncg_editor
import ncg_combiner


def create(parent):
    "create method to draw our window"""
    return ncg_selector(parent)

[wxID_NCG_SELECTOR, wxID_NCG_SELECTORFILE_COMBINER, 
 wxID_NCG_SELECTORFILE_EDITOR, wxID_NCG_SELECTORFILE_GENERATOR, 
] = [wx.NewId() for _init_ctrls in range(4)]


class ncg_selector(wx.Frame):
    """Main class definition"""

    def _init_ctrls(self, prnt):
	    """initialize our controls"""
        wx.Frame.__init__(self, id=wxID_NCG_SELECTOR, name=u'ncg_selector',
              parent=prnt, pos=wx.Point(423, 399), size=wx.Size(315, 196),
              style=wx.DEFAULT_FRAME_STYLE, title=u'NCG: Select a Mode to Run')
        self.SetClientSize(wx.Size(315, 196))

        self.file_generator = wx.Button(id=wxID_NCG_SELECTORFILE_GENERATOR,
              label=u'Audit File Generator', name=u'file_generator',
              parent=self, pos=wx.Point(48, 32), size=wx.Size(224, 32),
              style=0)
        self.file_generator.Bind(wx.EVT_BUTTON, self.OnFile_generatorButton,
              id=wxID_NCG_SELECTORFILE_GENERATOR)

        self.file_editor = wx.Button(id=wxID_NCG_SELECTORFILE_EDITOR,
              label=u'Audit File Editor', name=u'file_editor', parent=self,
              pos=wx.Point(48, 80), size=wx.Size(224, 32), style=0)
        self.file_editor.Bind(wx.EVT_BUTTON, self.OnFile_editorButton,
              id=wxID_NCG_SELECTORFILE_EDITOR)

        self.file_combiner = wx.Button(id=wxID_NCG_SELECTORFILE_COMBINER,
              label=u'Audit File Combiner', name=u'file_combiner', parent=self,
              pos=wx.Point(48, 128), size=wx.Size(224, 32), style=0)
        self.file_combiner.Bind(wx.EVT_BUTTON, self.OnFile_combinerButton,
              id=wxID_NCG_SELECTORFILE_COMBINER)
        self.SetBackgroundColour(wx.Colour(237, 237, 237))

    def __init__(self, parent):
 	    """std init method.  Call init_ctrls."""
        self._init_ctrls(parent)

    def OnFile_generatorButton(self, event):
        """Handler for file_generator button -- launches ncg_file_generator"""
        print "[debug]: trying to launch generator"
        ncg_file_generator.create(self).Show(True)
        event.Skip()

    def OnFile_editorButton(self, event):
        """Handler for file_editor button -- launches ncg_editor"""
        ncg_editor.create(self).Show(True)
        event.Skip()

    def OnFile_combinerButton(self, event):
        """Handler for file_combiner button -- launches ncg_combiner"""
        ncg_combiner.create(self).Show(True)
        event.Skip()
