%global commit0 210de6833ceb5a97aa5a3755a647df45c04d8029
%global date 20170302
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Can be rebuilt with FFmpeg/H264 support enabled by passing "--with=ffmpeg",
# "--with=x264" or "--with=openh264" to mock/rpmbuild; or by globally setting
# these variables:

#global _with_ffmpeg 1
#global _with_x264 1
#global _with_openh264 1

Name:           freerdp
Version:        2.0.0
Release:        21%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Epoch:          2
Summary:        Free implementation of the Remote Desktop Protocol (RDP)
License:        ASL 2.0
URL:            http://www.freerdp.com/

Source0:        https://github.com/FreeRDP/FreeRDP/archive/%{commit0}/FreeRDP-%{commit0}.tar.gz#/FreeRDP-%{shortcommit0}.tar.gz
Patch0:         freerdp-aarch64.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  cmake >= 2.8
BuildRequires:  cups-devel
BuildRequires:  gsm-devel
BuildRequires:  openssl-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
%{?_with_openh264:BuildRequires:  openh264-devel}
%{?_with_x264:BuildRequires:  x264-devel}
BuildRequires:  xmlto
BuildRequires:  zlib-devel

BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-fft-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)

%{?_with_ffmpeg:
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
}

Provides:       xfreerdp = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}

%description
The xfreerdp Remote Desktop Protocol (RDP) client from the FreeRDP project.

xfreerdp can connect to RDP servers such as Microsoft Windows machines, xrdp and
VirtualBox.

%package        libs
Summary:        Core libraries implementing the RDP protocol
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-plugins < 1:1.1.0
Provides:       %{name}-plugins = %{?epoch}:%{version}-%{release}
%description    libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 2.8

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}-libs.

%package        server
Summary:        Server support for %{name}

%description    server
The %{name}-server package contains servers which can export a desktop via
the RDP protocol.

%package -n     libwinpr
Summary:        Windows Portable Runtime
Provides:       %{name}-libwinpr = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-libwinpr < %{?epoch}:%{version}-%{release}

%description -n libwinpr
WinPR provides API compatibility for applications targeting non-Windows
environments. When on Windows, the original native API is being used instead of
the equivalent WinPR implementation, without having to modify the code using it.

%package -n     libwinpr-devel
Summary:        Windows Portable Runtime development files
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 2.8

%description -n libwinpr-devel
The %{name}-libwinpr-devel package contains libraries and header files for
developing applications that use %{name}-libwinpr.

%prep
%setup -qn FreeRDP-%{commit0}
%patch0 -p1 -b .aarch64

# Rpmlint fixes
find . -name "*.h" -exec chmod 664 {} \;
find . -name "*.c" -exec chmod 664 {} \;

%build
%cmake %{?_cmake_skip_rpath} \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
    -DWITH_ALSA=ON \
    -DWITH_CUPS=ON \
    -DWITH_CHANNELS=ON -DBUILTIN_CHANNELS=OFF \
    -DWITH_CLIENT=ON -DWITH_CLIENT_INTERFACE=ON \
    -DWITH_DIRECTFB=OFF \
    -DWITH_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_GSM=ON \
    -DWITH_GSTREAMER_1_0=ON -DWITH_GSTREAMER_0_10=OFF \
    -DWITH_IPP=OFF \
    -DWITH_JPEG=ON \
    -DWITH_KRB5=ON \
    -DWITH_MANPAGES=ON \
    -DWITH_OPENH264=%{?_with_openh264:ON}%{?!_with_openh264:OFF} \
    -DWITH_OPENSSL=ON \
    -DWITH_PCSC=ON \
    -DWITH_PULSE=ON \
    -DWITH_SERVER=ON -DWITH_SERVER_INTERFACE=ON \
    -DWITH_WAYLAND=ON \
    -DWITH_X11=ON \
    -DWITH_X264=%{?_with_x264:ON}%{?!_with_x264:OFF} \
    -DWITH_XCURSOR=ON \
    -DWITH_XEXT=ON \
    -DWITH_XKBFILE=ON \
    -DWITH_XI=ON \
    -DWITH_XINERAMA=ON \
    -DWITH_XRENDER=ON \
    -DWITH_XTEST=OFF \
    -DWITH_XV=ON \
    -DWITH_ZLIB=ON \
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
%ifarch aarch64
    -DWITH_SSE2=OFF \
%endif
    .

make %{?_smp_mflags}

pushd winpr/tools/makecert-cli
make %{?_smp_mflags}
popd

