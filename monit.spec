Summary:	Process monitor and restart utility
Summary(pl):	Narzêdzie do monitorowania procesów i ich restartowania
Name:		monit
%define		_ver 4.8
Version:	%{_ver}.1
Release:	3
License:	GPL
Group:		Applications/Console
Source0:	http://www.tildeslash.com/monit/dist/%{name}-%{_ver}.tar.gz
# Source0-md5:	376bd526ee5577a6f0a842216f8ccf25
Source1:	%{name}.init
# http://www.tildeslash.com/monit/dist/%{name}-4.8-patch01
Patch0:		%{name}-4.8-patch01.patch
Patch1:		%{name}-localhost-http.patch
URL:		http://www.tildeslash.com/monit/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
monit is an utility for monitoring daemons or similar programs running
on a Unix system. It will start specified programs if they are not
running and restart programs not responding.

%description -l pl
monit jest narzêdziem do monitorowania demonów oraz podobnych
programów pracuj±cych w systemie Unix. monit zrestartuje podany
program w momencie gdy przestaje on pracowaæ lub w momencie gdy
program przestaje odpowiadaæ.

%prep
%setup -q -n %{name}-%{_ver}
%patch0 -p0
%patch1 -p1

%build
%configure \
	--with-ssl-lib-dir=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,monit}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# include all files provided by services:
echo "include %{_sysconfdir}/monit/*.monitrc" >> monitrc.main

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install monitrc.main $RPM_BUILD_ROOT%{_sysconfdir}/monitrc
install monitrc $RPM_BUILD_ROOT%{_sysconfdir}/monit/default.monitrc

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service monit restart "Monit Daemon"

%preun
if [ "$1" = "0" ]; then
	%service monit stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc doc/*.html CHANGES.txt CONTRIBUTORS FAQ.txt README*
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}rc
%attr(751,root,root) %dir %{_sysconfdir}/monit
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/monit/*.monitrc
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man?/*
