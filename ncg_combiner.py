#Boa:Frame:ncg_combiner
"""ncg_combiner is used to combine several individual audits into one large file

ncg_combiner should be used to combine individual audits created using 
ncg_file_generator into one combined audit to add to nessus.  Note:  It is 
the best practice to always generate audits for individual items seperately 
(a single <custom_item> stanza in a nessus audit file), keep them in revision
control, and only combine them as a last step before adding them to nessus.

It should be noted that at present the ncg_editor program will only work on 
these individual audits.
"""

__author__ = "thompsonm@anl.gov (Mike Thompson)"

import os
import ncg_lib
import wx
import wx.lib.stattext
import wx.lib.filebrowsebutton


def create(parent):
    """create method to draw the window"""
    return ncg_combiner(parent)

[wxID_NCG_COMBINER, wxID_NCG_COMBINERADD_DIRECTORY, wxID_NCG_COMBINERADD_FILE, 
 wxID_NCG_COMBINERAUDIT_TYPE, wxID_NCG_COMBINERCURRENT_LIST_TEXT, 
 wxID_NCG_COMBINERCURRENT_LIST_TEXT2, wxID_NCG_COMBINERFILENAME_LABEL, 
 wxID_NCG_COMBINERFILENAME_TO_SAVE, wxID_NCG_COMBINERFILEPATH, 
 wxID_NCG_COMBINERFILES_HEADER_LABEL, wxID_NCG_COMBINERFILE_SAVE_TEXT, 
 wxID_NCG_COMBINERGENERATE, wxID_NCG_COMBINERPATH, 
 wxID_NCG_COMBINERPATH_TO_SAVE, wxID_NCG_COMBINERPLEASE_SELECT, 
 wxID_NCG_COMBINERSTATICTEXT1, wxID_NCG_COMBINERWELCOME, wxID_NCG_FILE_COMBINERNEW,
] = [wx.NewId() for _init_ctrls in range(18)]


