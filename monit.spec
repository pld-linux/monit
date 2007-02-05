Summary:	Process monitor and restart utility
Summary(pl):	Narzêdzie do monitorowania procesów i ich restartowania
Name:		monit
Version:	4.8.2
Release:	1.1
License:	GPL
Group:		Applications/Console
Source0:	http://www.tildeslash.com/monit/dist/%{name}-%{version}.tar.gz
# Source0-md5:	e7ad6056c71becf014653f6597d110ca
Source1:	%{name}.init
Patch0:		%{name}-localhost-http.patch
Patch1:		monit-config.patch
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
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	--with-ssl-lib-dir=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,monit},%{_sbindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install monitrc $RPM_BUILD_ROOT%{_sysconfdir}/monitrc
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/monit

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

%triggerpostun -- %{name} < 4.8.2-1.1
if [ -f %{_sysconfdir}/monit/default.monitrc.rpmsave ]; then
	cp -f %{_sysconfdir}/monitrc{,.rpmnew}
	mv -f %{_sysconfdir}/monit{/default.monitrc.rpmsave,rc}
	echo 'include /etc/monit/*.monitrc' >> %{_sysconfdir}/monitrc
	%service -q monit restart
fi

%files
%defattr(644,root,root,755)
%doc doc/*.html CHANGES.txt CONTRIBUTORS FAQ.txt README*
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}rc
%dir %attr(751,root,root) %{_sysconfdir}/monit
%attr(755,root,root) %{_sbindir}/monit
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man?/*
