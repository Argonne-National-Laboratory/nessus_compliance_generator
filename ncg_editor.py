#Boa:Frame:ncg_editor
"""ncg_editor is used to edit files created by the ncg_file_generator portion
of this program.  It will not work on combined files at this time.  It takes
a nessus audit file and parses it, allows a user to edit fields, then creates
a new file using the same filename as the original (thus replacing the original)
"""

__author__ = "thompsonm@anl.gov (Mike Thompson)"

import wx
import wx.lib.filebrowsebutton
import ncg_lib


def create(parent):
    """create method to draw the window"""
    return ncg_editor(parent)

[wxID_NCG_EDITOR, wxID_NCG_EDITORBROWSE_INSTRUCTIONS, 
 wxID_NCG_EDITOREXPECTED_OUTPUT, wxID_NCG_EDITOREXPECTED_OUTPUT_LABEL, 
 wxID_NCG_EDITORFILE_SAVE_TEXT, wxID_NCG_EDITORGROUP_NAME, 
 wxID_NCG_EDITORGROUP_NAME_LABEL, wxID_NCG_EDITORLOAD, 
 wxID_NCG_EDITORLONG_DESCRIPTION, wxID_NCG_EDITORLONG_DESCRIPTION_LABEL, 
 wxID_NCG_EDITORMEMBERS_TO_REQUIRE, wxID_NCG_EDITORPATH, wxID_NCG_EDITORREGEX, 
 wxID_NCG_EDITORREGEX_LABEL, wxID_NCG_EDITORREMOTE_FILE, 
 wxID_NCG_EDITORREMOTE_FILE_LABEL, wxID_NCG_EDITORREQUIRED_MEMBERS_LABEL, 
 wxID_NCG_EDITORSHORT_DESCRIPTION, wxID_NCG_EDITORSHORT_DESCRIPTION_LABEL, 
 wxID_NCG_EDITORSQL_QUERY, wxID_NCG_EDITORSQL_QUERY_LABEL, 
 wxID_NCG_EDITORUPDATE, 
] = [wx.NewId() for _init_ctrls in range(22)]


