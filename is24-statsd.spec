%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define __getent   /usr/bin/getent
%define __useradd  /usr/sbin/useradd
%define __userdel  /usr/sbin/userdel
%define __groupadd /usr/sbin/groupadd
%define __touch    /bin/touch
%define __service  /sbin/service

Name:           is24-statsd
Version:        0.1
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
%{__install} -Dp -m0644 stats.js config.js %{buildroot}%{__datadir}/%{name}


# Install init scripts
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# Install default configuration files
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
%{__install} -Dp -m0644 exampleConfig.js  %{buildroot}%{_sysconfdir}/%{name}/config.js

%{__mkdir_p} %{buildroot}%{_localstatedir}/run
%{__touch} %{buildroot}%{_localstatedir}/run/%{name}.pid

%pre
%{__getent} group %{name} >/dev/null || %{__groupadd} -r %{name}
%{__getent} passwd %{name} >/dev/null || \
    %{__useradd} -r -g %{name} -d %{_localstatedir}/lib/%{name} \
    -s /sbin/nologin -c "stats daemon" %{name}
exit 0

%preun
%{__service} %{name} stop
exit 0

%postun
if [ $1 = 0 ]; then
  %{__getent} passwd %{name} >/dev/null && \
      %{__userdel} -r %{name} 2>/dev/null
fi
exit 0

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%doc StatsdClient.java php-example.php python_exampl.py
%doc exampleConfig.js


/usr/share/%{name}/*
%{_initrddir}/%{name}

%config %{_sysconfdir}/%{name}
%ghost %{_localstatedir}/run/%{name}.pid

%changelog
