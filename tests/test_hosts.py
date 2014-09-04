from nose_parameterized import parameterized
from nose.tools import with_setup, raises
from mock import *
import imp
import libxml2
import re

vapptool = imp.load_source('vapptool', './vapptool')

@patch('vapptool.load_ovf')
@raises(Exception)
def test_cmd_hosts_with_no_ovfenv(mock_load_ovf):
  mock_load_ovf.side_effect = Exception('Boom!')
  vapptool.cmd_hosts()

@patch('vapptool.load_hosts')
@raises(Exception)
def test_cmd_hosts_with_no_etc_hosts(mock_load_hosts):
  mock_load_hosts.side_effect = Exception('Bam!')
  vapptool.cmd_hosts()

@patch('vapptool.load_ovf')
@patch('vapptool.load_hosts')
def test_cmd_hosts_with_default_hosts_and_a_known_ovfenv(mock_load_hosts, mock_load_ovf):
  mock_load_hosts.return_value = file('tests/fixtures/centos6/hosts.orig', 'r').read()
  mock_load_ovf.return_value   = file('tests/fixtures/ovfenv/alm-core.xml', 'r').read()

  actual = vapptool.cmd_hosts()

  assert actual[0] is 0,    'cmd_hosts should return a zero status when an ovfEnv is found that contains Rally vApp properties'
  assert actual[2] is None, 'cmd_hosts should return stderr when an ovfEnv is found that does not contain Rally vApp properties'

  stdout = actual[1]
  assert re.search('127.0.0.1\s+localhost', stdout)                                    is not None, 'cmd_hosts stdout should contain the contents of the original /etc/hosts file'
  assert re.search('10.32.30.29\s+vapp_localhost\s+vapp_localhost.f4tech.com', stdout) is not None, 'cmd_hosts stdout should contain a vapp_localhost entry'
  assert re.search('10.32.30.29\s+vapp_alm\s+vapp_alm.f4tech.com', stdout)             is not None, 'cmd_hosts stdout should contain a vapp_alm entry'
  assert re.search('10.32.30.30\s+vapp_core\s+vapp_core.f4tech.com', stdout)           is not None, 'cmd_hosts stdout should contain a vapp_core entry'


@patch('vapptool.load_ovf')
@patch('vapptool.load_hosts')
def test_cmd_hosts_with_modified_hosts_and_a_known_ovfenv(mock_load_hosts, mock_load_ovf):
  mock_load_hosts.return_value = file('tests/fixtures/centos6/hosts.orig', 'r').read()
  mock_load_ovf.return_value   = file('tests/fixtures/ovfenv/alm-core.xml', 'r').read()

  first_run = vapptool.cmd_hosts()
  mock_load_hosts.return_value = first_run[1]

  actual = vapptool.cmd_hosts()

  assert actual[0] is 0,    'cmd_hosts should return a zero status when an ovfEnv is found that contains Rally vApp properties'
  assert actual[2] is None, 'cmd_hosts should return stderr when an ovfEnv is found that does not contain Rally vApp properties'

  stdout = actual[1]
  assert re.search('127.0.0.1\s+localhost', stdout)                                          is not None, 'cmd_hosts stdout should contain the contents of the original /etc/hosts file'
  assert len(re.findall('10.32.30.29\s+vapp_localhost\s+vapp_localhost.f4tech.com', stdout)) is 1, 'cmd_hosts stdout should contain only one vapp_localhost entry'
  assert len(re.findall('10.32.30.29\s+vapp_alm\s+vapp_alm.f4tech.com', stdout))             is 1, 'cmd_hosts stdout should contain only one vapp_alm entry'
  assert len(re.findall('10.32.30.30\s+vapp_core\s+vapp_core.f4tech.com', stdout))           is 1, 'cmd_hosts stdout should contain only one vapp_core entry'
