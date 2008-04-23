%define name	ontv
%define version	3.0.0
%define release %mkrel 3


Name: %{name}
Summary: TV listings for the GNOME panel
Version: %{version}
Release: %{release}
Source: http://johan.svedberg.com/projects/coding/ontv/download/%{name}-%{version}.tar.gz
Patch0: ontv-3.0.0-assistant.patch
URL: http://johan.svedberg.com/projects/coding/ontv/
License: GPL
Group: Graphical desktop/GNOME
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: GConf2
BuildRequires: perl-XML-Parser
BuildRequires: pygtk2.0-devel
%if %mdkversion>=200810
BuildRequires: gnome-python-devel
%else
BuildRequires: gnome-python
%endif
BuildRequires: gnome-python-extras
BuildRequires: python-notify
BuildRequires: python-vte
BuildRequires: libgnome-window-settings-devel
Requires: GConf2
Requires: gnome-python-applet
Requires: xmltv-grabbers
#Requires: gnome-python-gconf
Requires: gnome-python-gnomevfs
Requires: python-celementtree
Requires: dbus-python
Requires: python-notify
Requires: python-vte

%description
OnTV is a GNOME Applet which uses XMLTV files to monitor current and upcoming
TV programs.

%prep
%setup -q
%patch0 -p1
#fix x86_64 build:
perl -pi -e "s|sysconfig.get_python_lib\(0|sysconfig.get_python_lib\(1|" configure

%build
#schemas install is not needed and produces garbage output while building
%configure2_5x --disable-schemas-install

%make
										
%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %name

%define schemas %name

%post
%post_install_gconf_schemas %{schemas}
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%update_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS FAQ README NEWS THANKS TODO
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/%name
%{_libdir}/bonobo/servers/*
%{py_platsitedir}/%name
%{_datadir}/%name
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/gnome-control-center/keybindings/90-%name.xml
%{_iconsdir}/hicolor/*

