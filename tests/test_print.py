from helper import *

@patch('vapptool.load_ovf')
@raises(Exception)
def test_cmd_printovf_with_no_ovfenv(mock_load_ovf):
  mock_load_ovf.side_effect = Exception('Boom!')
  vapptool.cmd_printovf()

@patch('vapptool.load_ovf')
def test_cmd_printovf_with_any_ovfenv(mock_load_ovf):
  mock_load_ovf.return_value = file('tests/fixtures/ovfenv/legacy-onprem.xml', 'r').read()
  expected_stdout = mock_load_ovf.return_value

  actual = vapptool.cmd_printovf()

  assert actual[0] is 0,                'cmd_printovf should return a zero status when an ovfEnv is found'
  assert actual[1] is expected_stdout,  'cmd_printovf should return the ovfEnv in stdout'
  assert actual[2] is None,             'cmd_printovf should not return stderr text when an ovfEnv is found'

@patch('vapptool.cmd_printovf')
def test_main_print(mock_cmd_printovf):
  mock_cmd_printovf.return_value = [ 0, 'stdout', 'stderr' ]

  actual = call_main_with('--print')

  assert actual[0] is 0,        '--print should exit zero'
  assert 'stdout' in actual[1], '--print should print stdout'
  assert 'stderr' in actual[2], '--print should not print stderr'


def test_main_print_with_wrong_options():
  actual = call_main_with('--print', '--wrongopt')

  assert actual[0] is not 0,      '--print should exit non-zero when called incorrectly'
  assert actual[1] is None,       '--print should not print stdout when called incorrectly'
  assert 'wrongopt' in actual[2], '--print should print stderr when called incorrectly'
