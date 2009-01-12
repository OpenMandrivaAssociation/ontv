Name:			ontv
Version:		3.0.0
Release:		%mkrel 6

Summary:	TV listings for the GNOME panel
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		ftp://ftp.gnome.org/pub/GNOME/sources/ontv

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/ontv/3.0/%{name}-%{version}.tar.gz
Patch0:		ontv-3.0.0-assistant.patch

BuildRequires:	GConf2
BuildRequires:	perl-XML-Parser
BuildRequires:	pygtk2.0-devel
%if %mdkversion>=200810
BuildRequires:	gnome-python-devel
%else
BuildRequires:	gnome-python
%endif
BuildRequires:	gnome-python-extras
BuildRequires:	python-notify
BuildRequires:	python-vte
BuildRequires:	libgnome-window-settings-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

Requires:	xmltv
Requires:	xmltv-grabbers
Requires:	GConf2
Requires:	gnome-python-applet
Requires:	gnome-python-gnomevfs
Requires:	dbus-python
Requires:	python-notify
Requires:	python-vte

%description
OnTV is a GNOME Applet which uses XMLTV files to monitor current and upcoming
TV programs.

%prep
%setup -q
%patch0 -p1
#fix x86_64 build:
perl -pi -e "s|sysconfig.get_python_lib\(0|sysconfig.get_python_lib\(1|" configure
%if %mdkversion >= 200910
perl -pi -e "s|python2.5|python2.6|" scripts/ontv.in
%endif

%build
#schemas install is not needed and produces garbage output while building
%configure2_5x --disable-schemas-install

%make
										
%install
rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{py_platsitedir}/%{name}/keybinder/_keybinder.a

%find_lang %{name}

%define schemas %{name}

%post
%post_install_gconf_schemas %{schemas}
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%update_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS FAQ README NEWS THANKS TODO
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/%{name}
%{_libdir}/bonobo/servers/*
%{py_platsitedir}/%{name}
%{_datadir}/%{name}
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/gnome-control-center/keybindings/90-%{name}.xml
%{_iconsdir}/hicolor/*

