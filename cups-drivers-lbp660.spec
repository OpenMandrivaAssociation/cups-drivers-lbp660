%define rname lbp660

Summary:	Linux Canon LBP-460/660 driver
Name:		cups-drivers-%{rname}
Version:	0.3.1
Release:	%mkrel 6
License:	GPL
Group:		System/Printing
URL:		http://www.boichat.ch/nicolas/lbp660/
Source0:	http://www.boichat.ch/nicolas/lbp660/lbp660-%{version}.tar.gz
Patch0:		lbp660-0.3.1-ldflags.patch
Requires:	cups
Conflicts:	cups-drivers = 2007
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64

%description
In this package there is a linux driver for the Canon LBP-660 and
LBP-460 printers.

This package contains CUPS drivers (PPD) for the following printers:

 o Canon-LBP-460
 o Canon-LBP-660

%prep

%setup -q -n %{rname}-%{version}
%patch0 -p1 -b .ldflags

%build

%make CFLAGS="%{optflags}" LDFLAGS="%{ldflags}"

# Correct PPD files to pass "cupstestppd"
perl -p -i -e "s/DefaultNoReset/DefaultAlwaysReset/" ppd/*.ppd

# Do not generate a log file with fixed name, security problem!
perl -p -i -e "s:/tmp/lbp.60.log:/dev/null:" ppd/*.ppd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/cups/model/%{rname}

install -m0755 lbp[46]60 %{buildroot}%{_bindir}/
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
%attr(4750,root,sys) %{_bindir}/lbp460
%attr(0755,root,root) %{_bindir}/lbp[46]60-*
%attr(0755,root,root) %dir %{_datadir}/cups/model/%{rname}
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Canon-LBP-460-lbp460.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Canon-LBP-660-%{rname}.ppd*


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-6mdv2011.0
+ Revision: 663437
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-5mdv2011.0
+ Revision: 603869
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-4mdv2010.1
+ Revision: 518841
- rebuild

* Thu Sep 24 2009 Olivier Blin <oblin@mandriva.com> 0.3.1-3mdv2010.0
+ Revision: 448233
- build on x86-only because using x86 specific stuff
  (from Arnaud Patard)

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-2mdv2010.0
+ Revision: 413285
- rebuild

* Sun Mar 22 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.3.1-1mdv2009.1
+ Revision: 360162
- Updated to version 0.3.1
- Redid ldflags patch.

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-7mdv2009.1
+ Revision: 318066
- use %%ldflags

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 0.2.4-6mdv2009.0
+ Revision: 220529
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 0.2.4-5mdv2008.1
+ Revision: 149146
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 30 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-4mdv2008.0
+ Revision: 75326
- fix deps (pixel)

* Wed Aug 22 2007 Thierry Vignaud <tv@mandriva.org> 0.2.4-3mdv2008.0
+ Revision: 69006
- fix description

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-2mdv2008.0
+ Revision: 64147
- use the new System/Printing RPM GROUP

* Mon Aug 13 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-1mdv2008.0
+ Revision: 62504
- Import cups-drivers-lbp660



* Mon Aug 13 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-1mdv2008.0
- initial Mandriva package
