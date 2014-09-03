from nose_parameterized import parameterized
from nose.tools import with_setup, raises
from mock import *
import imp

import libxml2

vapptool = imp.load_source('vapptool', './vapptool')

@patch('vapptool.load_ovf')
@raises(TypeError)
def test_cmd_inspect_without_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = False
  assert vapptool.cmd_inspect() is False

@patch('vapptool.load_ovf')
def test_cmd_inspect_with_unknown_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/legacy-onprem.xml', 'r').read()
  assert vapptool.cmd_inspect() is False

@patch('vapptool.load_ovf')
def test_cmd_inspect_with_compliant_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/alm.xml', 'r').read()
  assert vapptool.cmd_inspect() is True

@patch('vapptool.ovf_property')
def test_cmd_inspect_ovf_property_returns_a_known_value(mock_ovf_property):

  # here we have to create an additional mock to prevent an Exception from
  # being thrown when we call load_ovf.
  patch_load_ovf = patch('vapptool.load_ovf')
  mock_load_ovf = patch_load_ovf.start()
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/alm.xml', 'r').read()
  mock_load_ovf.stop()


  # TODO: Are we actually forcing this test to pass here or are we
  # actually testing that this code works correctly?
  #  if vm_name:
  #      result = vm_name[0]
  #
  #      if result and result.get_content():
  #         return True
  mock_ovf_property.return_value = [ MagicMock(spec=libxml2.xmlAttr) ]
  ovf_property_return_value = mock_ovf_property.return_value[0]
  ovf_property_return_value.get_content.return_value = 'alm'

  vapptool.cmd_inspect()

  assert mock_ovf_property.called, 'Expected that .ovf_property function is called'
  assert isinstance(mock_ovf_property.return_value[0], libxml2.xmlAttr), 'Expected ovf_property to be a %s, but we got %s' %(libxml2.xmlAttr, type(mock_ovf_property.return_value[0]))
  assert mock_ovf_property.return_value[0].get_content.called and mock_ovf_property.return_value[0].get_content.return_value == 'alm'