from helper import *

@patch('vapptool.load_ovf')
@raises(Exception)
def test_cmd_inspect_with_no_ovfenv(mock_load_ovf):
  mock_load_ovf.side_effect = Exception('Boom!')
  vapptool.cmd_inspect()

@patch('vapptool.load_ovf')
def test_cmd_inspect_with_unknown_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/legacy-onprem.xml', 'r').read()
  actual = vapptool.cmd_inspect()

  assert actual[0] is not 0,    'cmd_inspect should return a non-zero status when an ovfEnv is found that does not contain Rally vApp properties'
  assert actual[1] is None,     'cmd_inspect should not return stdout'
  assert actual[2] is not None, 'cmd_inspect should return stderr text when an ovfEnv is found that does not contain Rally vApp properties'

@patch('vapptool.load_ovf')
def test_cmd_inspect_with_a_known_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/alm.xml', 'r').read()
  actual = vapptool.cmd_inspect()

  assert actual[0] is 0,    'cmd_inspect should return a zero status when an ovfEnv is found that contains Rally vApp properties'
  assert actual[1] is None, 'cmd_inspect should not return stdout'
  assert actual[2] is None, 'cmd_inspect should not return stderr text when an ovfEnv is found that contains Rally vApp properties'

@patch('vapptool.cmd_inspect')
def test_main_inspect(mock_cmd_inspect):
  mock_cmd_inspect.return_value = [ 0, 'stdout', 'stderr' ]

  actual = call_main_with('--inspect')

  assert actual[0] is 0,        '--inspect should exit zero'
  assert 'stdout' in actual[1], '--inspect should print stdout'
  assert 'stderr' in actual[2], '--inspect should not print stderr'


def test_main_inspect_with_wrong_options():
  actual = call_main_with('--inspect', '--wrongopt')

  assert actual[0] is not 0,      '--inspect should exit non-zero when called incorrectly'
  assert actual[1] is None,       '--inspect should not print stdout when called incorrectly'
  assert 'wrongopt' in actual[2], '--inspect should print stderr when called incorrectly'
