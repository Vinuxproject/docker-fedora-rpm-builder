Name:		redis
Version:	%{_pkg_version}
Release:	%{_pkg_release}
Summary:	Open source in-memory database that persists on disk

License:	BSD
URL:		http://redis.io

# git repo and a config file
Source0:	redis.conf
Source1:	redis.service

ExclusiveArch:	x86_64
#Requires:	java-1.7.0-openjdk
BuildRequires:	git

%description
This is the first release candidate of Redis 3.0.0. Redis 3.0 features
support for Redis Cluster and important speed improvements under
certain workloads. This is a developers preview and is not suitable
for production environments. The next RC is scheduled for 3 November
2014.

%prep
test -d redis && ( cd redis; git pull ) || git clone https://github.com/antirez/redis.git redis
cp %SOURCE0 .
cp %SOURCE1 .

%build
make -C redis

%install
make -C redis install INTSALL="install -p" PREFIX=%{buildroot}%{_prefix}

install -d %{buildroot}%{_sharedstatedir}/%{name}
install -d %{buildroot}%{_localstatedir}/log/%{name}

install -pDm644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -pDm644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group %{name} &> /dev/null || \
groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c 'Redis Database Server' %{name} &> /dev/null
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%{_unitdir}/%{name}.service
%attr(0644, redis, root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %attr(0755, redis, redis) %{_sharedstatedir}/%{name}
%dir %attr(0755, redis, redis) %{_localstatedir}/log/%{name}
%{_bindir}/%{name}-*

%changelog
* Fri Sep 26 2014 Renning Bruns <rbruns@ixl.com>
- initial packaging.
