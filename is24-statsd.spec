
Name:           is24-statsd
Version:        0.8.10
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
getent group %{name} >/dev/null || groupadd -g 306 -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -u 306 -d %{_localstatedir}/lib/%{name} \
    -s /sbin/nologin -c "%{name} daemon" %{name}
exit 0

%preun
#final uninstall will stop service now, update keeps service running to remember service state for restart in post
if [ $1 = 0 ]; then
	service %{name} stop
fi
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
if [ $1 -gt 1 ]; then
    # restart service if it was running
    if /sbin/service %{name} status > /dev/null 2>&1; then
        echo "Restarting is24-statsd service because it was running."
        if ! /sbin/service %{name} restart ; then
                logger -s -t "%name" -- "Installation failure. Not able to restart the service." 
                exit 1
        fi
    fi
fi

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
* Tue Oct 16 2012 Oliver Schmitz <oli99sc@gmail.com> - 0.8.10-1
- use nodejs executable in init script instead of node after nodejs update, so we do not need dependency to compatibility rpm. 

* Tue Aug 16 2012 Oliver Schmitz <oli99sc@gmail.com> - 0.8.9-1
- improve localdev grouping 

* Tue Aug 13 2012 Oliver Schmitz <oli99sc@gmail.com> - 0.8.8-1
- all systems now measured only by host group, that is without trailing number in hostname

* Tue Aug 13 2012 Oliver Schmitz <oli99sc@gmail.com> - 0.8.7-1
- bui and dev systems not measured by host 

* Tue Aug 13 2012 Oliver Schmitz <oli99sc@gmail.com> - 0.8.6-1
- fix missing dot after other.unknowhost for counters 

* Tue Aug 11 2012 Oliver Schmitz <oli99sc@gmail.com> - 0.8.5-1
- statsd now handles our appname.hostname additional parameter on counters 
  and timers and sends it to graphite as key prefix

* Tue Jul 03 2012 Oliver Schmitz <oli99sc@gmail.com> - 0.8.4-1
- restart service on update if it was running before the update

* Tue Jul 03 2012 Oliver Schmitz <oli99sc@gmail.com> - 0.8.3-1
- create user and group with fixed uid / gid values and start service with this user
