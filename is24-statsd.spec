
Name:           is24-statsd
Version:        0.8
Release:        1%{?dist}
Summary:        monitoring daemon, that aggregates events received by udp in 10 second intervals
Group:          Applications/Internet
License:        Etsy open source license
URL:            https://github.com/oli99sc/statsd
Vendor:         Etsy, modified my OSchmitz IS24
Packager:       OSchmitz IS24 <oliver.schmitz@immobilienscout24.de>
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       nodejs

%description
Simple daemon for easy stats aggregation  

%prep
%setup -q


%build
echo "build not needed" 

%install
# install the js files which to the work
%{__mkdir_p} %{buildroot}/usr/share/is24-statsd
%{__install} -Dp -m0644 stats.js config.js %{buildroot}/usr/share/is24-statsd


# Install init scripts
%{__install} -Dp -m0755 redhat/is24-statsd %{buildroot}%{_initrddir}/%{name}

# Install default configuration files
%{__install} -Dp -m0644 exampleConfig.js  %{buildroot}%{_sysconfdir}/%{name}/config.js

%{__mkdir_p} %{buildroot}%{_localstatedir}/lock/subsys
touch %{buildroot}%{_localstatedir}/lock/subsys/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_localstatedir}/lib/%{name} \
    -s /sbin/nologin -c "%{name} daemon" %{name}
exit 0

%preun
service %{name} stop
exit 0

%postun
if [ $1 = 0 ]; then
	chkconfig --del %{name}
	getent passwd %{name} >/dev/null && \
	userdel -r %{name} 2>/dev/null
fi
exit 0

%post
chkconfig --add %{name}

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%doc StatsdClient.java php-example.php python_example.py
%doc exampleConfig.js


/usr/share/%{name}/*
%{_initrddir}/%{name}

%config %{_sysconfdir}/%{name}
%ghost %{_localstatedir}/lock/subsys/%{name}

%changelog
