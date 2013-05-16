# TODO
# - lighttpd support
%define	_hordeapp mottle
%define	_snap	2008-10-11
#define	_rc		rc1
%define	_rel	3

%include	/usr/lib/rpm/macros.php
Summary:	Template for horde projects
Name:		horde-%{_hordeapp}
Version:	0.1
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	ASL
Group:		Applications/WWW
# due builder limitations can't have complex macros in Source0
#Source0:	ftp://ftp.horde.org/pub/skeleton/%{_hordeapp}-h3-%{version}.tar.gz
#Source0:	ftp://ftp.horde.org/pub/skeleton/%{_hordeapp}-h3-%{version}-%{_rc}.tar.gz
Source0:	ftp://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-HEAD-%{_snap}.tar.gz
# Source0-md5:	d7d9d33a946221ab7c3fb715d409d132
Source1:	%{_hordeapp}-apache.conf
Source2:	%{_hordeapp}-httpd.conf
URL:		http://cvs.horde.org/mottle/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.264
BuildRequires:	tar >= 1:1.15.1
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Requires:	webapps
Conflicts:	apache-base < 2.4.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq_pear	Horde.*

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{_hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{_hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

# GET DESCRIPTION FROM PROJECT URL
%description
Mottle is a MOTD (Message of the Day) type application written in PHP
and utilizing the Horde Application Framework.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with mottle) please visit <http://www.horde.org/>.

%description -l pl.UTF-8
Mottle jest aplikacją typu MOTD (Message of the Day) napisaną w PHP
i wykorzystującą szkielet Horde.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Więcej informacji (włącznie z pomocą dla
Mottle) można znaleźć na stronie <http://www.horde.org/>.

%prep
%setup -qcT -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1

rm */.htaccess
#for i in config/*.dist; do
#	mv $i config/$(basename $i .dist)
#done
# considered harmful (horde/docs/SECURITY)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a lib locale templates themes $RPM_BUILD_ROOT%{_appdir}
cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<-EOF
	IMPORTANT:
	If you are installing Mottle for the first time, You may need to
	create the Mottle database tables. To do so run:
	zcat %{_docdir}/%{name}-%{version}/scripts/sql/%{_hordeapp}.sql.gz | mysql horde
EOF
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
#%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
