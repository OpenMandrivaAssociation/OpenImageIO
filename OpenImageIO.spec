%define major 1.8
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define utillibname %mklibname %{name}_Util %{major}
%define _disable_lto 1

Summary:	Library for reading and writing images
Name:		OpenImageIO
Version:	1.8.9
Release:	1
Group:		System/Libraries
License:	BSD
Url:		https://sites.google.com/site/openimageio/home
Source0:	https://github.com/OpenImageIO/oiio/archive/Release-%{version}.tar.gz
Patch0:		OpenImageIO-1.4.13-dl.patch
BuildRequires:	cmake
BuildRequires:	txt2man
BuildRequires:	boost-devel
BuildRequires:	boost-align-devel
BuildRequires:	boost-core-devel
BuildRequires:	pugixml-devel
BuildRequires:	qt5-devel
BuildRequires:	extra-cmake-modules
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(OpenColorIO)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(IlmBase)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(zlib)

%description
OpenImageIO is a library for reading and writing images, and a bunch of related
classes, utilities, and applications. Main features include:
- Extremely simple but powerful ImageInput and ImageOutput APIs for reading and
  writing 2D images that is format agnostic.
- Format plugins for TIFF, JPEG/JFIF, OpenEXR, PNG, HDR/RGBE, Targa, JPEG-2000,
  DPX, Cineon, FITS, BMP, ICO, RMan Zfile, Softimage PIC, DDS, SGI,
  PNM/PPM/PGM/PBM, Field3d.
- An ImageCache class that transparently manages a cache so that it can access
  truly vast amounts of image data.
- A really nice image viewer, iv, also based on OpenImageIO classes (and so
  will work with any formats for which plugins are available).

%package -n %{libname}
Summary:	A library for reading and writing images
Group:		System/Libraries
%rename		%{_lib}OpenImageIO1.0

%description -n %{libname}
OpenImageIO is a library for reading and writing images.

%package -n %{utillibname}
Summary:        A library for reading and writing images
Group:          System/Libraries

%description -n %{utillibname}
OpenImageIO is a library for reading and writing images.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Requires:	%{utillibname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for %{name} library.

%prep
%setup -qn oiio-Release-%{version}
%apply_patches
sed -i -e '/list.*APPEND.*cli_tools.*iv/d' src/doc/CMakeLists.txt

# Remove bundled pugixml
rm -f src/include/pugixml.hpp \
	src/include/pugiconfig.hpp \
	src/libutil/pugixml.cpp

# Remove bundled tbb
rm -rf src/include/tbb

%build

# clang segfaults on i586
%ifarch %{ix86}
export CC=gcc
export CXX=g++
%endif

%cmake \
	-DCMAKE_SKIP_RPATH:BOOL=TRUE \
	-DPYLIB_INSTALL_DIR:PATH=%{python3_sitearch} -DPYTHON_VERSION=%{py3_ver} \
	-DINCLUDE_INSTALL_DIR:PATH=/usr/include/%{name} \
	-DINSTALL_DOCS:BOOL=OFF \
	-DSTOP_ON_WARNING=OFF \
	-DUSE_EXTERNAL_PUGIXML:BOOL=ON \
	../

%make

%install
%makeinstall_std -C build

%files
%doc LICENSE
%{_bindir}/*
%{_xfontdir}/%{name}
%{python3_sitearch}/OpenImageIO.so

%files -n %{libname}
%{_libdir}/libOpenImageIO.so.%{major}*

%files -n %{utillibname}
%{_libdir}/libOpenImageIO_Util.so.%{major}*

%files -n %{devname}
%doc src/doc/*.pdf
%{_libdir}/libOpenImageIO.so
%{_libdir}/libOpenImageIO_Util.so
%{_includedir}/*
