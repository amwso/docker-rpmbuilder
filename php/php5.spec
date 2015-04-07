Name:php5-vhost
Version:5.6.7
%define installdir /usr/local/php5
Release:        sudu.cn%{?dist}
Summary:        php-%{version}
Source0: http://www.php.net/distributions/php-%{version}.tar.gz
Group:Applications
License:Share
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%description
%prep
%setup -q -n php-%{version}
%build
%define debug_package %{nil}
sed -i 's/^#ifdef CONFIGURE_COMMAND$/#if 0/' ext/standard/info.c
sed -i '/^Configure Command/d' ext/standard/tests/general_functions/phpinfo.phpt
export EXTENSION_DIR=%{installdir}/lib/php/extensions
./configure '--prefix=%{installdir}' \
 '--with-config-file-scan-dir=%{installdir}/etc/conf.d' \
 '--disable-static' \
 '--with-libdir=lib64' \
 '--with-mysql=shared' \
 '--with-mysqli=shared' \
 '--with-pgsql=shared' \
 '--with-sqlite3' \
 '--enable-cgi' \
 '--enable-fpm' \
 '--enable-sockets' \
 '--enable-ftp' \
 '--enable-zip' \
 '--enable-mbstring' \
 '--enable-mbregex' \
 '--enable-calendar' \
 '--with-curl=shared' \
 '--disable-debug' \
 '--disable-rpath' \
 '--with-gd=shared' \
 '--enable-gd-native-ttf' \
 '--with-gettext' \
 '--with-jpeg-dir=shared' \
 '--with-png-dir=shared' \
 '--with-bz2' \
 '--enable-pcntl' \
 '--with-iconv' \
 '--with-mcrypt=shared' \
 '--with-openssl' \
 '--with-xmlrpc=shared' \
 '--with-xsl=shared' \
 '--enable-exif' \
 '--with-mhash' \
 '--enable-soap' \
 '--without-pear' \
 '--with-zlib' \
 '--enable-bcmath' \
 '--enable-opcache' \
 '--enable-sysvsem' \
 '--enable-sysvshm' \
 '--enable-sysvmsg' \
 '--with-freetype-dir=shared' \
 '--with-png-dir=shared' \
 '--with-jpeg-dir=shared'
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{__make} install INSTALL_ROOT="%{buildroot}"
mkdir -p %{buildroot}%{installdir}%{_initrddir}
mkdir -p %{buildroot}%{installdir}/etc/conf.d
install -Dp -m0755 sapi/fpm/init.d.php-fpm %{buildroot}%{installdir}%{_initrddir}/php-fpm
ln -sf %{installdir}/bin/phar.phar %{buildroot}%{installdir}/bin/phar
install -Dp -m0644 php.ini-production %{buildroot}%{installdir}/lib/php.ini

for mod in curl gd mcrypt mysql mysqli pgsql xmlrpc xsl \
    ; do
    cat > %{buildroot}%{installdir}/etc/conf.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
done
echo 'zend_extension=opcache.so' > %{buildroot}%{installdir}/etc/conf.d/opcache.ini

rm -rf %{buildroot}%{installdir}/lib/php/extensions/*.a

sed -i 's/^short_open_tag.*/short_open_tag = On/' %{buildroot}%{installdir}/lib/php.ini
sed -i 's/^expose_php.*/expose_php = Off/' %{buildroot}%{installdir}/lib/php.ini
sed -i 's/^max_execution_time.*/max_execution_time = 60/' %{buildroot}%{installdir}/lib/php.ini
sed -i 's/^error_reporting.*/error_reporting = E_COMPILE_ERROR|E_RECOVERABLE_ERROR|E_ERROR|E_CORE_ERROR/' %{buildroot}%{installdir}/lib/php.ini
sed -i 's/^display_errors.*/display_errors = On/' %{buildroot}%{installdir}/lib/php.ini
sed -i 's/^post_max_size.*/post_max_size = 20M/' %{buildroot}%{installdir}/lib/php.ini
sed -i 's/^upload_max_filesize.*/upload_max_filesize = 20M/' %{buildroot}%{installdir}/lib/php.ini

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{installdir}
%config            %{installdir}/etc/php-fpm.conf.default
%config(noreplace) %{installdir}%{_initrddir}/php-fpm
%config(noreplace) %{installdir}/lib/php.ini
%config(noreplace) %attr(644,root,root) %{installdir}/etc/conf.d/*.ini

%doc
%changelog
