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
