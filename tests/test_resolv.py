from helper import *

@patch('vapptool.load_ovf')
@raises(Exception)
def test_cmd_resolv_with_no_ovfenv(mock_load_ovf):
  mock_load_ovf.side_effect = Exception('Boom!')
  vapptool.cmd_resolv()

@patch('vapptool.load_ovf')
def test_cmd_resolv_with_unknown_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/legacy-onprem.xml', 'r').read()

  actual = vapptool.cmd_resolv()

  assert isinstance(actual, list), 'cmd_resolv should return a list'
  assert len(actual) is 3,         'cmd_resolv should return a list of 3 items'
  assert actual[0] is not 0,       'cmd_resolv should return a non-zero status when an ovfEnv is found that does not contain Rally vApp properties'
  assert actual[1] is None,        'cmd_resolv should not return stdout when an ovfEnv is found that does not contain Rally vApp properties'
  assert actual[2] is not None,    'cmd_resolv should return stderr when an ovfEnv is found that does not contain Rally vApp properties'


@patch('vapptool.load_ovf')
def test_cmd_resolv_with_a_known_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/alm.xml', 'r').read()
  expected_stdout = '10.32.30.29'

  actual = vapptool.cmd_resolv()

  assert isinstance(actual, list), 'cmd_resolv should return a list'
  assert len(actual) is 3,         'cmd_resolv should return a list of 3 items'
  assert actual[0] is 0,           'cmd_resolv should return a zero status when an ovfEnv is found that contains Rally vApp properties'
  assert actual[2] is None,        'cmd_resolv should not return stderr when an ovfEnv is found that contains Rally vApp properties'

  stdout = actual[1]
  assert re.search('Auto-generated by Rally vapptool', stdout) is not None, 'cmd_resolv stdout should contain the auto-generated comment'
  assert re.search('domain f4tech.com', stdout)                is not None, 'cmd_resolv stdout should contain a domain directive'
  assert re.search('nameserver 10.32.0.9', stdout)             is not None, 'cmd_resolv stdout should contain a nameserver directive for dns1'
  assert re.search('nameserver 10.32.0.13', stdout)            is not None, 'cmd_resolv stdout should contain a nameserver directive for dns2'

@patch('vapptool.cmd_resolv')
def test_main_resolv(mock_cmd_resolv):
  mock_cmd_resolv.return_value = [ 0, 'stdout', 'stderr' ]

  actual = call_main_with('--resolv')

  assert actual[0] is 0,        '--resolv should exit zero'
  assert 'stdout' in actual[1], '--resolv should print stdout'
  assert 'stderr' in actual[2], '--resolv should not print stderr'

def test_main_resolv_with_wrong_options():
  actual = call_main_with('--resolv', '--wrongopt')

  assert actual[0] is not 0,      '--resolv should exit non-zero when called incorrectly'
  assert actual[1] is None,       '--resolv should not print stdout when called incorrectly'
  assert 'wrongopt' in actual[2], '--resolv should print stderr when called incorrectly'
