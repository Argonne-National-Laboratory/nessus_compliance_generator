#!/usr/bin/python
"""
Program to ease generating XML files required for NESSUS database compliance
audits for Oracle.  
"""

author = "thompsonm@anl.gov (Mike Thompson)"

import argparse
import sys

#GLOBAL VARS for Oracle - These may need to change for your database!
DB_TYPE = "Oracle"
VERSION = 1
GROUP_POLICY = "Test"


def gen_preamble(check_type):
  """
  Just puts the first lines of a properly formatted audit file into a list
  and returns that list.  Uses globals CHECK_TYPE, DB_TYPE, and VERSION
  
  Returns:
    A list of strings to be put at the beginning of an audit file.
  """
  out = []
  out.append(' ')
  check_type_tag = '<check_type: "%s" ' % check_type
  if check_type == "Database": # sql
    check_type_tag += 'db_type:"%s" version:"%d">' % \
             (DB_TYPE, VERSION)
  elif check_type == "Windows":
    check_type_tag += 'version: "2">'
  out.append(check_type_tag)
  out.append('  <group_policy: "%s">' % GROUP_POLICY)
  out.append(' ')
  return out

def gen_custom_item_sql(description, info, sql_request, sql_types, sql_expect):
  """
  Puts the main data stanza of a SQL audit file into a list for file generation.
  This could be used to generate multiple audit files.  Just start the file with
  the info in gen_preamble, run this function several times with different input
  and finish with gen closure.  We don't do that here, but probably for future
  implementation.

  Args:
    description: string that is a one line description of the query's purpose
    info: string that is a longer description of the query's purpose
    sql_request: string that is a sql query (no error checking performed)
    sql_types: string that is a SQL policy datatype, probably POLICY_VARCHAR
      or POLICY_INTEGER
    sql_expect: string, integer, or NULL, as appropriate -- what the sql
      query should return to signal a pass
  
  Returns:
    A list of strings to put in the main body of a SQL audit file.
  """
  # TODO: use xml gen functions?
  out = []
  out.append('')
  out.append('<custom_item>')
  out.append('  type: SQL_POLICY')
  out.append('  description: "%s"' % description.replace("\n", " "))
  out.append('  info: "%s"' % info.replace("\n", " "))
  out.append('  sql_request: "%s"' % sql_request.replace("\n", " "))
  out.append('  sql_types: %s' % sql_types)
  if sql_expect.upper() == "NULL":
    out.append('  sql_expect: NULL')
  else:
    out.append('  sql_expect: "%s"' % sql_expect)
  out.append('</custom_item>')
  out.append(' ')
  return out

def gen_custom_item_windows_file(description, info, value_type, value_data, 
  regex, expect):
  """Generates a custom item stanza for windows file contents audit

  Args:
    description: string, a description of the audit
    info:	 string, info about the audit
    value_type:	 string, "POLICY_TEXT" -- included for parity with other 
 	gen_* modules.
    value_data:  string, location of remote file to check
    regex: 	 string, regular expression to check file for
    expect:	 string, regular expression to match for a pass

  Returns:
    A list of strings to put in the main body of a Windows file audit file.
  """
  out = []
  out.append('')
  out.append('<custom_item>')
  out.append('  type: FILE_CONTENT_CHECK')
  out.append('  description: "%s"' % description.replace("\n", " "))
  out.append('  info: "%s"' % info.replace("\n", " "))
  out.append('  value_type: %s' % value_type)
  out.append('  value_data: "%s"' % value_data)
  out.append('  regex: "%s"' % regex)
  out.append('  expect: "%s"' % expect)
  out.append('</custom_item>')
  out.append(' ')
  return out

def gen_custom_item_windows_group(description, info, value_type, members,
  group_name):
  """
  Generates a custom item stanza for a windows group membership audit
 
  Args:
    description: string, a description of the audit
    info:        string, info about the audit
    value_type:  string, "POLICY_TEXT" -- included for parity with other 
        gen_* modules.
    members: 	 list, list of members that should be validated
    group_name:  string, name of the windows group
  
  Returns:
    list of strings, one for each line in the stanza to be outputted
  """
  members = members.split(',')
  out = []
  out.append('<custom_item>')
  out.append('  type: GROUP_MEMBERS_POLICY')
  out.append('  description: "%s"' % description.replace("\n", " "))
  out.append('  info: "%s"' % info.replace("\n", " "))
  out.append('  value_type: POLICY_TEXT')
  value_data = '"%s"' % members[0]
  if len(members) == 1 and members[0].find("||") > -1:
    members = '"%s"' % members
  elif len(members) > 1:
    for member in members[1:]:
      value_data += ' || "%s"' % member
  out.append('  value_data: %s' % value_data)
  out.append('  group_name: "%s"' % group_name)
  out.append('</custom_item>')
  out.append(' ')
  return out


def gen_closure():
  """
  Just prints out the closure tags for the audit file (to a list)

  Returns:
    A list of strings to close a SQL audit file for nessus.
  """
  out = []
  out.append(' ' )
  out.append('  </group_policy>')
  out.append('</check_type>')
  out.append(' ') 
  return out


