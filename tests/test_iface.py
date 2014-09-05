from helper import *

@patch('vapptool.load_ovf')
@raises(Exception)
def test_cmd_iface_with_no_ovfenv(mock_load_ovf):
  mock_load_ovf.side_effect = Exception('Boom!')
  vapptool.cmd_iface()

@patch('vapptool.load_ovf')
@patch('vapptool.load_iface')
def test_cmd_iface_with_an_unknown_ovfenv(mock_load_iface, mock_load_ovf):
  mock_load_iface.return_value = file('tests/fixtures/centos6/ifcfg-eth0.orig', 'r').read()
  mock_load_ovf.return_value   = file('tests/fixtures/ovfenv/legacy-onprem.xml', 'r').read()

  actual = vapptool.cmd_iface('eth0')

  assert actual[0] is not 0,    'cmd_iface should return a non-zero status when an ovfEnv is found that does not contain Rally vApp properties'
  assert actual[1] is None,     'cmd_iface should not return stdout when an ovfEnv is found that does not contain Rally vApp properties'
  assert actual[2] is not None, 'cmd_iface should return stderr when an ovfEnv is found that does not contain Rally vApp properties'

@patch('vapptool.load_ovf')
@patch('vapptool.load_iface')
def test_cmd_iface_with_default_iface_and_a_known_ovfenv(mock_load_iface, mock_load_ovf):
  mock_load_iface.return_value = file('tests/fixtures/centos6/ifcfg-eth0.orig', 'r').read()
  mock_load_ovf.return_value   = file('tests/fixtures/ovfenv/alm-core.xml', 'r').read()

  actual = vapptool.cmd_iface('eth0')

  assert actual[0] is 0,    'cmd_iface should return a zero status when an ovfEnv is found that contains Rally vApp properties'
  assert actual[2] is None, 'cmd_iface should not return stderr when an ovfEnv is found that contains Rally vApp properties'

  stdout = actual[1]
  assert 'DEVICE='                      in stdout, 'cmd_iface stdout should contain the contents of the original /etc/iface file'
  assert 'HOSTNAME=vapp_alm.f4tech.com' in stdout, 'cmd_iface stdout should contain a HOSTNAME entry'
  assert 'IPADDR=10.32.30.29'           in stdout, 'cmd_iface stdout should contain an IPADDR entry'
  assert 'NETMASK=255.255.254.0'        in stdout, 'cmd_iface stdout should contain an NETMASK entry'
  assert 'DNS1=10.32.0.9'               in stdout, 'cmd_iface stdout should contain an DNS1 entry'
  assert 'DNS2=10.32.0.13'              in stdout, 'cmd_iface stdout should contain an DNS2 entry'
  assert 'DOMAIN=f4tech.com'            in stdout, 'cmd_iface stdout should contain an DOMAIN entry'
  assert 'GATEWAY=10.32.30.1'           in stdout, 'cmd_iface stdout should contain an GATEWAY entry'


@patch('vapptool.load_ovf')
@patch('vapptool.load_iface')
def test_cmd_iface_with_default_iface_and_a_known_ovfenv(mock_load_iface, mock_load_ovf):
  mock_load_iface.return_value = file('tests/fixtures/centos6/ifcfg-eth0.orig', 'r').read()
  mock_load_ovf.return_value   = file('tests/fixtures/ovfenv/alm-core.xml', 'r').read()

  first_run = vapptool.cmd_iface('eth0')
  mock_load_iface.return_value = first_run[1]

  actual = vapptool.cmd_iface('eth0')

  assert actual[0] is 0,    'cmd_iface should return a zero status when an ovfEnv is found that contains Rally vApp properties'
  assert actual[2] is None, 'cmd_iface should not return stderr when an ovfEnv is found that contains Rally vApp properties'

  stdout = actual[1]
  # print stdout
  assert 'DEVICE=' in stdout,                      'cmd_iface stdout should contain the contents of the original /etc/iface file'
  assert len(re.findall('HOSTNAME', stdout)) is 1, 'cmd_iface stdout should contain only one HOSTNAME entry'
  assert len(re.findall('IPADDR',   stdout)) is 1, 'cmd_iface stdout should contain only one IPADDR entry'
  assert len(re.findall('NETMASK',  stdout)) is 1, 'cmd_iface stdout should contain only one NETMASK entry'
  assert len(re.findall('DNS1',     stdout)) is 1, 'cmd_iface stdout should contain only one DNS1 entry'
  assert len(re.findall('DNS2',     stdout)) is 1, 'cmd_iface stdout should contain only one DNS2 entry'
  assert len(re.findall('DOMAIN',   stdout)) is 1, 'cmd_iface stdout should contain only one DOMAIN entry'
  assert len(re.findall('GATEWAY',  stdout)) is 1, 'cmd_iface stdout should contain only one GATEWAY entry'
  assert stdout.count('\n\n') is 0, 'cmd_iface stdout should not contain empty lines'


@patch('vapptool.cmd_iface')
def test_main_iface(mock_cmd_iface):
  mock_cmd_iface.return_value = [ 0, 'stdout', 'stderr' ]

  actual = call_main_with('--iface=foo')

  assert actual[0] is 0,        '--iface should exit zero'
  assert 'stdout' in actual[1], '--iface should print stdout'
  assert 'stderr' in actual[2], '--iface should not print stderr'

def test_main_iface_without_iface_name():
  actual = call_main_with('--iface')

  assert actual[0] is not 0,    '--iface should exit non-zero when called without a iface name'
  assert actual[1] is None,     '--iface should not print stdout when called without a iface name'
  assert actual[2] is not None, '--iface should print stderr when called without a iface name'

def test_main_iface_with_wrong_options():
  actual = call_main_with('--iface=bar', '--wrongopt')

  assert actual[0] is not 0,      '--iface should exit non-zero when called incorrectly'
  assert actual[1] is None,       '--iface should not print stdout when called incorrectly'
  assert 'wrongopt' in actual[2], '--iface should print stderr when called incorrectly'
