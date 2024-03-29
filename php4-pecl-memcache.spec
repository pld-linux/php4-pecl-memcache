%define		_modname	memcache
%define		_status		stable
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%{_libdir}/php4
Summary:	%{_modname} - a memcached extension
Summary(pl.UTF-8):	%{_modname} - rozszerzenie memcached
Name:		php4-pecl-%{_modname}
Version:	1.5
Release:	4
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	f521dd4d3cad4ccb05d9ade4e1cc04d4
URL:		http://pecl.php.net/package/memcached/
BuildRequires:	php4-devel >= 3:4.3.3
BuildRequires:	rpmbuild(macros) >= 1.344
Requires:	php4-common >= 3:4.4.0-3
%{?requires_php_extension}
Obsoletes:	php4-pear-%{_modname}
Conflicts:	php4-mcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Memcached is a caching daemon designed especially for dynamic web
applications to decrease database load by storing objects in memory.

This extension allows you to work with memcached through handy OO and
procedural interfaces.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Memcached to zaprojektowany dla dynamicznych aplikacji internetowych
daemon cachujący mający za zadanie zmniejszenie obciążenia bazy danych
przez przechowywanie w pamięci obiektów.

To rozszerzenie umożliwia pracę z memcached za pomocą poręcznego
zorientowanego obiektowo (oraz przez procedury) interfejsu.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-zlib-dir=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php4_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php4_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,README,example.php}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
