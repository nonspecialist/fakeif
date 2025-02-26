Name:		fakeif
Version:	0.1
Release:	1%{?dist}
Summary:	Wrap a command so that calls to ioctl(2) for getting interface MAC addresses return something else

Group:		System Environment/Libraries
License:	GPL
URL:		https://github.com/nonspecialist/fakehostname
Source0:	fakeif.c
Source1:	Makefile

BuildRequires:	gcc
Requires:	bash

%description
fakeif provides a shared library which intercepts calls to
ioctl(2) from libc and allows you to override the returned MAC address for
one or more interfaces. This may be useful in scenarios such as containerisation
of legally-licensed workloads that are tied to a specific MAC address that
cannot be replicated in a cloud environment.

%prep
cp %{SOURCE0} %{SOURCE1} $RPM_BUILD_DIR

%build
make %{?_smp_mflags}


%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir} $RPM_BUILD_ROOT/%{_libdir}
make install BINDIR=$RPM_BUILD_ROOT/%{_bindir} LIBDIR=$RPM_BUILD_ROOT/%{_libdir}

%files
%defattr(-,root,root)
%attr(0755,root,root)	%{_libdir}/libfakeif.so.1

%changelog
* Tue Sep 18 2012 Colin Panisset <nonspecialist@clabber.com> 0.1-1
- initial version of the package forked from fakehostname