%install
%make_install
install -p -m 0755 winpr/tools/makecert-cli/winpr-makecert %{buildroot}%{_bindir}/

find %{buildroot} -name "*.a" -delete

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post -n libwinpr -p /sbin/ldconfig

%postun -n libwinpr -p /sbin/ldconfig

%files
%{_bindir}/winpr-hash
%{_bindir}/winpr-makecert
%{_bindir}/wlfreerdp
%{_bindir}/xfreerdp
%{_mandir}/man1/winpr-hash.1.*
%{_mandir}/man1/winpr-makecert.1.*
%{_mandir}/man1/wlfreerdp.1.*
%{_mandir}/man1/xfreerdp.1.*

%files libs
%license LICENSE
%doc README ChangeLog
%{_libdir}/freerdp2/
%{_libdir}/libfreerdp-client2.so.*
%{_libdir}/libfreerdp-server2.so.*
%{_libdir}/libfreerdp-shadow2.so.*
%{_libdir}/libfreerdp-shadow-subsystem2.so.*
%{_libdir}/libfreerdp2.so.*
%{_libdir}/libxfreerdp-client.so
%{_libdir}/libuwac0.so.*
%{_mandir}/man7/wlog.*

%files devel
%{_includedir}/freerdp2
%{_includedir}/uwac0
%{_libdir}/cmake/FreeRDP2
%{_libdir}/cmake/FreeRDP-Client2
%{_libdir}/cmake/FreeRDP-Server2
%{_libdir}/cmake/FreeRDP-Shadow2
%{_libdir}/cmake/uwac0
%{_libdir}/libfreerdp-client2.so
%{_libdir}/libfreerdp-server2.so
%{_libdir}/libfreerdp-shadow2.so
%{_libdir}/libfreerdp-shadow-subsystem2.so
%{_libdir}/libfreerdp2.so
%{_libdir}/libuwac0.so
%{_libdir}/pkgconfig/freerdp2.pc
%{_libdir}/pkgconfig/freerdp-client2.pc
%{_libdir}/pkgconfig/freerdp-server2.pc
%{_libdir}/pkgconfig/freerdp-shadow2.pc
%{_libdir}/pkgconfig/uwac0.pc

%files server
%{_bindir}/freerdp-shadow-cli
%{_mandir}/man1/freerdp-shadow-cli.1.*

%files -n libwinpr
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README ChangeLog
%{_libdir}/libwinpr2.so.*
%{_libdir}/libwinpr-tools2.so.*

%files -n libwinpr-devel
%{_libdir}/cmake/WinPR2
%{_includedir}/winpr2
%{_libdir}/libwinpr2.so
%{_libdir}/libwinpr-tools2.so
%{_libdir}/pkgconfig/winpr2.pc
%{_libdir}/pkgconfig/winpr-tools2.pc

%changelog
* Thu Mar 02 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-21.20170302git210de68
- Update to latest snapshot.
- Update build requirements, tune build options.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-20.20161228git90877f5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-19.20161228git90877f5
- Update to latest snapshot.

* Sat Dec 03 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-18.20161202gitd72ff5d
- Update to latest snapshot.

* Fri Nov 04 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-17.20161103gitea24c1f
- Update to latest snapshot.

* Thu Oct 20 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-16.20161020gita6f4117
- Update to latest snapshot.

* Fri Oct 14 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-15.20161014git9adc132
- Update to latest snapshot.

* Sat Oct 08 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-14.20161006git267dea9
- Update build options.

* Sat Oct 08 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-13.20160909git267dea9
- Update to latest snapshot.

* Tue Sep 20 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-12.20160909git1855e36
- Update to latest snapshot, update release to follow packaging guidelines.

* Fri Aug 12 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-11.git.5b2455f
- Update to latest snapshot.

* Tue Jun 21 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-10.git.e86f7c2
- Update to latest sources.

* Tue Jun 07 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-9.git.aa15327
- Update to latest sources.

* Tue May 24 2016 David Woodhouse <dwmw2@infradead.org> - 2:2.0.0-8.git.53de4b8
- Update to latest sources

* Fri May 20 2016 David Woodhouse <dwmw2@infradead.org> - 2:2.0.0-7.git.aeabb95
- Update to latest sources, adjust set of exported libraries.

* Thu Apr 21 2016 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-6.git.ca2d015
- Update to latest sources, adjust path of libraries.
- Add OpenH264 conditional.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-5.git.b02943a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 13 2015 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-4.git.b02943a
- Add FFMpeg/x264 build conditional.

