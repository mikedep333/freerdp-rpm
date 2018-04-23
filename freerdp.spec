%global commit0 a9ecd6a6ccc71130805a6bf3214c169fc42746ba
%global date 20180405
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Can be rebuilt with FFmpeg/H264 support enabled by passing "--with=ffmpeg",
# "--with=x264" or "--with=openh264" to mock/rpmbuild; or by globally setting
# these variables:

#global _with_ffmpeg 1
#global _with_x264 1
#global _with_openh264 1

# Momentarily disable GSS support
# https://github.com/FreeRDP/FreeRDP/issues/4348
#global _with_gss 1

Name:           freerdp
Version:        2.0.0
Release:        41%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}.3
Epoch:          2
Summary:        Free implementation of the Remote Desktop Protocol (RDP)
License:        ASL 2.0
URL:            http://www.freerdp.com/

Source0:        https://github.com/FreeRDP/FreeRDP/archive/%{commit0}/FreeRDP-%{commit0}.tar.gz#/FreeRDP-%{shortcommit0}.tar.gz
Patch0:         freerdp-aarch64.patch
Patch1111: 0001-Rewrite-of-sound-and-microphone-channels.patch
Patch1112: 0002-Added-CMake-option-WITH_DSP_EXPERIMENTAL.patch
Patch1113: 0003-Fix-4462-Fallback-typedef-for-AudioFormatID-on-MacOS.patch
Patch1114: 0004-Initialized-ALSA-backend-format.patch
Patch1115: 0005-Added-AudioFormatFlags-fallback.patch
Patch1116: 0006-Free-dsp-context-on-close.patch
Patch1117: 0007-Fixed-formatting-of-changed-files.patch
Patch1118: 0008-Fixed-function-pointer-typedef-formatting.patch
Patch1119: 0009-Fixed-channel-duplicate-disconnect-handling.patch
Patch1120: 0010-Added-fake-rdpsnd-backend.patch
Patch1121: 0011-Fix-rdpsnd-channel-detached-handling.patch
Patch1122: 0012-rdpsnd-add-support-for-wave2-PDU-in-client-2.patch
Patch1123: 0013-Ensure-audin-channel-uses-supported-protocol-version.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  cmake >= 2.8
BuildRequires:  cups-devel
BuildRequires:  gsm-devel
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
%{?_with_x264:BuildRequires:  x264-devel}
BuildRequires:  pam-devel
BuildRequires:  xmlto
BuildRequires:  zlib-devel

BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-0.10)
BuildRequires:  pkgconfig(gstreamer-base-0.10)
BuildRequires:  pkgconfig(gstreamer-app-0.10)
BuildRequires:  pkgconfig(gstreamer-audio-0.10)
BuildRequires:  pkgconfig(gstreamer-fft-0.10)
BuildRequires:  pkgconfig(gstreamer-pbutils-0.10)
BuildRequires:  pkgconfig(gstreamer-video-0.10)
%{?_with_gss:BuildRequires:  pkgconfig(krb5) >= 1.13}
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(openssl)

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
%patch1111 -p1
%patch1112 -p1
%patch1113 -p1
%patch1114 -p1
%patch1115 -p1
%patch1116 -p1
%patch1117 -p1
%patch1118 -p1
%patch1119 -p1
%patch1120 -p1
%patch1121 -p1
%patch1122 -p1
%patch1123 -p1

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
    -DWITH_GSSAPI=%{?_with_gss:ON}%{?!_with_gss:OFF} \
    -DWITH_GSTREAMER_0_10=ON \
    -DWITH_IPP=OFF \
    -DWITH_JPEG=ON \
    -DWITH_MANPAGES=ON \
    -DWITH_OPENH264=%{?_with_openh264:ON}%{?!_with_openh264:OFF} \
    -DWITH_OPENSSL=ON \
    -DWITH_PCSC=ON \
    -DWITH_PULSE=ON \
    -DWITH_SERVER=ON -DWITH_SERVER_INTERFACE=ON \
    -DWITH_SHADOW_X11=ON -DWITH_SHADOW_MAC=ON \
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
%{_bindir}/xfreerdp
%{_mandir}/man1/winpr-hash.1.*
%{_mandir}/man1/winpr-makecert.1.*
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
%{_mandir}/man7/wlog.*

%files devel
%{_includedir}/freerdp2
%{_libdir}/cmake/FreeRDP2
%{_libdir}/cmake/FreeRDP-Client2
%{_libdir}/cmake/FreeRDP-Server2
%{_libdir}/cmake/FreeRDP-Shadow2
%{_libdir}/libfreerdp-client2.so
%{_libdir}/libfreerdp-server2.so
%{_libdir}/libfreerdp-shadow2.so
%{_libdir}/libfreerdp-shadow-subsystem2.so
%{_libdir}/libfreerdp2.so
%{_libdir}/pkgconfig/freerdp2.pc
%{_libdir}/pkgconfig/freerdp-client2.pc
%{_libdir}/pkgconfig/freerdp-server2.pc
%{_libdir}/pkgconfig/freerdp-shadow2.pc

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
* Mon Apr 23 2018 Mike DePaulo (GFDL) - 2:2.0.0-41.20180405gita9ecd6a.3
- Backport to EL6

* Mon Apr 23 2018 Mike DePaulo (GFDL) - 2:2.0.0-41.20180405gita9ecd6a.2
- Fix crash by applying 13 patches from FreeRDP upstream merge request #4453
  "Sound channel refactoring", written against a9ecd6a exactly.

* Mon Apr 16 2018 Mike DePaulo (GFDL) - 2:2.0.0-41.20180405gita9ecd6a.1
- Fix build on EL7 by reverting "use versioned build requirement on pkgconfig(openssl)"

* Mon Apr 09 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-41.20180405gita9ecd6a
- Update to latest snapshot.

* Wed Mar 21 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-40.20180320gitde83f4d
- Add PAM support (fixes freerdp-shadow-cli). Thanks Paolo Zeppegno.
- Update to latest snapshot.

* Thu Mar 15 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-39.20180314gitf8baeb7
- Update to latest snapshot.
- Fixes connection to RDP servers with the latest Microsoft patches:
  https://github.com/FreeRDP/FreeRDP/issues/4449

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-38.20180115git8f52c7e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Karsten Hopp <karsten@redhat.com> - 2.0.0-37git}
- use versioned build requirement on pkgconfig(openssl) to prevent using
  compat-openssl10-devel instead of openssl-devel

* Tue Jan 16 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-36.20180115git8f52c7e
- Update to latest snapshot.
- Make GSS support optional and disable it for now (#1534094 and FreeRDP #4348,
  #1435, #4363).

* Wed Dec 20 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-35.20171220gitbfe8359
- Update to latest snapshot post 2.0.0rc1.

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
