from nose_parameterized import parameterized
from nose.tools import with_setup, raises, nottest
from mock import *
import sys
import imp
import libxml2
import re
from StringIO import StringIO

vapptool = imp.load_source('vapptool', './vapptool')

def call_main_with(*argv):
  saved_stdout = sys.stdout
  saved_stderr = sys.stdout

  try:
    out = StringIO()
    sys.stdout = out

    err = StringIO()
    sys.stderr = err

    vapptool.main(list(argv))

  except SystemExit, ex:
    return [ ex.code, out.getvalue().strip() or None, err.getvalue().strip() or None]

  finally:
    sys.stdout = saved_stdout
    sys.stdout = saved_stderr


# @nottest
# def capture_stdout(callback, out=sys.stdout, *callback_args):
#     from StringIO import StringIO
#     saved_stdout = out
#     try:
#         out = StringIO()
#         sys.stdout = out
#         if callback_args:
#             callback(callback_args)
#         else:
#             callback()
#         output = out.getvalue().strip()
#         return output
#     finally:
#         print('exception occured in capture_stdout')
#         sys.stdout = saved_stdout
