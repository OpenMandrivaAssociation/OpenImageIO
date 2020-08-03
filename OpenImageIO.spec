%define major 2.1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define utillibname %mklibname %{name}_Util %{major}
#define _disable_lto 1
%bcond_without	full

Summary:	Library for reading and writing images
Name:		OpenImageIO
Version:	2.1.18.1
Release:	1
Group:		System/Libraries
License:	BSD
Url:		https://sites.google.com/site/openimageio/home
Source0:	https://github.com/OpenImageIO/oiio/archive/oiio-Release-%{version}.tar.gz

BuildRequires:	cmake
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
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(freetype2)
%if %{with full}
BuildRequires:	qt5-devel
BuildRequires:	qt5-platformtheme-gtk3
BuildRequires:	extra-cmake-modules
BuildRequires:	pkgconfig(OpenColorIO)
BuildRequires:	pkgconfig(IlmBase)
BuildRequires:	pkgconfig(glew)
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
%autosetup -p1 -n oiio-Release-%{version}
sed -i -e '/list.*APPEND.*cli_tools.*iv/d' src/doc/CMakeLists.txt

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
%{python3_sitearch}/OpenImageIO.so

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
%{_datadir}/cmake/Modules/FindOpenImageIO.cmake
