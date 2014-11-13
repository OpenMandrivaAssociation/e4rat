%define major 0
%define libname %mklibname %{name}-core %{major}

Summary:	Toolset to accelerate the boot process as well as application startups
Name:		e4rat
Version:	0.2.3
Release:	2
License:	GPLv3
Group:		System/Configuration/Boot and Init
URL:		http://e4rat.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/dracut/%{name}_%{version}_src.tar.gz
Patch1:		e4rat-0.2.2-libdir.patch
Patch2:		e4rat-0.2.3-shared-build.patch
Patch3:		e4rat-0.2.3-boostfsv3.patch
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	ext2fs-devel
BuildRequires:	pkgconfig(blkid)
BuildRequires:	audit-devel
BuildRequires:	auparse-devel
BuildRequires:	libstdc++-devel
BuildRequires:	audit
# (tpg) this packages causes negative effect
Conflicts:	preload

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

%package %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description %{libname}
Main library for %{name}.

%prep
%setup -q
%patch1 -p1 -b .libdir
%patch2 -p1 -b .shared
%patch3 -p0 -b .boost3

%build
%cmake
%make

%install
%makeinstall_std -C build

%files
%doc README
%config %{_sysconfdir}/%{name}.conf
%{_sbindir}/%{name}-collect
%{_sbindir}/%{name}-preload
%{_sbindir}/%{name}-realloc
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man8/%{name}-collect.8*
%{_mandir}/man8/%{name}-preload.8*
%{_mandir}/man8/%{name}-realloc.8*

%files %{libname}
%{_libdir}/lib*%{name}-core.so
%{_libdir}/lib*%{name}-core.so.%{major}
