#Boa:Frame:ncg_file_generator
"""ncg_file_generator creates a nessus compliance audit file using 
user supplied data.
"""

__author__ = "thompsonm@anl.gov (Mike Thompson)"

import os
import wx
import wx.lib.stattext
import wx.lib.filebrowsebutton
import ncg_lib


def create(parent):
    """Create method to draw the window"""
    return ncg_file_generator(parent)

[wxID_NCG_FILE_GENERATOR, wxID_NCG_FILE_GENERATORAUDIT_TYPE, 
 wxID_NCG_FILE_GENERATOREXPECTED_OUTPUT, 
 wxID_NCG_FILE_GENERATOREXPECTED_OUTPUT_LABEL, 
 wxID_NCG_FILE_GENERATORFILENAME, wxID_NCG_FILE_GENERATORFILENAME_LABEL, 
 wxID_NCG_FILE_GENERATORFILE_SAVE_TEXT, wxID_NCG_FILE_GENERATORGROUP_NAME, 
 wxID_NCG_FILE_GENERATORGROUP_NAME_LABEL, 
 wxID_NCG_FILE_GENERATORLONG_DESCRIPTION, 
 wxID_NCG_FILE_GENERATORLONG_DESCRIPTION_LABEL, 
 wxID_NCG_FILE_GENERATORMEMBERS_TO_REQUIRE, wxID_NCG_FILE_GENERATORNEW, 
 wxID_NCG_FILE_GENERATORPATH, wxID_NCG_FILE_GENERATORREGEX, 
 wxID_NCG_FILE_GENERATORREGEX_LABEL, 
 wxID_NCG_FILE_GENERATORREMOTE_PATH_TO_CHECK, 
 wxID_NCG_FILE_GENERATORREMOTE_PATH_TO_CHECK_LABEL, 
 wxID_NCG_FILE_GENERATORREQUIRED_MEMBERS_LABEL, wxID_NCG_FILE_GENERATORSAVE, 
 wxID_NCG_FILE_GENERATORSHORT_DESCRIPTION, 
 wxID_NCG_FILE_GENERATORSHORT_DESCRIPTION_LABEL, 
 wxID_NCG_FILE_GENERATORSQL_QUERY, wxID_NCG_FILE_GENERATORSQL_QUERY_LABEL, 
] = [wx.NewId() for _init_ctrls in range(24)]


