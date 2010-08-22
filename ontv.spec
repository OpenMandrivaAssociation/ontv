Name:			ontv
Version:		3.2.0
Release:		%mkrel 1

Summary:	TV listings for the GNOME panel
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		ftp://ftp.gnome.org/pub/GNOME/sources/ontv

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/ontv/3.0/%{name}-%{version}.tar.bz2
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
BuildRequires:	intltool
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

%build
%configure2_5x --disable-schemas-install
%make
										
%install
rm -rf %{buildroot}
%makeinstall_std

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
%{_libdir}/bonobo/servers/*
%{_bindir}/*
%{_libexecdir}/ontv-applet
%{python_sitelib}/%name
%{_datadir}/%{name}
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/applications/ontv.desktop
%{_datadir}/gnome-control-center/keybindings/90-%{name}.xml
%{_iconsdir}/hicolor/*

