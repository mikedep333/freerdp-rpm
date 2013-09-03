Name:           freerdp
Version:        1.1.0
Release:        0.2.beta1%{?dist}
Summary:        Remote Desktop Protocol client

License:        ASL 2.0
URL:            http://www.freerdp.com/
Source0:        http://pub.freerdp.com/releases/%{name}-%{version}-beta1.tar.gz

BuildRequires:  cmake
BuildRequires:  xmlto
BuildRequires:  openssl-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXv-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  cups-devel
BuildRequires:  pcsc-lite-devel
BuildRequires:  desktop-file-utils

Provides:       xfreerdp = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-libwinpr%{?_isa} = %{version}-%{release}

%description
The xfreerdp Remote Desktop Protocol (RDP) client from the FreeRDP
project.

xfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.


%package        libs
Summary:        Core libraries implementing the RDP protocol
Requires:       %{name}-libwinpr%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-plugins < 1.1.0-0
Provides:       %{name}-plugins = %{version}-%{release}
%description    libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.


%package        libwinpr
Summary:        FreeRDP Windows API runtime
%description    libwinpr
An implementation of much of Windows' APIs.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-libwinpr%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name} libs.


%prep

%setup -q -n freerdp-1.1.0-beta1

cat << EOF > xfreerdp.desktop 
[Desktop Entry]
Type=Application
Name=X FreeRDP
NoDisplay=true
Comment=Connect to RDP server and display remote desktop
Icon=%{name}
Exec=/usr/bin/xfreerdp
Terminal=false
Categories=Network;RemoteAccess;
EOF


%build

%cmake \
        -DWITH_CUPS=ON \
        -DWITH_PCSC=ON \
        -DWITH_PULSEAUDIO=ON \
        -DWITH_X11=ON \
        -DWITH_XCURSOR=ON \
        -DWITH_XEXT=ON \
        -DWITH_XINERAMA=ON \
        -DWITH_XKBFILE=ON \
        -DWITH_XV=ON \
        -DWITH_ALSA=OFF \
        -DWITH_CUNIT=OFF \
        -DWITH_DIRECTFB=OFF \
        -DWITH_FFMPEG=OFF \
%ifarch x86_64
        -DWITH_SSE2=ON \
%else
        -DWITH_SSE2=OFF \
%endif
%ifarch armv7hl
        -DARM_FP_ABI=hard \
        -DWITH_NEON=OFF \
%endif
%ifarch armv7hnl
        -DARM_FP_ABI=hard \
        -DWITH_NEON=ON \
%endif
%ifarch armv5tel armv6l armv7l
        -DARM_FP_ABI=soft \
        -DWITH_NEON=OFF \
%endif
        -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
        .

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications xfreerdp.desktop
install -p -m 644 -D resources/FreeRDP_Icon_256px.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png


%post
# This is no gtk application, but try to integrate nicely with GNOME if it is available
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%{_bindir}/xfreerdp
%{_mandir}/man1/xfreerdp.*
%{_datadir}/applications/xfreerdp.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

%files libs
%{_libdir}/lib%{name}-*.so.*

%files libwinpr
%doc LICENSE README ChangeLog
%{_libdir}/libwinpr-*.so.*

%files devel
%{_includedir}/%{name}/
%{_includedir}/winpr/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Sep 03 2013 Mads Kiilerich <mads@kiilerich.com> - 1.1.0-0.3.beta1
- Remove obsolete defattr, Group and BuildRoot RPM tags for Fedora / RHEL 6+.
- Move license file and documentation to libwinpr subpackage so any combination
  of installed packages result in the LICENSE file available.

* Sun Sep 01 2013 Mads Kiilerich <mads@kiilerich.com> - 1.1.0-0.2.beta1
- SSE2 should only be used on x86_64

* Sun Sep 01 2013 Dennis Gilmore <dennis@ausil.us> - 1.1.0-0.1.beta1
- disable neon on armv7hl and armv5tel
- set arm floating point correctly for the different targets

* Sun Sep 01 2013 Mads Kiilerich <mads@kiilerich.com> - 1.1.0-0.beta+2013071101
- Update to 1.1.0 beta1, add winpr package, drop plugins package.
- Drop unnecessary rm -rf of build roots.

* Sat Aug 31 2013 Mads Kiilerich <mads@kiilerich.com> - 1.0.2-4
- don't make freerdp.png executable

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Mads Kiilerich <mads@kiilerich.com> - 1.0.2-1
- freerdp-1.0.2

* Sun Sep 30 2012 Mads Kiilerich <mads@kiilerich.com> - 1.0.1-7
- merge f17 1.0.1-6 - Backport fix for bug 816692

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 29 2012 Mads Kiilerich <mads@kiilerich.com> - 1.0.1-5
- Use new upstream tar with standard naming
- Use _isa for subpackage dependencies

* Tue Feb 28 2012 Mads Kiilerich <mads@kiilerich.com> - 1.0.1-4
- Include patch for sending invalid extra data

* Tue Feb 28 2012 Mads Kiilerich <mads@kiilerich.com> - 1.0.1-3
- Install a freedesktop .desktop file and a high-res icon instead of relying on
  _NET_WM_ICON

* Sat Feb 25 2012 Mads Kiilerich <mads@kiilerich.com> - 1.0.1-2
- Explicit build requirement for xmlto - needed for EL6

* Wed Feb 22 2012 Mads Kiilerich <mads@kiilerich.com> - 1.0.1-1
- FreeRDP-1.0.1 - major upstream rewrite and relicensing under Apache license

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Mads Kiilerich <mads@kiilerich.com> - 0.8.2-2
- rebuild on rawhide because of broken dependencies

* Tue Nov 16 2010 Mads Kiilerich <mads@kiilerich.com> - 0.8.2-1
- freerdp-0.8.2

* Mon Nov 08 2010 Mads Kiilerich <mads@kiilerich.com> - 0.8.1-2
- make -devel require pkgconfig
- first official Fedora package

* Sun Nov 07 2010 Mads Kiilerich <mads@kiilerich.com> - 0.8.1-1
- freerdp-0.8.1

* Sat Sep 25 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.4-2
- hack the generated libtool to not set rpath on x86_64
- configure with alsa explicitly

* Tue Aug 24 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.4-1
- freerdp-0.7.4
- cleanup of packaging structure

* Wed Jul 28 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.3-1
- 0.7.3
- fix some minor pylint warnings

* Fri Jul 23 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.2-2
- 0.7.2
- Address many comments from cwickert:
- - cleanup of old formatting, alignment with spectemplate-lib.spec and
    cwickert spec from #616193
- - add alsa as build requirement
- - remove superfluous configure options and disable static libs
- - add missing rpm groups

* Sun Jun 13 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.0-1
- First official release, first review request