def gen_sql_audit_file(description, info, sql_request, sql_types, sql_expect, 
  filename):
  """
  Does the work to actually print the SQL audit file.

  Args:
      description: string that is a one line description of the query's purpose
      info: string that is a longer description of the query's purpose
      sql_request: string that is a sql query (no error checking performed)
      sql_types: string that is a SQL policy datatype, probably POLICY_VARCHAR
        or POLICY_INTEGER
      sql_expect: string, integer, or NULL, as appropriate -- what the sql
        query should return to signal a pass
      filename: a filename provided by the user where the new file should be
        created

  Doesn't return anything, but writes the file and prints status to the console.
  """
  with open('%s' % filename, 'w') as f:
    f.write("\n".join(gen_preamble("Database")))
    f.write("    \n".join(gen_custom_item_sql(
      description, info, sql_request, sql_types, sql_expect)).encode("ascii", "ignore"))
    f.write("\n".join(gen_closure()))
  print "file written to: %s" % filename 
  
def gen_windows_file_audit(description, info, value_type, value_data, regex, 
  expect, filename):
  with open('%s' % filename, 'w') as f:
    f.write("\n".join(gen_preamble("Windows")))
    f.write("    \n".join(gen_custom_item_windows_file(
      description, info, value_type, value_data, regex, expect)).encode("ascii", "ignore"))
    f.write("\n".join(gen_closure()))
  print "file written to: %s" % filename 

def gen_windows_group_audit(description, info, value_type, value_data, 
  group_name, filename):
  with open('%s' % filename, 'w') as f:
    f.write("\n".join(gen_preamble("Windows")))
    f.write("    \n".join(gen_custom_item_windows_group(
      description, info, value_type, value_data, group_name)).encode("ascii", "ignore"))
    f.write("\n".join(gen_closure()))
  print "file written to: %s" % filename


def combine_files(audit_type, files, new_name):
  """
  Does the work to combine several individual audit files into one combined
  audit file.

  Args:
    files: a list of valid filenames (we don't do error checking)
    new_name: filename for the new combined filename.

  Doesn't return anything but writes the file to disk and prints success to the 
  console.
  """
  newfile = []
  newfile.append(gen_preamble(audit_type))
  for filename in files:
    with open(filename, 'rb') as f:
      for line in f.readlines():
        no_space = line.strip()
        if (not no_space.startswith("<check_type") 
          and not no_space.startswith("<group_policy")
          and not no_space.startswith("</check_type")
          and not no_space.startswith("</group_policy")):
       
          newfile.append([line])
      # end for
    # end with  
  # end for
  newfile.append(gen_closure())
  with open('%s' % new_name, 'w') as f:
    for line in newfile:
      f.write("\n".join(line))
  print "file written to: %s" % new_name 


def parse_audit_file(filename):
  """ Parses a nessus audit file created by the ncg tools and returns
  relevant data for ncg_editor.py

  Args:
    filename - string, filename or full path to pass to open

  Returns:
    A dictionary like one of the following (depending on the audit type found
    in the opened file):
      { audit_type:(description, info, sql_request, sql_expect) }
      { windows_type:(description, info, value_data, group_name) }
      { windows_type:(description, info, value_data, regex) }
  """
  lines = []
  with open (filename, 'rb') as f:
    for line in f.readlines():
      print "[debug1]: read %s" % line
      lines.append(line)
    #lines = f.read().split("\n")

  audit_type = ""
  windows_type = ""
  description=info=sql_request=sql_expect=value_data=group_name=regex=""
  for line in lines:
    print "[debug]: read %s" % line
    if line.find("check_type") >= 0:
      print "check_type"
      if line.find("Database") >= 0:
        audit_type = "Database"
      if line.find("Windows") >= 0:
        # we'll get more specific on the next line
        audit_type = "Windows"
    # exclusive with above   
    if line.find("type") >= 0 and line.find("value_type") == -1 and \
      line.find("check_type") == -1:
      windows_type = line.replace("type:", "").strip()
    if line.find("description") >= 0:
      description = line.replace("description:", "").strip().strip("\"")
    if line.find("info") >= 0:
      info = line.replace("info:", "").strip().strip("\"")
    if line.find("sql_request") >= 0:
      sql_request = line.replace("sql_request:", "").strip().strip("\"")
    if line.find("sql_expect") >= 0:
      sql_expect = line.replace("sql_expect:", "").strip().strip("\"")
    if line.find("value_data") >= 0:
      value_data = line.replace("value_data:", "").replace(" || ", ",").replace("\"", "").strip()
    if line.find("regex") >= 0:
      regex = line.replace("regex:", "").strip().strip("\"")
    if line.find("group_name") >= 0:
      group_name = line.replace("group_name:", "").strip().strip("\"")

  if audit_type == "Database":
     retval = { audit_type:
       (description, info, sql_request, sql_expect) }
  else:
    retval = {}
    if windows_type == "GROUP_MEMBERS_POLICY":
      retval = { windows_type:
        (description, info, value_data, group_name) }
    elif windows_type == "FILE_CONTENT_CHECK":
      retval =  { windows_type:
        (description, info, value_data, regex) }
  print "[debug]: returning %s" % retval
  return retval