class ncg_editor(wx.Frame):
    """Main class for ncg_editor"""

    def _init_ctrls(self, prnt):
        """Initialize all controls"""
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_NCG_EDITOR, name=u'ncg_editor',
              parent=prnt, pos=wx.Point(527, 187), size=wx.Size(1011, 577),
              style=wx.DEFAULT_FRAME_STYLE, title=u'NCG: Audit File Editor')
        self.SetClientSize(wx.Size(1011, 577))
        self.SetBackgroundColour(wx.Colour(237, 237, 237))

        self.short_description = wx.TextCtrl(id=wxID_NCG_EDITORSHORT_DESCRIPTION,
              name=u'short_description', parent=self, pos=wx.Point(400, 72),
              size=wx.Size(584, 32), style=0, value=u'')

        self.long_description = wx.TextCtrl(id=wxID_NCG_EDITORLONG_DESCRIPTION,
              name=u'long_description', parent=self, pos=wx.Point(400, 120),
              size=wx.Size(584, 112), style=wx.TE_MULTILINE | wx.TE_LINEWRAP,
              value=u'')

        self.sql_query = wx.TextCtrl(id=wxID_NCG_EDITORSQL_QUERY,
              name=u'sql_query', parent=self, pos=wx.Point(400, 248),
              size=wx.Size(584, 120), style=wx.TE_MULTILINE | wx.TE_LINEWRAP,
              value=u'')

        self.expected_output = wx.TextCtrl(id=wxID_NCG_EDITOREXPECTED_OUTPUT,
              name=u'expected_output', parent=self, pos=wx.Point(400, 384),
              size=wx.Size(584, 32), style=0, value=u'')

        self.update = wx.Button(id=wxID_NCG_EDITORUPDATE, label=u'Update',
              name=u'update', parent=self, pos=wx.Point(840, 512),
              size=wx.Size(136, 40), style=0)
        self.update.Bind(wx.EVT_BUTTON, self.OnUpdateButton,
              id=wxID_NCG_EDITORUPDATE)

        self.remote_file = wx.TextCtrl(id=wxID_NCG_EDITORREMOTE_FILE,
              name=u'remote_file', parent=self, pos=wx.Point(376, 264),
              size=wx.Size(608, 32), style=0, value=u'')

        self.regex = wx.TextCtrl(id=wxID_NCG_EDITORREGEX, name=u'regex',
              parent=self, pos=wx.Point(376, 312), size=wx.Size(608, 32),
              style=0, value=u'')

        self.short_description_label = wx.StaticText(id=wxID_NCG_EDITORSHORT_DESCRIPTION_LABEL,
              label=u'Short Description:', name=u'short_description_label',
              parent=self, pos=wx.Point(280, 80), size=wx.Size(112, 13),
              style=0)

        self.long_description_label = wx.StaticText(id=wxID_NCG_EDITORLONG_DESCRIPTION_LABEL,
              label=u'Long Description:', name=u'long_description_label',
              parent=self, pos=wx.Point(272, 168), size=wx.Size(116, 16),
              style=0)

        self.sql_query_label = wx.StaticText(id=wxID_NCG_EDITORSQL_QUERY_LABEL,
              label=u'SQL Query:', name=u'sql_query_label', parent=self,
              pos=wx.Point(320, 296), size=wx.Size(65, 16), style=0)

        self.expected_output_label = wx.StaticText(id=wxID_NCG_EDITOREXPECTED_OUTPUT_LABEL,
              label=u'Expected Output:', name=u'expected_output_label',
              parent=self, pos=wx.Point(288, 392), size=wx.Size(112, 16),
              style=0)

        self.remote_file_label = wx.StaticText(id=wxID_NCG_EDITORREMOTE_FILE_LABEL,
              label=u'Remote File To Check:', name=u'remote_file_label',
              parent=self, pos=wx.Point(240, 272), size=wx.Size(136, 16),
              style=0)

        self.regex_label = wx.StaticText(id=wxID_NCG_EDITORREGEX_LABEL,
              label=u'Regex to Match in File:', name=u'regex_label',
              parent=self, pos=wx.Point(216, 320), size=wx.Size(152, 16),
              style=0)

        self.path = wx.lib.filebrowsebutton.FileBrowseButton(buttonText=u'Browse',
              dialogTitle=u'Select a file', fileMask='*.*', fileMode=1,
              id=wxID_NCG_EDITORPATH, initialValue='',
              labelText='Select a file:', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(448, 64), startDirectory='.', style=wx.THICK_FRAME,
              toolTip='Type File name or browse to select')
        self.path.SetBackgroundColour(wx.Colour(237, 237, 237))
        self.path.SetToolTipString(u'path')
        self.path.SetValue(u'')
        self.path.SetLabel(u'Select a file:')
        self.path.SetName(u'path')

        self.load = wx.Button(id=wxID_NCG_EDITORLOAD, label=u'Load',
              name=u'load', parent=self, pos=wx.Point(472, 16), size=wx.Size(88,
              32), style=0)
        self.load.Bind(wx.EVT_BUTTON, self.OnLoadButton, id=wxID_NCG_EDITORLOAD)

        self.group_name = wx.TextCtrl(id=wxID_NCG_EDITORGROUP_NAME,
              name=u'group_name', parent=self, pos=wx.Point(432, 240),
              size=wx.Size(272, 32), style=0, value=u'')

        self.group_name_label = wx.StaticText(id=wxID_NCG_EDITORGROUP_NAME_LABEL,
              label=u'Group to Check:', name=u'group_name_label', parent=self,
              pos=wx.Point(320, 248), size=wx.Size(95, 17), style=0)

        self.members_to_require = wx.TextCtrl(id=wxID_NCG_EDITORMEMBERS_TO_REQUIRE,
              name=u'members_to_require', parent=self, pos=wx.Point(432, 280),
              size=wx.Size(520, 32), style=0, value=u'')

        self.required_members_label = wx.StaticText(id=wxID_NCG_EDITORREQUIRED_MEMBERS_LABEL,
              label=u'Members to Require:', name=u'required_members_label',
              parent=self, pos=wx.Point(264, 288), size=wx.Size(128, 24),
              style=0)

        self.file_save_text = wx.StaticText(id=wxID_NCG_EDITORFILE_SAVE_TEXT,
              label=u'', name=u'file_save_text', parent=self, pos=wx.Point(8,
              552), size=wx.Size(992, 17), style=0)

        self.browse_instructions = wx.StaticText(id=wxID_NCG_EDITORBROWSE_INSTRUCTIONS,
              label=u'Browse or enter a filename and then click "Load"',
              name=u'browse_instructions', parent=self.path, pos=wx.Point(88,
              48), size=wx.Size(270, 17), style=0)
        self.browse_instructions.SetToolTipString(u'')

    def __init__(self, parent):
        """Class init method.  Hides most controls by default."""
        self._init_ctrls(parent)
        self.hide_all()
        self.type = ""
        
    def hide_all(self):
        """Hides all controls except the file dialog box"""
        # start with all controls not shown.  We'll display as needed 
        # depending on the selected file.
        self.short_description.Show(False)
        self.long_description.Show(False)
        self.sql_query.Show(False)
        self.expected_output.Show(False)
        self.update.Show(False)
        self.remote_file.Show(False)
        self.regex.Show(False)
        self.short_description_label.Show(False)
        self.long_description_label.Show(False)
        self.sql_query_label.Show(False)
        self.expected_output_label.Show(False)
        self.remote_file_label.Show(False) 
        self.regex_label.Show(False)
        self.group_name.Show(False) 
        self.group_name_label.Show(False)
        self.members_to_require.Show(False)
        self.required_members_label.Show(False)
        
    def show_sql(self):
        """Shows controls for the sql editor mode"""
        self.short_description.Show(True)
        self.long_description.Show(True)
        self.sql_query.Show(True)
        self.expected_output.Show(True)        
        self.short_description_label.Show(True)
        self.long_description_label.Show(True)
        self.sql_query_label.Show(True)
        self.expected_output_label.Show(True)
        self.update.Show(True)
        
    def show_windows_group(self):
        """Shows controls for the windows group membership editor mode"""
        self.short_description.Show(True)
        self.long_description.Show(True)
        self.short_description_label.Show(True)
        self.long_description_label.Show(True)
        self.group_name.Show(True) 
        self.group_name_label.Show(True)
        self.members_to_require.Show(True)
        self.required_members_label.Show(True)
        self.update.Show(True)
        
    def show_windows_file(self):
        """Shows controls for the windows file contents mode"""
        self.short_description.Show(True)
        self.long_description.Show(True)
        self.short_description_label.Show(True)
        self.long_description_label.Show(True)
        self.remote_file.Show(True)
        self.regex.Show(True)
        self.remote_file_label.Show(True) 
        self.regex_label.Show(True)
        self.update.Show(True)
        
    def OnLoadButton(self, event):
        """Handler for the load button click action
        
        Uses ncg_lib.parse_audit_file to make a guess at what type of audit
        file this is.  Error checking is minimal
        """
        self.hide_all()
        filename = self.path.GetValue()
        parsed = ncg_lib.parse_audit_file(filename)
        self.type = parsed.keys()[0]
        info = parsed.values()[0][0]
        description = parsed.values()[0][1]
        self.short_description.SetValue(info)
        self.long_description.SetValue(description)
        if self.type == "Database":
            sql_request = parsed.values()[0][2]
            sql_expect = parsed.values()[0][3]
            print "[debug] sql vals: %s %s" % (sql_request, sql_expect)
            self.sql_query.SetValue(sql_request)
            self.expected_output.SetValue(sql_expect)
            self.show_sql()
        else:
            value_data = parsed.values()[0][2]
            if self.type == "GROUP_MEMBERS_POLICY":
                group_name = parsed.values()[0][3] 
                self.group_name.SetValue(group_name)
                self.members_to_require.SetValue(value_data)
                self.show_windows_group()
            elif self.type == "FILE_CONTENT_CHECK":
                regex = parsed.values()[0][3]
                self.regex.SetValue(regex)
                self.remote_file.SetValue(value_data)
                self.show_windows_file()
        event.Skip()

    def OnUpdateButton(self, event):
        """Handler for update button click action
    
        Uses generate methods to generate a new audit file in place of the old
        one.  This means that items changed not using ncg_ tools will not 
        be reflected!
        """
        filename = self.path.GetValue()
        info = self.long_description.GetValue()
        description = self.short_description.GetValue()
        if self.type == "Database":
            sql_request = self.sql_query.GetValue()
            sql_expect = self.expected_output.GetValue()
            # TODO: check for numeric values
            sql_types = "POLICY_VARCHAR"
            ncg_lib.gen_sql_audit_file(
                description,
                info,
                sql_request, 
                sql_types,
                sql_expect,
                filename,
            )
        elif self.type == "GROUP_MEMBERS_POLICY":
            value_type = "POLICY_TEXT"
            value_data = self.members_to_require.GetValue()
            group_name = self.group_name.GetValue()
            ncg_lib.gen_windows_group_audit(
                description,
                info,
                value_type,
                value_data, 
                group_name,
                filename,
            )
        elif self.type == "FILE_CONTENT_CHECK":
            value_type = "POLICY_TEXT"
            value_data = self.remote_file.GetValue()
            regex = expect = self.regex.GetValue()
            ncg_lib.gen_windows_file_audit(
                description,
                info,
                value_type,
                value_data, 
                regex,
                expect,
                filename,
            )
        self.file_save_text.SetLabel("File saved to %s" % filename)  
        event.Skip()
