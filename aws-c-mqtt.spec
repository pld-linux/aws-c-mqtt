#
# Conditional build:
%bcond_without	tests		# unit tests
#
Summary:	AWS C MQTT library
Summary(pl.UTF-8):	Biblioteka AWS C MQTT
Name:		aws-c-mqtt
Version:	0.13.1
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/awslabs/aws-c-mqtt/releases
Source0:	https://github.com/awslabs/aws-c-mqtt/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d369035551221d37e1f6552df76554cc
URL:		https://github.com/awslabs/aws-c-mqtt
BuildRequires:	aws-c-common-devel
BuildRequires:	aws-c-http-devel
BuildRequires:	cmake >= 3.9
BuildRequires:	gcc >= 5:3.2
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Core C99 package for AWS SDK for C. Includes cross-platform
primitives, configuration, data structures, and error handling.

%description -l pl.UTF-8
Główny pakiet C99 dla AWS SDK dla języka C. Zawiera wieloplatformowe
podstawy, konfigurację, struktury danych i obsługę błędów.

%package devel
Summary:	Header files for AWS C MQTT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AWS C MQTT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	aws-c-http-devel

%description devel
Header files for AWS C MQTT library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AWS C MQTT.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	%{!?with_tests:-DBUILD_TESTING=OFF}

%{__make}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with tests}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{elasticpubsub,elasticpubsub5,elastishadow,mqtt5canary}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NOTICE README.md
%attr(755,root,root) %{_libdir}/libaws-c-mqtt.so.1.0.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libaws-c-mqtt.so
%{_includedir}/aws/mqtt
%{_libdir}/cmake/aws-c-mqtt