class ncg_combiner(wx.Frame):
    """Main class for ncg_combiner"""

    def _init_ctrls(self, prnt):
        """ Initialize controls in this window """
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_NCG_COMBINER, name=u'ncg_combiner',
            parent=prnt, pos=wx.Point(415, 217), size=wx.Size(1026, 656),
            style=wx.TAB_TRAVERSAL | wx.DEFAULT_FRAME_STYLE,
            title=u'Nessus Compliance Generator: File Combiner')
        self.SetClientSize(wx.Size(1026, 656))
        self.SetBackgroundColour(wx.Colour(237, 237, 237))

        self.welcome = wx.StaticText(id=wxID_NCG_COMBINERWELCOME,
            label=u'Welcome to the audit file combiner.  This program will combine multiple audit files into a single combined audit to upload to Nessus.',
            name=u'welcome', parent=self, pos=wx.Point(16, 16),
            size=wx.Size(766, 17), style=0)

        self.please_select = wx.StaticText(id=wxID_NCG_COMBINERPLEASE_SELECT,
            label=u'Please select a file or directory to add to the session.  Note:  directories must contain only audit files generated by this program.',
            name=u'please_select', parent=self, pos=wx.Point(16, 80),
            size=wx.Size(735, 17), style=0)

        self.filepath = wx.lib.filebrowsebutton.FileBrowseButtonWithHistory(buttonText=u'Browse',
            dialogTitle=u'Select a file', id=wxID_NCG_COMBINERFILEPATH,
            initialValue='', labelText='Select a file:', parent=self,
            pos=wx.Point(16, 104), size=wx.Size(448, 64),
            toolTip='Type File name or browse to select')
        self.filepath.SetBackgroundColour(wx.Colour(237, 237, 237))
        self.filepath.SetLabel(u'Select a file:')

        self.path = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='Browse',
            dialogTitle=u'Select a directory to save in',
            id=wxID_NCG_COMBINERPATH, labelText='Select a directory:',
            newDirectory=False, parent=self, pos=wx.Point(16, 184),
            size=wx.Size(448, 64), startDirectory='.', style=wx.TAB_TRAVERSAL,
            toolTip='Type directory name or browse to select')
        self.path.SetName(u'path')
        self.path.SetBackgroundColour(wx.Colour(237, 237, 237))

        self.add_file = wx.Button(id=wxID_NCG_COMBINERADD_FILE,
            label=u'Add File', name=u'add_file', parent=self,
            pos=wx.Point(496, 120), size=wx.Size(93, 32), style=0)
        self.add_file.Bind(wx.EVT_BUTTON, self.Onadd_fileButton,
            id=wxID_NCG_COMBINERADD_FILE)

        self.add_directory = wx.Button(id=wxID_NCG_COMBINERADD_DIRECTORY,
            label=u'Add Directory', name=u'add_directory', parent=self,
            pos=wx.Point(496, 200), size=wx.Size(93, 32), style=0)
        self.add_directory.Bind(wx.EVT_BUTTON, self.OnAdd_directoryButton,
            id=wxID_NCG_COMBINERADD_DIRECTORY)

        self.staticText1 = wx.StaticText(id=wxID_NCG_COMBINERSTATICTEXT1,
            label=u'Audit files should only be combined with others of the same type -- SQL or Windows but not both.  Its recommended that you keep the original audit files, as the editor only works on individual items -- not combined files.',
            name='staticText1', parent=self, pos=wx.Point(16, 32),
            size=wx.Size(776, 32), style=0)

        self.current_list_text = wx.StaticText(id=wxID_NCG_COMBINERCURRENT_LIST_TEXT,
            label=u'', name=u'current_list_text', parent=self,
            pos=wx.Point(624, 120), size=wx.Size(170, 480), style=0)

        self.current_list_text2 = wx.StaticText(id=wxID_NCG_COMBINERCURRENT_LIST_TEXT2,
            label=u'', name=u'current_list_text2', parent=self,
            pos=wx.Point(824, 120), size=wx.Size(170, 480), style=0)

        self.files_header_label = wx.StaticText(id=wxID_NCG_COMBINERFILES_HEADER_LABEL,
            label=u'Files to be combined:', name=u'files_header_label',
            parent=self, pos=wx.Point(616, 104), size=wx.Size(124, 17),
            style=0)

        self.generate = wx.Button(id=wxID_NCG_COMBINERGENERATE,
            label=u'Generate Combined File', name=u'generate', parent=self,
            pos=wx.Point(800, 600), size=wx.Size(176, 32), style=0)
        self.generate.Bind(wx.EVT_BUTTON, self.OnGenerateButton,
            id=wxID_NCG_COMBINERGENERATE)

        self.path_to_save = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='Browse',
            dialogTitle=u'Select a directory to save in',
            id=wxID_NCG_COMBINERPATH_TO_SAVE, labelText='Select a directory:',
            newDirectory=False, parent=self, pos=wx.Point(480, 592),
            size=wx.Size(296, 48), startDirectory='.', style=wx.TAB_TRAVERSAL,
            toolTip='Type directory name or browse to select')
        self.path_to_save.SetBackgroundColour(wx.Colour(237, 237, 237))

        self.filename_to_save = wx.TextCtrl(id=wxID_NCG_COMBINERFILENAME_TO_SAVE,
            name=u'filename', parent=self, pos=wx.Point(320, 600),
            size=wx.Size(120, 32), style=0, value=u'')

        self.filename_label = wx.StaticText(id=wxID_NCG_COMBINERFILENAME_LABEL,
            label=u'Filename:', name=u'filename_label', parent=self,
            pos=wx.Point(248, 608), size=wx.Size(64, 17), style=0)

        self.file_save_text = wx.lib.stattext.GenStaticText(ID=wxID_NCG_COMBINERFILE_SAVE_TEXT,
              label=u'', name=u'file_save_text', parent=self, pos=wx.Point(24,
              632), size=wx.Size(968, 17), style=0)
        self.file_save_text.SetBackgroundColour(wx.Colour(237, 237, 237))

        self.audit_type = wx.RadioBox(choices=['SQL', 'Windows'],
            id=wxID_NCG_COMBINERAUDIT_TYPE, label=u'Compliance Audit Type',
            majorDimension=1, name=u'audit_type', parent=self,
            pos=wx.Point(16, 256), size=wx.Size(216, 72),
            style=wx.RA_SPECIFY_COLS)
        self.audit_type.SetBackgroundStyle(wx.BG_STYLE_COLOUR)

        self.new = wx.Button(id=wxID_NCG_FILE_COMBINERNEW, label=u'New',
            name=u'new', parent=self, pos=wx.Point(132, 600), size=wx.Size(96,
            32), style=0)
        self.new.Bind(wx.EVT_BUTTON, self.OnButtonNew,
            id=wxID_NCG_FILE_COMBINERNEW)

    def OnButtonNew(self, event):
        """Handler for 'New' button"""
        self.filename_to_save.SetValue('')
        self.filepath.SetValue('')
        self.path.SetValue('')
        self.path_to_save.SetValue('')
        self.files = []
        self.display_files()
        event.Skip()

    def display_files(self):
        """Displays all files that have been added up to this point"""
        text = ""
        text2 = ""
        if len(self.files) > 25:
            for file in self.files[:25]:
                pathitems = file.split(os.path.sep)
                basename = pathitems[len(pathitems)-1]
                text += "%s\n" % basename
            for file in self.files[25:]:
                pathitems = file.split(os.path.sep)
                basename = pathitems[len(pathitems)-1]
                text2 += "%s\n" % basename
        else:        
            for file in self.files:
                pathitems = file.split(os.path.sep)
                basename = pathitems[len(pathitems)-1]
                text += "%s\n" % basename
        
        self.current_list_text.SetLabel(text)
        self.current_list_text2.SetLabel(text2)

    def __init__(self, parent):
        """Class init method"""
        self._init_ctrls(parent)
        self.files = [] 
        
    def Onadd_fileButton(self, event):
        """Handler for add_file button click event.

        Adds whatever is in the file box to the files class datastructure.
        """
        add_file = True
        file = self.filepath.GetValue()
        for f in self.files:
          if f == file:
            self.file_save_text.SetLabel("%s is already in list!" % file)
            add_file = False
            break
        if add_file:
          self.files.append(file)
        self.display_files()
        event.Skip()

    def OnAdd_directoryButton(self, event):
        """Handler for add_directory button click event
        
        Adds all files within the chosen directory to the files list.
        """
        path = self.path.GetValue()
        basenames = os.listdir(path)
        

        for basename in basenames:
          add_file = True
          file = os.path.join(path, basename)
          for f in self.files:
            if f == file:
              self.file_save_text.SetLabel("One or more files are already in list!")
              add_file = False
              break
          if add_file:
            self.files.append(file)
        self.display_files()
        event.Skip()

    def OnGenerateButton(self, event):
        """Handler for generate button.
 
        Calls ncg_lib.combine_files, and if succussful, saves a file to disk

        TODO: get status from ncg_lib to return back to the user.
        """
        filename = self.filename_to_save.GetValue()
        full_path = os.path.join(self.path_to_save.GetValue(), filename)
        if (self.audit_type.GetSelection() == 0):
            audit_type = "Database"
        else:
            audit_type = "Windows"
        ncg_lib.combine_files(audit_type, self.files, full_path)
        self.file_save_text.SetLabel("File saved to %s" % full_path) 
        event.Skip()
