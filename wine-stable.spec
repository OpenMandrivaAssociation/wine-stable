%ifarch x86_64
%define	wine	wine64-stable
%define	mark64	()(64bit)
%else
%define	wine	wine-stable
%define	mark64	%{nil}
%endif
%define	lib_name_orig	lib%{name}
%define	lib_major	1
%define	lib_name	%mklibname %{name} %{lib_major}
%define	lib_name_devel	%{mklibname -d wine}
%define	oname 		wine


# On 32-bit we have
# wine32 - those 32-bit binaries that are also used on 64-bit for 32-bit support
# wine - all other files (requires 'wine32')
# On 64-bit we have
# wine64 - all 64-bit files (suggests 'wine32')
# - Anssi 07/2010

Name:		wine-stable
#(peroyvind): please do backports for new versions
Version:	1.4.1
%define rel	1.1
Release:	%mkrel %{rel}
%define o_ver	%{version}
Epoch:		1
Summary:	WINE Is Not An Emulator - runs MS Windows programs
License:	LGPLv2+
Group:		Emulators
URL:		https://www.winehq.com/
Source0:	http://ibiblio.org/pub/linux/system/emulators/wine/%{oname}-%{o_ver}.tar.bz2
Source1:	http://ibiblio.org/pub/linux/system/emulators/wine/%{oname}-%{o_ver}.tar.bz2.sign

# RH stuff
Source2:        wine.init
Source10:	wine.rpmlintrc
Patch0:		wine-1.0-rc3-fix-conflicts-with-openssl.patch
Patch1:		wine-1.1.7-chinese-font-substitutes.patch
# (Anssi 05/2008) Adds:
# a: => /media/floppy (/mnt/floppy on 2007.1 and older)
# d: => $HOME (at config_dir creation time, not refreshed if $HOME changes;
#              note that Wine also provides $HOME in My Documents)
# only on 2008.0: e: => /media/cdrom (does not exist on 2008.1+)
# only on 2007.1 and older: e: => /mnt/cdrom
# com4 => /dev/ttyUSB0 (replaces /dev/ttyS3)
# have to substitute @MDKVERSION@ in dlls/ntdll/server.c
Patch108:	wine-mdkconf.patch

#(eandry) add a pulseaudio sound driver (from http://art.ified.ca/downloads/ )

# Rediff configure.ac patch manually until winepulse upstream fixes it

# (anssi) Wine needs GCC 4.4+ on x86_64 for MS ABI support. Note also that
# 64-bit wine cannot run 32-bit programs without wine32.
ExclusiveArch:	%{ix86}
%if %mdkversion >= 201010
ExclusiveArch:	x86_64
%endif
%ifarch x86_64
BuildRequires:	gcc >= 4.4
%endif

BuildRequires:  bison flex
BuildRequires:  gpm-devel 
BuildRequires:  perl-devel
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  cups-devel   
BuildRequires:  sane-devel   
BuildRequires:  lcms-devel   
BuildRequires:  autoconf     
BuildRequires:  docbook-utils docbook-dtd-sgml
BuildRequires:  docbook-utils docbook-dtd-sgml sgml-tools
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  libmpg123-devel 
BuildRequires:  openal-devel    
BuildRequires:  alsa-oss-devel   
BuildRequires:  pkgconfig(gstreamer-0.10) libgstreamer0.10-plugins-base-devel
BuildRequires:  isdn4k-utils-devel
BuildRequires:  glibc-static-devel
BuildRequires:  chrpath
BuildRequires:  ungif-devel pkgconfig(xpm)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  librsvg   
BuildRequires:  imagemagick
BuildRequires:  pkgconfig(libgphoto2)
BuildRequires:  desktop-file-utils
BuildRequires:  openldap-devel    
BuildRequires:  pkgconfig(libxslt)     
BuildRequires:  dbus-devel        
BuildRequires:  valgrind          
BuildRequires:  gsm-devel         
BuildRequires:  unixODBC-devel    
BuildRequires:  pkgconfig(gnutls)      
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(glu)
BuildRequires:  libv4l-devel 
BuildRequires:  libxcursor-devel libxcomposite-devel
BuildRequires:  pkgconfig(xinerama) pkgconfig(xrandr)   
BuildRequires:  pkgconfig(x11) pkgconfig(xrender)
BuildRequires:  pkgconfig(xext) libsm-devel
BuildRequires:  fontforge fontconfig-devel pkgconfig(freetype2)

