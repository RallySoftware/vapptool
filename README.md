vapptool
========
vapptool is a utility that reads basic IPv4 network information from VMware OVF
Environment vApp Properties and generates system-compatible static IP network
configuration.

##Supported properties

###Virtual Machine properties
|Property|Type|Example|Description|Required|
|--------|:--:|:------|:----------|:------:|
| `vm_name` | String | `alm` | Used as a component of the VM's `HOSTNAME`.  Should only contain domain-name compatible characters.| Required |

###vApp properties
|Property|Type|Example|Description|Required|
|--------|:--:|:------|:----------|:------:|
| `ip_address_#{vm_name}` | IP | `10.0.0.5` | The vApp must have one of these properties defined for each VM in the vApp, using the `vm_name` assigned to the VM.| Required |
| `netmask` | IP | `255.255.255.0` | IP netmask. | Required |
| `dns_search_domain` | String | `f4tech.com` | Used as the resolver's dns search domain and as a component each of the VMs' `HOSTNAME`s. Must be a validly formatted domain name. | Required |
| `dns1` | IP | `8.8.8.8` | Primary DNS server. | Required |
| `dns2` | IP | `8.8.4.4` | Secondary DNS server. | Required |
| `default_gateway` | IP | `10.0.0.1` | Default gateway (router) IP address. | Required |

##Usage
```shell
% ./vapptool --help
Usage: vapptool [options]

Options:
  -h, --help            show this help message and exit
  -i, --inspect         Exits 0 when executed from on a VM within Rally vApp,
                        otherwise non-zero
  -P, --print           Prints the value of guestinfo.ovfEnv
  -l, --localhost       Prints the value of the ip_address property for this
                        VM
  -p PROPERTY, --property=PROPERTY
                        Prints the value of the property for this VM
  -H, --hosts           Prints output suitable for /etc/hosts that contains
                        entries for all VMs in this vApp
  -r, --resolv          Prints output suitable for /etc/resolv.conf that
                        contains entries for dns_search_domain, dns1, and dns2
  -n, --sysconfig-network
                        Prints output suitable for /etc/sysconfig/network that
                        contains a HOSTNAME entry for this VM
  -f IFACE, --iface=IFACE
                        Prints output suitable for /etc/sysconfig/network-
                        scripts/ifcfg-<iface> for this VM
```

##OSX Development setup (using system python)
These instructions assume OSX 1.9.4.

###libxml2
```shell
% brew uninstall libxml2
% brew install python
% brew install --with-python libxml2
% mkdir -p ~/Library/Python/2.7/lib/python/site-packages
% echo '/usr/local/opt/libxml2/lib/python2.7/site-packages' > ~/Library/Python/2.7/lib/python/site-packages/homebrew.pth
```

###python packages
```shell
pip install -r requirements.txt
```

###Running the tests
```shell
nosetests -s
```
