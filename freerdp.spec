%global commit0 3b8352690e5ff1ab34357a2df2b6e22423bcea38
%global date 20170831
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Can be rebuilt with FFmpeg/H264 support enabled by passing "--with=ffmpeg",
# "--with=x264" or "--with=openh264" to mock/rpmbuild; or by globally setting
# these variables:

#global _with_ffmpeg 1
#global _with_x264 1
#global _with_openh264 1

Name:           freerdp
Version:        2.0.0
Release:        34%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
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
    -DWITH_CLIENT=ON \
    -DWITH_DIRECTFB=OFF \
    -DWITH_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_GSM=ON \
    -DWITH_GSTREAMER_1_0=ON -DWITH_GSTREAMER_0_10=OFF \
    -DGSTREAMER_1_0_INCLUDE_DIRS=%{_includedir}/gstreamer-1.0 \
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
    .

make %{?_smp_mflags}

pushd winpr/tools/makecert-cli
make %{?_smp_mflags}
popd

%install
%make_install
%make_install COMPONENT=tools

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
* Mon Sep 11 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-34.20170831git3b83526
- Update to latest snapshot.
- Trim changelog.

* Mon Aug 07 2017 Björn Esser <besser82@fedoraproject.org> - 2:2.0.0-33.20170724gitf8c9f43
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-32.20170724gitf8c9f43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-31.20170724gitf8c9f43
- Update to latest snapshot, Talos security fixes.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-30.20170710gitf580bea
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-29.20170710gitf580bea
- Update to latest snapshot.

* Mon Jun 26 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-28.20170623git9904c32
- Update to latest snapshot.

* Mon May 15 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-27.20170512gitb1df835
- Update to latest snapshot.

* Thu Apr 20 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-26.20170419gitbfcf8e7
- Update to latest 2.0 snapshot.

* Thu Apr 13 2017 Orion Poplawski <orion@cora.nwra.com> - 2:2.0.0-25.20170317git8c68761
- Install tools via make install

* Wed Mar 22 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-24.20170317git8c68761
- Update to latest snapshot.

* Mon Mar 06 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-23.20170302git210de68
- Remove shared libxfreerdp-client shared library.

* Thu Mar 02 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-22.20170302git210de68
- Move libxfreerdp-client shared object into devel subpackage.

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