BuildRequires:	bison flex gpm-devel perl-devel pkgconfig(ncurses) sgml-tools
BuildRequires:	pkgconfig(x11) pkgconfig(xrender) pkgconfig(xext) libsm-devel
BuildRequires:	pkgconfig(freetype2) autoconf docbook-utils docbook-dtd-sgml
BuildRequires:	cups-devel pkgconfig(jack) imagemagick isdn4k-utils-devel pkgconfig(xpm)
BuildRequires:	sane-devel glibc-static-devel ungif-devel chrpath
BuildRequires:	desktop-file-utils alsa-oss-devel openldap-devel lcms-devel
BuildRequires:	pkgconfig(libxslt) dbus-devel
BuildRequires:	valgrind librsvg pkgconfig(libpulse) gettext-devel
BuildRequires:	gsm-devel
BuildRequires:	pkgconfig(glu)
BuildRequires:	fontforge
BuildRequires:	unixODBC-devel
BuildRequires:	libmpg123-devel
BuildRequires:	openal-devel pkgconfig(xrandr) pkgconfig(xinerama) libxcomposite-devel
BuildRequires:	libxcursor-devel fontconfig-devel
BuildRequires:	pkgconfig(gnutls) pkgconfig(libtiff-4) libv4l-devel
BuildRequires:	pkgconfig(gstreamer-0.10) libgstreamer0.10-plugins-base-devel
%if %mdvver >= 201100
BuildRequires:	prelink
%endif

%define desc Wine is a program which allows running Microsoft Windows programs \
(including DOS, Windows 3.x and Win32 executables) on Unix. It \
consists of a program loader which loads and executes a Microsoft \
Windows binary, and a library (called Winelib) that implements Windows \
API calls using their Unix or X11 equivalents.  The library may also \
be used for porting Win32 code into native Unix executables.

%ifarch x86_64
%package -n	%{wine}
Summary:	WINE Is Not An Emulator - runs MS Windows programs
Group:		Emulators
Suggests:	wine32 = %{EVRD}
Suggests:	wine64-gecko
%else
# on 32-bit we always want wine32 package
Requires:	wine32 = %{EVRD}
%endif

Provides:	%{wine}-utils = %{EVRD} %{wine}-full = %{EVRD}
Provides:	%{lib_name}-capi = %{EVRD} %{lib_name}-twain = %{EVRD}
Provides:	%{lib_name} = %{EVRD}
Provides:	wine-bin = %{EVRD}
Obsoletes:	%{wine}-utils %{wine}-full %{lib_name}-capi %{lib_name}-twain
Obsoletes:	%{lib_name} <= %{EVRD}
Requires:	xmessage
Suggests:	sane-frontends
# wine dlopen's these, so let's add the dependencies ourself
Requires:	libfreetype.so.6%{mark64} libasound.so.2%{mark64}
Requires:	libXrender.so.1%{mark64}
%if %mdkversion >= 201200
Requires:	libpng15.so.15%{mark64}
%else
Requires:	libpng12.so.0%{mark64}
%endif
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires(post): desktop-common-data
Requires(postun): desktop-common-data
Requires(preun): rpm-helper
Requires(post):	rpm-helper
Conflicts:	%{wine} < 1:0.9-3mdk
%ifarch %{ix86}
Conflicts:	wine64
%else
Conflicts:	wine
%endif

%description
%desc

%ifarch x86_64
%description -n	%{wine}
%desc

