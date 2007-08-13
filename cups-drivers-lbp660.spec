%define rname lbp660

Summary:	Linux Canon LBP-460/660 driver
Name:		cups-drivers-%{rname}
Version:	0.2.4
Release:	%mkrel 1
License:	GPL
Group:		System/Configuration/Printing
URL:		http://www.boichat.ch/nicolas/lbp660/
Source0:	http://www.boichat.ch/nicolas/lbp660/lbp660-%{version}.tar.bz2
Requires:	cups
Conflicts:	cups-drivers-2006 cups-drivers-2007
Conflicts:	printer-utils-2006 printer-utils-2007
Conflicts:	printer-filters-2006 printer-filters-2007
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
In this package there is a linux driver for the Canon LBP-660 and
LBP-460 printers.

Most of my work is based on Rildo Pragana's driver for Samsung ML-85G,
see : http://pragana.net - "Adventures in Linux Programming".

It should support both A4 and Letter sized paper, but I only tested it
with A4 sized paper.

This package contains CUPS drivers (PPD) for the following printers:

 o Canon-LBP-460
 o Canon-LBP-660

%prep

%setup -q -n %{rname}-%{version}

%build

%make CFLAGS="%{optflags}"

# Correct PPD files to pass "cupstestppd"
perl -p -i -e "s/DefaultNoReset/DefaultAlwaysReset/" ppd/*.ppd

# Do not generate a log file with fixed name, security problem!
perl -p -i -e "s:/tmp/lbp.60.log:/dev/null:" ppd/*.ppd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/cups/model/%{rname}

install -m0755 %{rname} %{buildroot}%{_bindir}/
install -m0755 lbp[46]60-* %{buildroot}%{_bindir}/
install -m0644 ppd/*.ppd %{buildroot}%{_datadir}/cups/model/%{rname}/

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc COPYING NEWS README THANKS TODO
# "%{rname}" talks directly to the parallel port I/O 0x378, not to /dev/lp0
# Therefore SUID "root" is needed. Program only executable by "lp" & "root"
# (group-executable).
%attr(4750,root,sys) %{_bindir}/%{rname}
%attr(0755,root,root) %{_bindir}/lbp[46]60-*
%attr(0755,root,root) %dir %{_datadir}/cups/model/%{rname}
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Canon-LBP-460-lbp460.ppd
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Canon-LBP-660-%{rname}.ppd
