%define major   0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
#define devstat %%mklibname %%{name} -d -s

Name:           hackrf
Version:        2018.01.1
Release:        1
Summary:        A project to produce a low cost open source software radio platform
Group:          Communications/Radio
License:        GPLv2
# https://github.com/mossmann/hackrf/wiki
URL:            https://github.com/mossmann/%{name}/wiki
Source0:        https://github.com/mossmann/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  pkgconfig(libusb)
BuildRequires:  systemd
BuildRequires:  pkgconfig(fftw3)

%description
Hardware designs and software for HackRF, a project to produce a low cost, open
source software radio platform.

%package -n %{libname}
Summary:        Library files for %{name}
Requires:       %{name} = %{version}-%{release}

%package -n %{devname}
Summary:        Development files for %{name}
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%package doc
Requires:       %{name} = %{version}-%{release}
Summary:        Supplemental documentation for HackRF
BuildArch:      noarch

%if %{defined devstat}
%package -n %{devstat}
Summary:        Static libraries for libhackrf
Requires:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-static-devel = %{version}-%{release}

%description -n %{devstat}
Static libraries for libhackrf.

%files -n %{devstat}
%{_libdir}/libhackrf.a
%endif

%description -n %{devname}
Files needed to develop software against libhackrf.

%description -n %{libname}
hackrf library files.

%description doc
Supplemental documentation for HackRF. For more information, visit the wiki at
https://github.com/mossmann/hackrf/wiki

%prep
%setup -q

# Fix "plugdev" nonsense
sed -i -e 's/GROUP="plugdev"/ENV{ID_SOFTWARE_RADIO}="1"/g' host/libhackrf/53-hackrf.rules

%build
pushd host
%cmake \
    -DINSTALL_UDEV_RULES=on \
    -DUDEV_RULES_PATH=%{_udevrulesdir}
%make_build
popd

%install
%make_install -C host/build

%if ! %{defined devstat}
rm -f %{buildroot}%{_libdir}/libhackrf.a
%endif

%files
%doc TRADEMARK Readme.md
%{_bindir}/hackrf_*
%{_udevrulesdir}/53-hackrf.rules

%files -n %{libname}
%{_libdir}/libhackrf.so.%{major}{,.*}

%files -n %{devname}
%{_includedir}/libhackrf/hackrf.h
%{_libdir}/pkgconfig/libhackrf.pc
%{_libdir}/libhackrf.so

%files doc
%doc doc/*