class ncg_file_generator(wx.Frame):
    """Our main class"""
    
    def _init_ctrls(self, prnt):
        """ Initialize controls """
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_NCG_FILE_GENERATOR,
              name=u'ncg_file_generator', parent=prnt, pos=wx.Point(527, 110),
              size=wx.Size(992, 568),
              style=wx.TAB_TRAVERSAL | wx.DEFAULT_FRAME_STYLE,
              title=u'Nessus Compliance Generator: New Audit File')
        self.SetClientSize(wx.Size(992, 568))
        self.SetBackgroundColour(wx.Colour(237, 237, 237))

        self.audit_type = wx.RadioBox(choices=['Oracle SQL',
              'Windows Group Membership', 'Windows File Contents'],
              id=wxID_NCG_FILE_GENERATORAUDIT_TYPE, label=u'Nessus Audit Type',
              majorDimension=1, name=u'audit_type', parent=self, pos=wx.Point(8,
              0), size=wx.Size(248, 128), style=wx.RA_SPECIFY_COLS)
        self.audit_type.SetStringSelection(u'SQL')
        self.audit_type.Bind(wx.EVT_RADIOBOX, self.OnAudit_typeRadiobox,
              id=wxID_NCG_FILE_GENERATORAUDIT_TYPE)

        self.path = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='Browse',
              dialogTitle=u'Select a directory to save in',
              id=wxID_NCG_FILE_GENERATORPATH, labelText='Select a directory:',
              newDirectory=False, parent=self, pos=wx.Point(456, 496),
              size=wx.Size(296, 48), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip='Type directory name or browse to select')
        self.path.SetName(u'path')
        self.path.SetBackgroundColour(wx.Colour(237, 237, 237))

        self.save = wx.Button(id=wxID_NCG_FILE_GENERATORSAVE, label=u'Save',
              name=u'save', parent=self, pos=wx.Point(768, 504),
              size=wx.Size(96, 32), style=0)
        self.save.Bind(wx.EVT_BUTTON, self.OnSaveButton,
              id=wxID_NCG_FILE_GENERATORSAVE)

        self.new = wx.Button(id=wxID_NCG_FILE_GENERATORNEW, label=u'New',
              name=u'new', parent=self, pos=wx.Point(880, 504), size=wx.Size(96,
              32), style=0)
        self.new.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_NCG_FILE_GENERATORNEW)

        self.file_save_text = wx.lib.stattext.GenStaticText(ID=wxID_NCG_FILE_GENERATORFILE_SAVE_TEXT,
              label=u'', name=u'file_save_text', parent=self, pos=wx.Point(8,
              544), size=wx.Size(968, 17), style=0)
        self.file_save_text.SetBackgroundColour(wx.Colour(237, 237, 237))

        self.filename = wx.TextCtrl(id=wxID_NCG_FILE_GENERATORFILENAME,
              name=u'filename', parent=self, pos=wx.Point(320, 504),
              size=wx.Size(120, 32), style=0, value=u'')

        self.filename_label = wx.StaticText(id=wxID_NCG_FILE_GENERATORFILENAME_LABEL,
              label=u'Filename:', name=u'filename_label', parent=self,
              pos=wx.Point(248, 512), size=wx.Size(64, 17), style=0)

        self.short_description = wx.TextCtrl(id=wxID_NCG_FILE_GENERATORSHORT_DESCRIPTION,
              name=u'short_description', parent=self, pos=wx.Point(432, 8),
              size=wx.Size(536, 32), style=0, value=u'')

        self.long_description = wx.TextCtrl(id=wxID_NCG_FILE_GENERATORLONG_DESCRIPTION,
              name=u'long_description', parent=self, pos=wx.Point(432, 56),
              size=wx.Size(536, 144), style=wx.TE_MULTILINE,
              value=u'')

        self.sql_query = wx.TextCtrl(id=wxID_NCG_FILE_GENERATORSQL_QUERY,
              name=u'sql_query', parent=self, pos=wx.Point(432, 216),
              size=wx.Size(536, 152), style=wx.TE_MULTILINE,
              value=u'')

        self.expected_output = wx.TextCtrl(id=wxID_NCG_FILE_GENERATOREXPECTED_OUTPUT,
              name=u'expected_output', parent=self, pos=wx.Point(432, 384),
              size=wx.Size(536, 32), style=0, value=u'')

        self.short_description_label = wx.StaticText(id=wxID_NCG_FILE_GENERATORSHORT_DESCRIPTION_LABEL,
              label=u'Short Description:', name=u'short_description_label',
              parent=self, pos=wx.Point(304, 16), size=wx.Size(117, 17),
              style=0)

        self.long_description_label = wx.StaticText(id=wxID_NCG_FILE_GENERATORLONG_DESCRIPTION_LABEL,
              label=u'Long Description:', name=u'long_description_label',
              parent=self, pos=wx.Point(304, 64), size=wx.Size(114, 17),
              style=0)

        self.sql_query_label = wx.StaticText(id=wxID_NCG_FILE_GENERATORSQL_QUERY_LABEL,
              label=u'SQL Query:', name=u'sql_query_label', parent=self,
              pos=wx.Point(344, 232), size=wx.Size(72, 17), style=0)

        self.expected_output_label = wx.StaticText(id=wxID_NCG_FILE_GENERATOREXPECTED_OUTPUT_LABEL,
              label=u'Expected Output:', name=u'expected_output_label',
              parent=self, pos=wx.Point(304, 392), size=wx.Size(113, 17),
              style=0)

        self.remote_path_to_check = wx.TextCtrl(id=wxID_NCG_FILE_GENERATORREMOTE_PATH_TO_CHECK,
              name=u'remote_path_to_check', parent=self, pos=wx.Point(384, 248),
              size=wx.Size(584, 32), style=0, value=u'')

        self.remote_path_to_check_label = wx.StaticText(id=wxID_NCG_FILE_GENERATORREMOTE_PATH_TO_CHECK_LABEL,
              label=u'Remote File (Full Path) To Check:',
              name=u'remote_path_to_check_label', parent=self, pos=wx.Point(192,
              256), size=wx.Size(190, 15), style=0)

        self.regex = wx.TextCtrl(id=wxID_NCG_FILE_GENERATORREGEX, name=u'regex',
              parent=self, pos=wx.Point(384, 288), size=wx.Size(584, 31),
              style=0, value=u'')

        self.regex_label = wx.StaticText(id=wxID_NCG_FILE_GENERATORREGEX_LABEL,
              label=u'Regex to Find in File:', name=u'regex_label', parent=self,
              pos=wx.Point(256, 296), size=wx.Size(116, 15), style=0)

        self.group_name = wx.TextCtrl(id=wxID_NCG_FILE_GENERATORGROUP_NAME,
              name=u'group_name', parent=self, pos=wx.Point(432, 216),
              size=wx.Size(272, 32), style=0, value=u'')

        self.group_name_label = wx.StaticText(id=wxID_NCG_FILE_GENERATORGROUP_NAME_LABEL,
              label=u'Group to Check:', name=u'group_name_label', parent=self,
              pos=wx.Point(328, 224), size=wx.Size(95, 17), style=0)

        self.members_to_require = wx.TextCtrl(id=wxID_NCG_FILE_GENERATORMEMBERS_TO_REQUIRE,
              name=u'members_to_require', parent=self, pos=wx.Point(432, 256),
              size=wx.Size(520, 32), style=0, value=u'')

        self.required_members_label = wx.StaticText(id=wxID_NCG_FILE_GENERATORREQUIRED_MEMBERS_LABEL,
              label=u'Members to Require:', name=u'required_members_label',
              parent=self, pos=wx.Point(296, 264), size=wx.Size(128, 17),
              style=0)

    def __init__(self, parent):
        """init method 
        
        defaults to showing only controls for the SQL mode.
        """
        self._init_ctrls(parent)
        self.remote_path_to_check.Show(False)
        self.remote_path_to_check_label.Show(False)
        self.regex.Show(False)
        self.regex_label.Show(False)
        self.group_name.Show(False) 
        self.group_name_label.Show(False)
        self.members_to_require.Show(False)
        self.required_members_label.Show(False)
        
    def hide_all(self):
        """Hides all controls that aren't global"""
        self.sql_query.Show(False)
        self.sql_query_label.Show(False)
        self.expected_output.Show(False)
        self.expected_output_label.Show(False)
        self.remote_path_to_check.Show(False)
        self.remote_path_to_check_label.Show(False)
        self.regex.Show(False)
        self.regex_label.Show(False)
        self.group_name.Show(False) 
        self.group_name_label.Show(False)
        self.members_to_require.Show(False)
        self.required_members_label.Show(False)

    def OnAudit_typeRadiobox(self, event):
        """Handler for radiobox selection"""
        print "[debug]: dir(event.GetSelection()) %s event.GetSelection() %s" % (dir(event.GetSelection()), event.GetSelection())
        if event.GetSelection() == 0:
            self.hide_all()
            self.sql_query.Show(True)
            self.sql_query_label.Show(True)
            self.expected_output.Show(True)
            self.expected_output_label.Show(True)
        if event.GetSelection() == 1:
            self.hide_all()
            self.group_name.Show(True) 
            self.group_name_label.Show(True)
            self.members_to_require.Show(True)
            self.required_members_label.Show(True)
        elif event.GetSelection() == 2:
            self.hide_all()
            self.remote_path_to_check.Show(True)
            self.remote_path_to_check_label.Show(True)
            self.regex.Show(True)
            self.regex_label.Show(True)
        event.Skip()

    def OnButton2Button(self, event):
        """Handler for "new" button"""
        self.filename.SetValue('')
        self.short_description.SetValue('')
        self.long_description.SetValue('')
        self.sql_query.SetValue('')
        self.expected_output.SetValue('')
        self.remote_path_to_check.SetValue('')
        self.regex.SetValue('')
        self.group_name.SetValue('')
        self.members_to_require.SetValue('')
        event.Skip()

    def OnSaveButton(self, event):
        """Handler for save button"""
        # TODO: error check missing fields
        # TODO: handle different filetypes
        audit_type = self.audit_type.GetSelection()
        print "[debug]: self.path.GetValue() %s" % self.path.GetValue()
        filename = os.path.join(self.path.GetValue(), self.filename.GetValue())
        info = self.long_description.GetValue()
        description = self.short_description.GetValue()
        if audit_type == 0:
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
        elif audit_type == 1:
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
        elif audit_type == 2:
            value_type = "POLICY_TEXT"
            value_data = self.remote_path_to_check.GetValue()
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
