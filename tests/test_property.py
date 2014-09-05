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

@patch('vapptool.cmd_property')
def test_main_property(mock_cmd_property):
  mock_cmd_property.return_value = [ 0, 'stdout', 'stderr' ]

  actual = call_main_with('--property=foo')

  assert actual[0] is 0,        '--property should exit zero'
  assert 'stdout' in actual[1], '--property should print stdout'
  assert 'stderr' in actual[2], '--property should not print stderr'

def test_main_property_without_property_name():
  actual = call_main_with('--property')

  assert actual[0] is not 0,    '--property should exit non-zero when called without a property name'
  assert actual[1] is None,     '--property should not print stdout when called without a property name'
  assert actual[2] is not None, '--property should print stderr when called without a property name'

def test_main_property_with_wrong_options():
  actual = call_main_with('--property=bar', '--wrongopt')

  assert actual[0] is not 0,      '--property should exit non-zero when called incorrectly'
  assert actual[1] is None,       '--property should not print stdout when called incorrectly'
  assert 'wrongopt' in actual[2], '--property should print stderr when called incorrectly'
