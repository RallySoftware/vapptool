from helper import *

@patch('vapptool.load_ovf')
@raises(Exception)
def test_cmd_property_with_no_ovfenv(mock_load_ovf):
  mock_load_ovf.side_effect = Exception('Boom!')
  vapptool.cmd_property()

@patch('vapptool.load_ovf')
def test_cmd_property_with_any_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/alm.xml', 'r').read()
  expected_stdout = '10.32.0.9'

  actual = vapptool.cmd_property('dns1')

  assert actual[0] is 0,               'cmd_property should return zero status when an ovfEnv is found that contains the property asked for'
  assert actual[1] == expected_stdout, "cmd_property should return the property value on stdout when an ovfEnv is found that contains the property asked for.  Expected [%s], got [%s]." %(expected_stdout, actual[1])
  assert actual[2] is None,            'cmd_property should not return stderr when an ovfEnv is found that contains the property asked for'

@patch('vapptool.load_ovf')
def test_cmd_property_with_any_ovfenv_missing_property(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/alm.xml', 'r').read()

  actual = vapptool.cmd_property('xyz123')

  assert actual[0] is not 0,    'cmd_property should return non-zero status when an ovfEnv is found that does not contain the property asked for'
  assert actual[1] is None,     'cmd_property should not stdout when an ovfEnv is found that does not contain the property asked for.'
  assert actual[2] is not None, 'cmd_property should return stderr when an ovfEnv is found that does not contain the property asked for'
