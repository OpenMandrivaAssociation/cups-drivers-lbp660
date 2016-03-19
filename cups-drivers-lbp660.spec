%define rname lbp660

Summary:	Linux Canon LBP-460/660 driver
Name:		cups-drivers-%{rname}
Version:	0.3.1
Release:	16
License:	GPLv2
Group:		System/Printing
Url:		http://www.boichat.ch/nicolas/lbp660/
Source0:	http://www.boichat.ch/nicolas/lbp660/lbp660-%{version}.tar.gz
Patch0:		lbp660-0.3.1-ldflags.patch
Requires:	cups
ExclusiveArch:	%{ix86} x86_64

%description
In this package there is a linux driver for the Canon LBP-660 and
LBP-460 printers.

This package contains CUPS drivers (PPD) for the following printers:

 o Canon-LBP-460
 o Canon-LBP-660

%prep

%setup -qn %{rname}-%{version}
%patch0 -p1 -b .ldflags

%build
%make CFLAGS="%{optflags}" LDFLAGS="%{ldflags}"

# Correct PPD files to pass "cupstestppd"
sed -i -e "s/DefaultNoReset/DefaultAlwaysReset/" ppd/*.ppd

# Do not generate a log file with fixed name, security problem!
sed -i -e "s:/tmp/lbp.60.log:/dev/null:" ppd/*.ppd

%install

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/cups/model/%{rname}

install -m0755 lbp[46]60 %{buildroot}%{_bindir}/
install -m0755 lbp[46]60-* %{buildroot}%{_bindir}/
install -m0644 ppd/*.ppd %{buildroot}%{_datadir}/cups/model/%{rname}/

%files
%doc COPYING NEWS README THANKS TODO
# "%{rname}" talks directly to the parallel port I/O 0x378, not to /dev/lp0
# Therefore SUID "root" is needed. Program only executable by "lp" & "root"
# (group-executable).
%attr(4750,root,sys) %{_bindir}/%{rname}
%attr(4750,root,sys) %{_bindir}/lbp460
%attr(0755,root,root) %{_bindir}/lbp[46]60-*
%attr(0755,root,root) %dir %{_datadir}/cups/model/%{rname}
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Canon-LBP-460-lbp460.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Canon-LBP-660-%{rname}.ppd*

