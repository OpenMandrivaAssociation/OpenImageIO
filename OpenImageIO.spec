%define _disable_ld_no_undefined 1

%define major %(echo %{version} |cut -d. -f1-2)
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d
%define utillibname %mklibname %{name}_Util
%define __requires_exclude cmake.*IlmBase
%bcond_without	full

Summary:	Library for reading and writing images
Name:		OpenImageIO
Version:	3.1.6.2
Release:	1
Group:		System/Libraries
License:	BSD
Url:		https://sites.google.com/site/openimageio/home
Source0:	https://github.com/AcademySoftwareFoundation/OpenImageIO/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://github.com/Tessil/robin-map/archive/refs/tags/v1.4.0.tar.gz
Patch0:		oiio-2.2.8.0-missing-include.patch
Patch1:		oiio-find-current-tbb.patch
#Patch2:		https://github.com/AcademySoftwareFoundation/OpenImageIO/pull/4870.patch
Patch3:		oiio-fix-robinmap.patch

BuildRequires:	cmake
BuildRequires:  cmake(pybind11)
BuildRequires:	txt2man
BuildRequires:	boost-devel
BuildRequires:	boost-align-devel
BuildRequires:	boost-core-devel
BuildRequires:	pugixml-devel
BuildRequires:	tiff-devel
BuildRequires:	git-core
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(Imath)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:  pkgconfig(libunwind-llvm)
BuildRequires:	pkgconfig(fmt)
BuildRequires:	cmake(OpenColorIO)
%if %{with full}
BuildRequires:	cmake(ECM)
BuildRequires:	pkgconfig(yaml-cpp)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	qt6-qtbase-theme-gtk3
BuildRequires:	pkgconfig(OpenColorIO)
BuildRequires:	pkgconfig(glew)
BuildRequires:  pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
%endif

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
%autosetup -p1 -n %{name}-%{version}
sed -i -e '/list.*APPEND.*cli_tools.*iv/d' src/doc/CMakeLists.txt

# If  this doesn't exist, cmake downloads it from git
tar xf %{S:1}
mkdir ext
mv robin-map-* ext/robin-map

# Remove bundled pugixml
rm -f src/include/pugixml.hpp \
	src/include/pugiconfig.hpp \
	src/libutil/pugixml.cpp

# Remove bundled tbb
rm -rf src/include/tbb

%build
%ifarch %{ix86}
# Because of incompatibility between boost-atomic 1.67 headers and clang 7.0:
# /usr/include/boost/atomic/detail/ops_gcc_x86_dcas.hpp:163:21: error: address argument to atomic builtin cannot be const-qualified
export CC=gcc
export CXX=g++
%endif

%cmake \
	-Wno-dev \
	-DTBB_INCLUDE_DIR:PATH=%{_includedir}/oneapi \
	-DCMAKE_SKIP_RPATH:BOOL=TRUE \
	-DPYLIB_INSTALL_DIR:PATH=%{python3_sitearch} -DPYTHON_VERSION=%{py3_ver} \
	-DINCLUDE_INSTALL_DIR:PATH=/usr/include/%{name} \
	-DINSTALL_DOCS:BOOL=OFF \
	-DSTOP_ON_WARNING=OFF \
	-DUSE_EXTERNAL_PUGIXML:BOOL=ON \
	-DOpenGL_GL_PREFERENCE=GLVND \
	../

%make_build

%install
%make_install -C build

%files
%{_bindir}/*
%{_xfontdir}/%{name}
%{python3_sitearch}/OpenImageIO

%files -n %{libname}
%{_libdir}/libOpenImageIO.so.%{major}*

%files -n %{utillibname}
%{_libdir}/libOpenImageIO_Util.so.%{major}*

%files -n %{devname}
%{_libdir}/libOpenImageIO.so
%{_libdir}/libOpenImageIO_Util.so
%{_includedir}/*
%{_libdir}/pkgconfig/OpenImageIO.pc
%{_libdir}/cmake/OpenImageIO/*
#{_datadir}/cmake/Modules/FindOpenImageIO.cmake
