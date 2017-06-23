# nessus compliance generator
GUI program to generate Windows and SQL audit files for nessus

Using Nessus to audit Oracle SQL database configurations is fairly straightforward and only requires a few pieces to get moving.  The Nessus Compliance Generator (NCG) program has been supplied to assist in building compliance audits to plug in to Nessus.  The audit files themselves have a simple xml-like format.  Currently supported by our generator tool are the following types of audits:

1. Oracle database compliance: requires a SQL query and an expected output.
2. Windows group membership compliance: requires a group name and expected members.
3. Windows file contents compliance: requires a filename to check on a remote system and a regular expression to validate contents.

Compliance type 1 above requires database credentials to be entered into Nessus.  Types 2 and 3 require that SMB file sharing be enabled and require administrator credentials be entered into Nessus.  Note that all of the compliance checks we do are read-only queries and that the credentials need not be entered by the person conducting the audit.

Full documentation can be found in NCG_documentation.pdf