* Sun Dec 13 2015 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-3.git.b02943a
- Move winpr-makecert into main package.

* Sun Dec 13 2015 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-2.git.b02943a
- Update to latest snapshot.
- Build winpr-makecert (#1288900).

* Sun Nov 15 2015 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-1.git.be8f8f7
- Update to latest snapshot, remove upstreamed patches.
- Update to new packaging guidelines for GitHub sources and license tag.
- Adjust CMake options to latest release, enable Wayland backend.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.2.0-0.10.git.24a752a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 22 2015 Kalev Lember <kalevlember@gmail.com> - 2:1.2.0-0.9.git.24a752a
- Bump epoch after the version downgrade

* Wed Mar 18 2015 David Woodhouse <dwmw2@infradead.org> - 1:1.2.0-0.8.git.24a752a
- Fix version number. No epoch++ since it was only in rawhide & f22-beta updates-testing.

* Tue Mar 17 2015 David Woodhouse <dwmw2@infradead.org> - 1:1.2.1-0.2.git.24a752a
- Revert to an older snapshot (+fixes) to fix guacamole-server build failure

* Fri Mar 13 2015 Simone Caronni <negativo17@gmail.com> - 1:1.2.1-0.1.git.6ac7180
- Use packaging guidelines for Github snapshots.
- Version is now at 1.2.1-dev.

* Fri Mar 13 2015 David Woodhouse <dwmw2@infradead.org> - 1:1.2.0-0.7.beta.1
- Update to git snapshot (dfc12385) and enable server build

* Thu Jan 15 2015 Orion Poplawski <orion@cora.nwra.com> - 1:1.2.0-0.6.beta.1
- Use better upstream patch to fix command line parsing

* Wed Jan 14 2015 Orion Poplawski <orion@cora.nwra.com> - 1:1.2.0-0.5.beta.1
- Add patch to fix command line parsing segfault (bug #1150349) and to
  fix old style command line options

* Tue Dec 16 2014 Simone Caronni <negativo17@gmail.com> - 1:1.2.0-0.4.beta.1
- Fix build on CMake 3.1.

* Wed Nov 12 2014 Simone Caronni <negativo17@gmail.com> - 1:1.2.0-0.3.beta.1
- Update to latest 1.2.0 beta 1 refresh.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-0.2.beta.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Simone Caronni <negativo17@gmail.com> - 1:1.2.0-0.1.beta.1
- Update to latest 1.2.0 beta 1.
- Rename freerdp-libwinpr to libwinpr and create a separate libwinpr-devel
  subpackage now that is considered a different set of libraries.
- Put CMake files in devel subpackages.
- Enable new Gstreamer 1.0, OpenSSL, JPEG, GSM, Zlib, libXi and Xrandr support.
- Disable static channels.
- Add new BuildRequires, build options and sort them.
- Fix rpmlint complaints.
- Align all description etc. to column 80.
- Remove desktop file for xfreerdp, it is command line only and has its own
  icon.

* Sat Jun  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.1.0-0.12.beta.2013071101
- Fix aarch64

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.0-0.11.beta.2013071101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Mads Kiilerich <mads@kiilerich.com> - 1:1.1.0-0.10.beta.2013071101
- Fix PulseAudio define

* Sun Feb  2 2014 Ville Skyttä <ville.skytta@iki.fi> - 1:1.1.0-0.9.beta.2013071101
- Install SVG icon.

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1:1.1.0-0.8.beta.2013071101
- Disable RPATH.

* Mon Nov 04 2013 Kalev Lember <kalevlember@gmail.com> - 1.1.0-0.7.beta.2013071101
- Add missing epoch to freerdp-plugins obsoletes

* Tue Sep 10 2013 Simone Caronni <negativo17@gmail.com> - 1.1.0-0.6.beta.2013071101
- Add epoch to requirements.

* Tue Sep 10 2013 Simone Caronni <negativo17@gmail.com> - 1.1.0-0.5.beta.2013071101
- Bump epoch.

* Thu Sep 05 2013 Mads Kiilerich <mads@kiilerich.com> - 1.1.0-0.4.beta.2013071101
- libxfreerdp-client is needed ...

* Tue Sep 03 2013 Mads Kiilerich <mads@kiilerich.com> - 1.1.0-0.3.beta1
- Add missing ldconfig for libwinpr
- Based on patch from Simone Caronni:
- Update to the latest beta 1 refresh (1.1.0-beta+2013071101).
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
