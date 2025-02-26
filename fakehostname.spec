Name:		fakehostname
Version:	0.2
Release:	2%{?dist}
Summary:	Wrap a command so that gethostname(2) and calls to libudev return something else

Group:		System Environment/Libraries
License:	GPL
URL:		https://github.com/nonspecialist/fakehostname
Source0:	fakehostname
Source1:	fakeudev
Source2:	fakehostname.c
Source3:	fakeudev.c
Source4:	Makefile

BuildRequires:	gcc
Requires:	bash

%description
fakehostname provides a shared library which intercepts calls to
gethostname(2) from libc and permits you to override it using an environment
variable so that you can fake the hostname that applications see. This can
be useful for testing, or for fixing broken software which can't be rewritten.

As of v0.3, the package has been extended to support overriding responses
from libudev to replace the returned MAC address of discovered network adapters.
This functionality is often useful in supporting older software with license keys
that are tied to particular MAC addresses when run in containerised environments
that don't support setting the MAC address visible to the running container (eg AWS
Fargate)

%prep
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} $RPM_BUILD_DIR

%build
make %{?_smp_mflags}


%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir} $RPM_BUILD_ROOT/%{_libdir}
make install BINDIR=$RPM_BUILD_ROOT/%{_bindir} LIBDIR=$RPM_BUILD_ROOT/%{_libdir}

%files
%defattr(-,root,root)
%attr(0755,root,root)	%{_bindir}/fakehostname
%attr(0755,root,root)	%{_bindir}/fakeudev
%attr(0755,root,root)	%{_libdir}/libfakehostname.so.1
%attr(0755,root,root)	%{_libdir}/libfakeudev.so.1

%changelog
* Tue Feb 25 2025 Colin Panisset <nonspecialist@clabber.com> 0.3-1
- add libudev wrapping for device discovery overrides
* Thu Sep 20 2012 Colin Panisset <nonspecialist@clabber.com> 0.2-1
- make fakehostname wrapper try other locations for library
* Tue Sep 18 2012 Colin Panisset <nonspecialist@clabber.com> 0.1-1
- initial version of the package
- wrapper shell script and shared library
