Name:    e4rat
Version: 0.2.1
Release: %mkrel 1
Summary: e4rat is a toolset to accelerate the boot process as well as application startups
License: GPLv3
URL:     http://e4rat.sourceforge.net/
Group:   System/Configuration/Boot and Init
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source0: http://downloads.sourceforge.net/project/dracut/%{name}_%{version}_src.tar.gz
Patch0:	e4rat_0.2.1-dynamic-link.patch

BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: ext2fs-devel
BuildRequires: libblkid-devel
BuildRequires: audit-devel
BuildRequires: auparse-devel
BuildRequires: libstdc++-devel
BuildRequires: audit

%description
e4rat ("Ext4 - Reducing Access Times") is a toolset to accelerate the boot
process as well as application startups. Through physical file realloction
e4rat eliminates both seek times and rotational delays. This leads to a high
disk transfer rate.

Placing files on disk in a sequentially ordered way allows to efficiently
read-ahead files in parallel to the program startup. The combination of
sequentially reading and a high cache hit rate may reduce the boot time by a
factor of three, as the example below shows.

e4rat is based on the online defragmentation ioctl EXT4_IOC_MOVE_EXT from the
Ext4 filesystem, which was introduced in Linux Kernel 2.6.31. Other filesystem
types and/or earlier versions of extended filesystems are not supported. 

%prep
%setup -q -n %name-%version
%patch0 -p1 -b .dynamic-link

%build
%cmake
%make

%install
%makeinstall_std -C build

# (eugeni) remove left-over static library
rm -f %{buildroot}%{_libdir}/libe4rat-core.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%config %{_sysconfdir}/%name.conf
%{_sbindir}/%name-collect
%{_sbindir}/%name-preload
%{_sbindir}/%name-realloc
%{_mandir}/man5/%name.conf.5*
%{_mandir}/man8/%name-collect.8*
%{_mandir}/man8/%name-preload.8*
%{_mandir}/man8/%name-realloc.8*
