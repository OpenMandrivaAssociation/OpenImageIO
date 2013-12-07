%define major	1.0
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Summary:	Library for reading and writing images
Name:		OpenImageIO
Version:	1.0.9
Release:	5
Group:		System/Libraries
License:	BSD
Url:		https://sites.google.com/site/openimageio/home
Source0:	https://download.github.com/%{name}-oiio-Release-%{version}-0-g0b78dec.tar.gz
Patch1:		OpenImageIO-1.0.2-dl.patch
BuildRequires:	cmake
BuildRequires:	txt2man
BuildRequires:	boost-devel
BuildRequires:	pugixml-devel
BuildRequires:	qt4-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(OpenColorIO)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(IlmBase)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(python)
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

%description -n %{libname}
OpenImageIO is a library for reading and writing images.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for %{name} library.

%prep
%setup -qn %{name}-oiio-0d48631
%apply_patches

# Remove bundled pugixml
rm -f src/include/pugixml.hpp \
	src/include/pugiconfig.hpp \
	src/libutil/pugixml.cpp

%build
%cmake \
	-DCMAKE_SKIP_RPATH:BOOL=TRUE \
	-DPYLIB_INSTALL_DIR:PATH=%{python_sitearch} \
	-DINCLUDE_INSTALL_DIR:PATH=/usr/include/%{name} \
	-DINSTALL_DOCS:BOOL=OFF \
	-DUSE_EXTERNAL_PUGIXML:BOOL=ON \
	../src

%make

%install
%makeinstall_std -C build

# Move man pages to the right directory
mkdir -p %{buildroot}%{_mandir}/man1
cp -a build/doc/*.1 %{buildroot}%{_mandir}/man1

%files
%doc CHANGES LICENSE
%{_bindir}/*
%{python_sitearch}/OpenImageIO.so
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libOpenImageIO.so.%{major}*

%files -n %{devname}
%doc src/doc/*.pdf
%{_libdir}/libOpenImageIO.so
%{_includedir}/*