This package contains the Win64 version of Wine. You need the wine32
package from the 32-bit repository to be able to run 32-bit applications.
%endif

%ifarch %ix86
%package -n	wine32
Summary:	32-bit support for Wine
Group:		Emulators
# This is not an EVR-specific requirement, as otherwise on x86_64 urpmi could
# resolve the dependency to wine64 even on upgrades, and therefore replace
# wine+wine32 installation with a wine32+wine64 installation. - Anssi
Requires:	wine-bin
Conflicts:	wine < 1:1.2-0.rc7.1
Conflicts:	wine64 < 1:1.2-0.rc7.1
# (Anssi) If wine-gecko is not installed, wine pops up a dialog on first
# start proposing to download wine-gecko from sourceforge, while recommending
# to use distribution packages instead. Therefore suggest wine-gecko here:
Suggests:	wine-gecko

%description -n	wine32
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

This package contains the files needed to support 32-bit Windows
programs.
%endif

%package -n	%{wine}-devel
Summary:	Static libraries and headers for %{name}
Group:		Development/C
Requires:	%{wine} = %{EVRD}
%rename		%{lib_name_devel}
Provides:	%{lib_name_orig}-devel = %{EVRD}
Obsoletes:	%{mklibname -d wine 1} < %{EVRD}
%ifarch %{ix86}
Conflicts:	wine64-devel
%else
Conflicts:	wine-devel
%endif

%description -n	%{wine}-devel
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

%{wine}-devel contains the libraries and header files needed to
develop programs which make use of wine.

Wine is often updated.

%prep
%setup -q -n %{oname}-%{o_ver}
%patch1 -p0 -b .chinese
%patch108 -p1 -b .conf
sed -i 's,@MDKVERSION@,%{mdkversion},' dlls/ntdll/server.c

%build
%ifarch %ix86
# (Anssi 04/2008) bug #39604
# Some protection systems complain "debugger detected" with our
# -fomit-frame-pointer flag, so disable it.
export CFLAGS="%{optflags} -fno-omit-frame-pointer"
%endif

# (Anssi 04/2008)
# If icotool is present, it is used to rebuild icon files. It is in contrib
# so we do not do that; this is here to ensure that installed icoutils does
# not change build behaviour.
export ICOTOOL=false

autoreconf
%configure2_5x	--with-x \
		--with-pulse \
		--without-nas \
%ifarch x86_64
		--enable-win64
%endif

%make depend
%make

%install
rm -rf %{buildroot}
%makeinstall_std LDCONFIG=/bin/true 

# Danny: dirty:
install -m755 tools/fnt2bdf -D %{buildroot}%{_bindir}/fnt2bdf

# Allow users to launch Windows programs by just clicking on the .exe file...
install -m755 %{SOURCE2} -D %{buildroot}%{_initrddir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
cat > %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/mandriva-%{name}.menu <<EOF
<!DOCTYPE Menu PUBLIC "-//freedesktop//DTD Menu 1.0//EN"
"http://www.freedesktop.org/standards/menu-spec/menu-1.0.dtd">
<Menu>
    <Name>Applications</Name>
    <Menu>
        <Name>Tools</Name>
        <Menu>
            <Name>Emulators</Name>
            <Menu>
                <Name>Wine</Name>
                <Directory>mandriva-%{name}.directory</Directory>
                <Include>
                    <Category>X-MandrivaLinux-MoreApplications-Emulators-Wine</Category>
                </Include>
            </Menu>
        </Menu>
    </Menu>
</Menu>
EOF

mkdir -p %{buildroot}%{_datadir}/desktop-directories
cat > %{buildroot}%{_datadir}/desktop-directories/mandriva-%{name}.directory <<EOF
[Desktop Entry]
Name=Wine
Icon=%{name}
Type=Directory
EOF

mkdir -p %{buildroot}%{_datadir}/applications/
for i in	winecfg:Configurator \
		notepad:Notepad \
		winefile:File\ Manager \
		regedit:Registry\ Editor \
		winemine:Minesweeper \
		wineboot:Reboot \
		"wineconsole cmd":Command\ Line \
		"wine uninstaller:Wine Software Uninstaller";
do cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-`echo $i|cut -d: -f1`.desktop << EOF
[Desktop Entry]
Name=`echo $i|cut -d: -f2`
Comment=`echo $i|cut -d: -f2`
Exec=`echo $i|cut -d: -f1`
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Emulators-Wine;
EOF
done

# Categories=Emulator does nothing and is added as a workaround to kde #27700
desktop-file-install	--vendor="" \
			--add-mime-type=application/x-zip-compressed \
			--remove-mime-type=application/x-zip-compressed \
			--add-category=Emulator \
			--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/wine.desktop

%ifarch x86_64
# fix the binary name
sed -i 's,Exec=wine ,Exec=wine64 ,' %{buildroot}%{_datadir}/applications/wine.desktop
%endif

install -d %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}

