%define		major		0.10
%define		libname		%mklibname OpenImageIO %{major}
%define		develname	%mklibname OpenImageIO -d

Name:		OpenImageIO
Version:	0.10.4
Release:	%mkrel 1
Summary:	Library for reading and writing images
Group:		System/Libraries
License:	BSD
URL:		https://sites.google.com/site/openimageio/home
Source0:	https://download.github.com/%{name}-oiio-Release-%{version}-0-gad1950d.tar.gz
Patch0:		OpenImageIO-0.10.2-git_backports.patch
Patch1:		OpenImageIO-0.10.4-dl.patch
Patch2:		OpenImageIO-0.10.2-Z_BEST_COMPRESSION.patch
BuildRequires:	boost-devel
BuildRequires:	glew-devel
BuildRequires:	qt4-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	ilmbase-devel
BuildRequires:	python-devel
BuildRequires:	txt2man
BuildRequires:	png-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
BuildRequires:	jasper-devel
BuildRequires:	pugixml-devel

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

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files for %{name} library.

%prep
%setup -q -n %{name}-oiio-ad1950d

%patch0 -p1
%patch1 -p1
%patch2 -p1

# Remove bundled pugixml
rm -f src/include/pugixml.hpp \
      src/include/pugiconfig.hpp \
      src/libutil/pugixml.cpp

%build
%cmake -DCMAKE_SKIP_RPATH:BOOL=TRUE \
       -DPYLIB_INSTALL_DIR:PATH=%{python_sitearch} \
       -DINCLUDE_INSTALL_DIR:PATH=/usr/include/%{name} \
       -DINSTALL_DOCS:BOOL=OFF \
       -DUSE_EXTERNAL_PUGIXML:BOOL=ON \
       ../src

%make

%install
%__rm -rf %{buildroot}
%makeinstall_std -C build

# Move man pages to the right directory
%__mkdir_p %{buildroot}%{_mandir}/man1
%__cp -a build/doc/*.1 %{buildroot}%{_mandir}/man1

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES LICENSE
%{_bindir}/*
%{python_sitearch}/OpenImageIO.so
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libOpenImageIO.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc src/doc/*.pdf
%{_libdir}/libOpenImageIO.so
%{_includedir}/*

