What is this?
=============

An example override of the libc function [`ioctl(2)`](https://linux.die.net/man/2/ioctl)
when used to retrieve the MAC address of a local interface.

How do I use it?
================

* build the shared library (`make`) or the RPM (`make rpm`)
* install it somewhere (`make install`) or (`rpm -ivh .../path/to/new-rpm`)
* either:
  * set the installed shared library to be loaded prior to libc
    (`export LD_PRELOAD=/path/to/shared/library.so.1`)
  * set the environment variable `HWADDR_<interface-name>` to whatever MAC address
    you want (note this MUST conform to the format `xx:xx:xx:xx:xx:xx`)
  * run your application normally

If you don't set `$HWADDR_<interface-name>`, the actual MAC address returned by the
real [`ioctl(2)`](https://linux.die.net/man/2/ioctl) call will be used

MAC addresses for any interfaces NOT overridden will be returned unchanged as well.

Examples
========

```shell
$ HWADDR_eth0=de:ad:be:ef:ca:fe LD_PRELOAD=/home/fred/libfakeif.so.1 command
Replacing original address 02:42:ac:1a:00:02 of eth0 with de:ad:be:ef:ca:fe
```

Debugging
=========

If you set the environment variable `FAKEIF_DEBUG` to literally anything, you'll
get some debugging.

For example:

```shell
$ FAKEIF_DEBUG=yesplease HWADDR_eth0=de:ad:be:ef:ca:fe LD_PRELOAD=/home/fred/libfakeif.so.1 command
SIOCGIFHWADDR intercepted
Old MAC address 02:42:ac:1a:00:02
Replacing original address 02:42:ac:1a:00:02 of eth0 with de:ad:be:ef:ca:fe
New MAC address 02:4b:01:c0:d2:b1
ioctl hooked: returns 0
SIOCGIFHWADDR intercepted
No override for eth1
ioctl hooked: returns -1
SIOCGIFHWADDR intercepted
No override for eth2
ioctl hooked: returns -1
SIOCGIFHWADDR intercepted
...
```

License
=======

This code is licensed under the GPLv3 -- a copy of the license can be found in
the file LICENSE.