# winecfg icon
convert dlls/user32/resources/oic_winlogo.ico[8] %{buildroot}%{_miconsdir}/%{name}.png
convert dlls/user32/resources/oic_winlogo.ico[7] %{buildroot}%{_iconsdir}/%{name}.png
convert dlls/user32/resources/oic_winlogo.ico[6] %{buildroot}%{_liconsdir}/%{name}.png

# notepad icon
convert programs/notepad/notepad.ico[2] %{buildroot}%{_miconsdir}/notepad.png
convert programs/notepad/notepad.ico[7] %{buildroot}%{_iconsdir}/notepad.png
convert programs/notepad/notepad.ico[8] %{buildroot}%{_liconsdir}/notepad.png
# winefile icon
convert programs/winefile/winefile.ico[2] %{buildroot}%{_miconsdir}/winefile.png
convert programs/winefile/winefile.ico[8] %{buildroot}%{_iconsdir}/winefile.png
convert programs/winefile/winefile.ico[7] %{buildroot}%{_liconsdir}/winefile.png
# regedit icon
convert programs/regedit/regedit.ico[2] %{buildroot}%{_miconsdir}/regedit.png
convert programs/regedit/regedit.ico[8] %{buildroot}%{_iconsdir}/regedit.png
convert programs/regedit/regedit.ico[7] %{buildroot}%{_liconsdir}/regedit.png
# winemine icon
convert programs/winemine/winemine.ico[2] %{buildroot}%{_miconsdir}/winemine.png
convert programs/winemine/winemine.ico[8] %{buildroot}%{_iconsdir}/winemine.png
convert programs/winemine/winemine.ico[7] %{buildroot}%{_liconsdir}/winemine.png

# wine uninstaller icon:
convert programs/msiexec/msiexec.ico[2] %{buildroot}%{_miconsdir}/msiexec.png
convert programs/msiexec/msiexec.ico[8] %{buildroot}%{_iconsdir}/msiexec.png
convert programs/msiexec/msiexec.ico[7] %{buildroot}%{_liconsdir}/msiexec.png

# change the icons in the respective .desktop files, in order:
sed -i 's,Icon=%{name},Icon=notepad,' %{buildroot}%{_datadir}/applications/mandriva-%{name}-notepad.desktop
sed -i 's,Icon=%{name},Icon=winefile,' %{buildroot}%{_datadir}/applications/mandriva-%{name}-winefile.desktop
sed -i 's,Icon=%{name},Icon=regedit,' %{buildroot}%{_datadir}/applications/mandriva-%{name}-regedit.desktop
sed -i 's,Icon=%{name},Icon=winemine,' %{buildroot}%{_datadir}/applications/mandriva-%{name}-winemine.desktop
sed -i 's,Icon=%{name},Icon=msiexec,' "%{buildroot}%{_datadir}/applications/mandriva-wine-stable-wine uninstaller.desktop"

