Summary:	Process monitor and restart utility
Summary(pl):	Narzêdzie do monitorowania procesów i ich restartowania
Name:		monit
Version:	4.1
Release:	1
Group:		Applications/Console
License:	GPL
Source0:	http://www.tildeslash.com/monit/dist/%{name}-%{version}.tar.gz
# Source0-md5:	dd43941901a066bb530adf11b4266e82
Source1:	%{name}.init
URL:		http://www.tildeslash.com/monit/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	openssl-devel >= 0.9.7c
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
monit is an utility for monitoring daemons or similar programs running
on a Unix system. It will start specified programs if they are not
running and restart programs not responding.

%description -l pl
monit jest narzêdziem do monitorowania demonów oraz podonych programów
pracuj±cych w systemie Unix. monit zrestartuje podany program w
momencie gdy przestaje on pracowaæ lub w momencie gdy program
przestaje odpowiadaæ.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install monitrc $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f %{_var}/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_var}/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc doc/*.html CHANGES.txt CONTRIBUTORS FAQ.txt README*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}rc
