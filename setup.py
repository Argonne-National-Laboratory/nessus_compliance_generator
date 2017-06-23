#!/usr/bin/env python2
"""
Simple setup script to be used (on a windows machine) to generate an .exe file.

Must run with Python 2.x

In order to build the exe file, run python.exe setup.py py2exe in the directory
that contains both this setup file and nessus_sql_gen.py
"""
__author__ = "thompsonm@anl.gov (Mike Thompson)"

from distutils.core import setup
import py2exe

manifest = """
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<assembly xmlns='urn:schemas-microsoft-com:asm.v1' manifestVersion='1.0'>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level='asInvoker' uiAccess='false' />
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
     type='win32'
     name='Microsoft.VC90.CRT'
     version='9.0.21022.8'
     processorArchitecture='*'
     publicKeyToken='1fc8b3b9a1e18e3b' />
    </dependentAssembly>
  </dependency>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
         type="win32"
         name="Microsoft.Windows.Common-Controls"
         version="6.0.0.0"
         processorArchitecture="*"
         publicKeyToken="6595b64144ccf1df"
         language="*" />
    </dependentAssembly>
  </dependency>
</assembly>
"""

setup(
  #options = {'py2exe': {'bundle_files': 1}},
  options = {
            "py2exe":{
            "dll_excludes": ["MSVCP90.dll"],
        }
    },
  zipfile = None,
  windows = [
    { "script": "ncg.py",
      "version": "0.2",
      "company_name" : "Argonne National Laboratory",
      "copyright" : "2014",
      "name" : "Nessus Compliance Generator",
      "icon_resources" : [(1, "ncg.ico")],
      "other_resources" : [(24, 1, manifest)],
      "dest_base": "ncg",
    }
  ], data_files=["ncg.ico"]
)
