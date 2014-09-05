from helper import *

@patch('vapptool.load_ovf')
@raises(Exception)
def test_cmd_sysconfig_network_with_no_ovfenv(mock_load_ovf):
  mock_load_ovf.side_effect = Exception('Boom!')
  vapptool.cmd_sysconfig_network()

@patch('vapptool.load_sysconfig_network')
@raises(Exception)
def test_cmd_sysconfig_network_with_no_etc_sysconfig_network(mock_load_sysconfig_network):
  mock_load_sysconfig_network.side_effect = Exception('Bam!')
  vapptool.cmd_sysconfig_network()

@patch('vapptool.load_ovf')
@patch('vapptool.load_sysconfig_network')
def test_cmd_sysconfig_network_with_an_unknown_ovfenv(mock_load_sysconfig_network, mock_load_ovf):
  mock_load_sysconfig_network.return_value = file('tests/fixtures/centos6/sysconfig_network.orig', 'r').read()
  mock_load_ovf.return_value   = file('tests/fixtures/ovfenv/legacy-onprem.xml', 'r').read()

  actual = vapptool.cmd_sysconfig_network()

  assert actual[0] is not 0,    'cmd_sysconfig_network should return a non-zero status when an ovfEnv is found that does not contain Rally vApp properties'
  assert actual[1] is None,     'cmd_sysconfig_network should not return stdout when an ovfEnv is found that does not contain Rally vApp properties'
  assert actual[2] is not None, 'cmd_sysconfig_network should return stderr when an ovfEnv is found that does not contain Rally vApp properties'

@patch('vapptool.load_ovf')
@patch('vapptool.load_sysconfig_network')
def test_cmd_sysconfig_network_with_default_sysconfig_network_and_a_known_ovfenv(mock_load_sysconfig_network, mock_load_ovf):
  mock_load_sysconfig_network.return_value = file('tests/fixtures/centos6/sysconfig_network.orig', 'r').read()
  mock_load_ovf.return_value   = file('tests/fixtures/ovfenv/alm-core.xml', 'r').read()

  actual = vapptool.cmd_sysconfig_network()

  assert actual[0] is 0,    'cmd_sysconfig_network should return a zero status when an ovfEnv is found that contains Rally vApp properties'
  assert actual[2] is None, 'cmd_sysconfig_network should not return stderr when an ovfEnv is found that does not contain Rally vApp properties'

  stdout = actual[1]
  assert 'NETWORKING=yes' in stdout,               'cmd_sysconfig_network stdout should contain the contents of the original /etc/sysconfig/network file'
  assert 'HOSTNAME=vapp_alm.f4tech.com' in stdout, 'cmd_sysconfig_network stdout should contain a HOSTNAME entry for vapp_alm'


@patch('vapptool.load_ovf')
@patch('vapptool.load_sysconfig_network')
def test_cmd_sysconfig_network_with_modified_sysconfig_network_and_a_known_ovfenv(mock_load_sysconfig_network, mock_load_ovf):
  mock_load_sysconfig_network.return_value = file('tests/fixtures/centos6/sysconfig_network.orig', 'r').read()
  mock_load_ovf.return_value   = file('tests/fixtures/ovfenv/alm-core.xml', 'r').read()

  first_run = vapptool.cmd_sysconfig_network()
  mock_load_sysconfig_network.return_value = first_run[1]

  actual = vapptool.cmd_sysconfig_network()

  assert actual[0] is 0,    'cmd_sysconfig_network should return a zero status when an ovfEnv is found that contains Rally vApp properties'
  assert actual[2] is None, 'cmd_sysconfig_network should not return stderr when an ovfEnv is found that does not contain Rally vApp properties'

  stdout = actual[1]
  assert 'NETWORKING=yes' in stdout,                                   'cmd_sysconfig_network stdout should contain the contents of the original /etc/sysconfig/network file'
  assert len(re.findall('HOSTNAME=vapp_alm.f4tech.com', stdout)) is 1, 'cmd_sysconfig_network stdout should contain only one HOSTNAME entry'
  assert stdout.count('\n\n') is 0,                                    'cmd_sysconfig_network stdout should not contain empty lines'


@patch('vapptool.cmd_sysconfig_network')
def test_main_sysconfig_network(mock_cmd_sysconfig_network):
  mock_cmd_sysconfig_network.return_value = [ 0, 'stdout', 'stderr' ]

  actual = call_main_with('--sysconfig-network')

  assert actual[0] is 0,        '--sysconfig-network should exit zero'
  assert 'stdout' in actual[1], '--sysconfig-network should print stdout'
  assert 'stderr' in actual[2], '--sysconfig-network should not print stderr'

def test_main_sysconfig_network_with_wrong_options():
  actual = call_main_with('--sysconfig-network', '--wrongopt')

  assert actual[0] is not 0,      '--sysconfig-network should exit non-zero when called incorrectly'
  assert actual[1] is None,       '--sysconfig-network should not print stdout when called incorrectly'
  assert 'wrongopt' in actual[2], '--sysconfig-network should print stderr when called incorrectly'
