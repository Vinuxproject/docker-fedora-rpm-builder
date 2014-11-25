%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

Name:		redis
Version:	%{_pkg_version}
Release:	%{_pkg_release}
Summary:	A persistent key-value database (IXL custom)

License:	BSD
URL:		http://redis.io

# git repo and a config file
Source0:	%{name}.conf
Source1:	%{name}.service
Source2:	%{name}.tmpfiles
Source3:	%{name}.init

ExclusiveArch:	x86_64
#Requires:	java-1.7.0-openjdk
BuildRequires:	git

%if 0%{?with_systemd}
BuildRequires:     systemd
%endif

%if 0%{?with_systemd}
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts
%endif

%description
Redis is an advanced key-value store. It is often referred to as a data
structure server since keys can contain strings, hashes, lists, sets and
sorted sets.

You can run atomic operations on these types, like appending to a string;
incrementing the value in a hash; pushing to a list; computing set
intersection, union and difference; or getting the member with highest
ranking in a sorted set.

In order to achieve its outstanding performance, Redis works with an
in-memory dataset. Depending on your use case, you can persist it either
by dumping the dataset to disk every once in a while, or by appending
each command to a log.

Redis also supports trivial-to-setup master-slave replication, with very
fast non-blocking first synchronization, auto-reconnection on net split
and so forth.

Other features include Transactions, Pub/Sub, Lua scripting, Keys with a
limited time-to-live, and configuration settings to make Redis behave like
a cache.

You can use Redis from most programming languages also.

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

%if 0%{?with_systemd}
install -pDm644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -pDm644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -pDm644 %{name}.tmpfiles %{buildroot}%{_tmpfilesdir}/%{name}.conf
%else
install -pDm755 %{name}.init %{buildroot}%{_initrddir}/%{name}
%endif

%pre
getent group %{name} &> /dev/null || \
groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c 'Redis Database Server' %{name} &> /dev/null
exit 0

%post
%if 0%{?with_systemd}
%systemd_post %{name}.service
%else
chkconfig --add %{name}
%endif

%preun
%if 0%{?with_systemd}
%systemd_preun %{name}.service
%else
if [ $1 -eq 0 ] ; then
service %{name} stop &> /dev/null
chkconfig --del %{name} &> /dev/null
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun_with_restart %{name}.service
%else
if [ "$1" -ge "1" ] ; then
    service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif

%files
%attr(0644, redis, root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %attr(0755, redis, redis) %{_sharedstatedir}/%{name}
%dir %attr(0755, redis, redis) %{_localstatedir}/log/%{name}
%{_bindir}/%{name}-*

%if 0%{?with_systemd}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

%changelog
* Fri Sep 26 2014 Renning Bruns <rbruns@ixl.com>
- initial packaging.
