=================
Base Pretty Print
=================

Base module that provide display functions on the base model.

The method `pprint` is a close equivalent to `read()`,
except it truncates every text field to at most `limit` characters (defaults to 300),
and replace set binary fields value by the string "Binary file".

The method `pwrite` writes this result to a text file to `/tmp`,
with the possibility to choose the name/folder as named arguments.

self.env['res.partner'].search([], limit=1).pprint()