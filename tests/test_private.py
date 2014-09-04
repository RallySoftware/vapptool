from nose_parameterized import parameterized
from nose.tools import with_setup, raises
from mock import *
import imp
import libxml2

vapptool = imp.load_source('vapptool', './vapptool')

@patch('vapptool.ovf_xpath')
def test_ovf_property_with_a_single_found_value(mock_ovf_xpath):
  expected = 'a value'
  mock_ovf_xpath.return_value = [ MagicMock(spec=libxml2.xmlAttr) ]
  mock_ovf_xpath.return_value[0].get_content.return_value = expected
  actual = vapptool.ovf_property('a_prop')
  assert actual is expected, "cmd_property should return a string when a single matching property is found in the ovfEnv.  Expected [%s], got [%s]." %(expected, actual)

@patch('vapptool.ovf_xpath')
@raises(Exception)
def test_ovf_property_with_multiple_found_values(mock_ovf_xpath):
  mock_ovf_xpath.return_value = [ MagicMock(spec=libxml2.xmlAttr), MagicMock(spec=libxml2.xmlAttr) ]
  vapptool.ovf_property('a_prop')

@patch('vapptool.ovf_xpath')
def test_ovf_property_with_no_values_found(mock_ovf_xpath):
  expected = None
  mock_ovf_xpath.return_value = [ ]
  actual = vapptool.ovf_property('a_prop')
  assert actual is expected, "cmd_property should return None when a no matching property is found in the ovfEnv.  Expected [%s], got [%s]." %(expected, actual)
