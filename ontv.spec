%define name	ontv
%define version	2.8.0
%define release %mkrel 1

Name: %{name}
Summary: TV listings for the GNOME panel
Version: %{version}
Release: %{release}
Source: http://johan.svedberg.com/projects/coding/ontv/download/%{name}-%{version}.tar.bz2
Source10: ontv.pot
Source11: fr.po
Patch0: ontv-2.6.0-assistant.patch
URL: http://johan.svedberg.com/projects/coding/ontv/
License: GPL
Group: Graphical desktop/GNOME
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: GConf2
BuildRequires: perl-XML-Parser
BuildRequires: pygtk2.0-devel
BuildRequires: gnome-python
BuildRequires: gnome-python-extras
BuildRequires: python-notify
BuildRequires: python-vte
#>= 0.16.0-2mdv2007.1
Requires: GConf2 gnome-python-applet xmltv
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
#%patch0 -p1
#avoids creation of %{_iconsdir}/hicolor/icon-theme.cache
#this file conflicts with hicolor-icon-theme
perl -pi -e "s|gtk_update_icon_cache = |gtk_update_icon_cache = #|" data/images/Makefile.in
cp -f %{SOURCE10} %{SOURCE11} po/
#fix x86_64 build:
perl -pi -e "s|sysconfig.get_python_lib\(0|sysconfig.get_python_lib\(1|" configure

%build
#schemas install is not needed and produces garbage output while building
%configure2_5x --disable-schemas-install

%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%find_lang %name

%define schemas %name

%post
%post_install_gconf_schemas %{schemas}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS FAQ README NEWS THANKS TODO
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/%name
%{_libdir}/bonobo/servers/*
%{_libdir}/python*/site-packages/%name
%{_datadir}/%name
%{_datadir}/gnome-2.0/ui/*.xml
%{_iconsdir}/hicolor/*
