#
# Conditional build:
%bcond_without	pam		# PAM support
%bcond_without	ssl		# SSL support

# NOTES:
# - Release notes: https://mmonit.com/monit/changes/

Summary:	Process monitor and restart utility
Summary(pl.UTF-8):	Narzędzie do monitorowania procesów i ich restartowania
Name:		monit
Version:	5.15
Release:	2
License:	AGPL v3
Group:		Daemons
Source0:	http://mmonit.com/monit/dist/%{name}-%{version}.tar.gz
# Source0-md5:	c723745298d7ba6d28194b9f25eba6fe
Source1:	%{name}.init
Source2:	%{name}rc
Source3:	%{name}.config
Patch0:		config.patch
URL:		http://mmonit.com/monit/
BuildRequires:	bison
BuildRequires:	flex
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_pam:BuildRequires:	pam-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.0.15
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
monit is an utility for monitoring daemons or similar programs running
on a Unix system. It will start specified programs if they are not
running and restart programs not responding.

%description -l pl.UTF-8
monit jest narzędziem do monitorowania demonów oraz podobnych
programów pracujących w systemie Unix. monit zrestartuje podany
program w momencie gdy przestaje on pracować lub w momencie gdy
program przestaje odpowiadać.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--bindir=%{_sbindir} \
	%{__with_without ssl} \
	%{__with_without pam} \
	--with-ssl-lib-dir=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,monit,sysconfig}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/monit

cp -p monitrc $RPM_BUILD_ROOT%{_sysconfdir}/monitrc
# NOTE: 'include *.monitrc' will fail if nothing matches the glob.
# so install dummy config not to remove it with upgrades (avoid .rpmsave)
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/monit/default.monitrc

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
%doc CONTRIBUTORS README*
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/monitrc
%dir %attr(751,root,root) %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/default.monitrc
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/monit
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/monit
%{_mandir}/man1/monit.1*