%ifarch x86_64
chrpath -d %{buildroot}%{_bindir}/{wine64,wineserver,wmc,wrc} %{buildroot}%{_libdir}/%{oname}/*.so
%else
chrpath -d %{buildroot}%{_bindir}/{wine,wineserver,wmc,wrc} %{buildroot}%{_libdir}/%{oname}/*.so
%endif

%ifarch x86_64
cat > README.install.urpmi <<EOF
This is the Win64 version of Wine. This version can only be used to run
64-bit Windows applications as is. For running 32-bit Windows applications,
you need to also install the 'wine32' package from the 32-bit repository.
EOF
%endif

%preun -n %{wine}
%_preun_service %{name}

%post -n %{wine}
%_post_service %{name}

%files -n %{wine}
%doc ANNOUNCE AUTHORS README
%ifarch x86_64
%doc README.install.urpmi
%{_bindir}/wine64
%{_bindir}/wine64-preloader
%endif
%{_initrddir}/%{name}
%{_bindir}/winecfg
%{_bindir}/wineconsole*
%{_bindir}/wineserver
%{_bindir}/wineboot
%{_bindir}/function_grep.pl
#%{_bindir}/wineprefixcreate
%{_bindir}/msiexec
%{_bindir}/notepad
%{_bindir}/regedit
%{_bindir}/winemine
%{_bindir}/winepath
%{_bindir}/regsvr32
%{_bindir}/winefile
%{_mandir}/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%dir %{_datadir}/%{oname}
%{_datadir}/%{oname}/generic.ppd
%{_datadir}/%{oname}/%{oname}.inf
%{_datadir}/%{oname}/l_intl.nls
%{_datadir}/applications/*.desktop
%{_sysconfdir}/xdg/menus/applications-merged/mandriva-%{name}.menu
%{_datadir}/desktop-directories/mandriva-%{name}.directory
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/fonts/*
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png

%ifarch %{ix86}
%files -n wine32
%{_bindir}/wine
%{_bindir}/wine-preloader
%endif

%{_libdir}/libwine*.so.%{lib_major}*
%dir %{_libdir}/%{oname}
%{_libdir}/%{oname}/*.cpl.so
%{_libdir}/%{oname}/*.drv.so
%{_libdir}/%{oname}/*.dll.so
%{_libdir}/%{oname}/*.exe.so
%{_libdir}/%{oname}/*.acm.so
%{_libdir}/%{oname}/*.ocx.so
%ifarch %{ix86}
%{_libdir}/%{oname}/*.vxd.so
%{_libdir}/%{oname}/*16.so
%endif
%{_libdir}/%{oname}/*.tlb.so
%{_libdir}/%{oname}/*.ds.so
%{_libdir}/%{oname}/*.sys.so
%{_libdir}/%{oname}/fakedlls

%files -n %{wine}-devel
%{_libdir}/%{oname}/*.a
%{_libdir}/libwine*.so
%{_libdir}/%{oname}/*.def
%{_includedir}/*
%{_bindir}/fnt2bdf
%{_bindir}/wmc
%{_bindir}/wrc
%{_bindir}/winebuild
%{_bindir}/winegcc
%{_bindir}/wineg++
%{_bindir}/winecpp
%{_bindir}/widl
%{_bindir}/winedbg
%{_bindir}/winemaker
%{_bindir}/winedump
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineg++.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/pl.UTF-8/man1/wine.1*


%changelog
* Wed Jun 20 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.4.1-1.1mdv2011.0
+ Revision: 806473
- upgrade to 1.4.1

* Fri Apr 20 2012 Zombie Ryushu <ryushu@mandriva.org> 1:1.4-1.1
+ Revision: 792462
- fix oname
- deal with name change
- Fix revision
- Fix name
- Fix name
- Fix name
- Update Stable version to 1.4
- Update Stable version to 1.4
- Update Stable version to 1.4
- Update Stable version to 1.4
- increment and rebuild
- fix prelink condition

* Sun Jun 19 2011 Zombie Ryushu <ryushu@mandriva.org> 1:1.2.3-1
+ Revision: 686079
- fix preun
- imported package wine-stable

