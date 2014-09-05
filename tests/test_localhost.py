from helper import *

@patch('vapptool.load_ovf')
@raises(Exception)
def test_cmd_localhost_with_no_ovfenv(mock_load_ovf):
  mock_load_ovf.side_effect = Exception('Boom!')
  vapptool.cmd_localhost()

@patch('vapptool.load_ovf')
@raises(Exception)
def test_cmd_localhost_with_unknown_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/legacy-onprem.xml', 'r').read()

  actual = vapptool.cmd_localhost()

@patch('vapptool.load_ovf')
def test_cmd_localhost_with_a_known_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/alm.xml', 'r').read()
  expected_stdout = '10.32.30.29'

  actual = vapptool.cmd_localhost()

  assert actual[0] is 0,               'cmd_localhost should return a zero status when an ovfEnv is found that contains Rally vApp properties'
  assert actual[1] == expected_stdout, "cmd_localhost should return an ip address on stdout when an ovfEnv is found that contains Rally vApp properties.  Expected [%s], got [%s]." %(expected_stdout, actual[1])
  assert actual[2] is None,            'cmd_localhost should not return stderr when an ovfEnv is found that contains Rally vApp properties'

@patch('vapptool.cmd_localhost')
def test_main_localhosts(mock_cmd_localhost):
  mock_cmd_localhost.return_value = [ 0, 'stdout', 'stderr' ]

  actual = call_main_with('--localhost')

  assert actual[0] is 0,        '--localhosts should exit zero'
  assert 'stdout' in actual[1], '--localhosts should print stdout'
  assert 'stderr' in actual[2], '--localhosts should not print stderr'


def test_main_localhosts_with_wrong_options():
  actual = call_main_with('--localhost', '--wrongopt')

  assert actual[0] is not 0,      '--localhost should exit non-zero when called incorrectly'
  assert actual[1] is None,       '--localhost should not print stdout when called incorrectly'
  assert 'wrongopt' in actual[2], '--localhost should print stderr when called incorrectly'
