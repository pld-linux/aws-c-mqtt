#
# Conditional build:
%bcond_without	tests		# unit tests
#
Summary:	AWS C MQTT library
Summary(pl.UTF-8):	Biblioteka AWS C MQTT
Name:		aws-c-mqtt
Version:	1.0.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/awslabs/aws-c-mqtt/releases
Source0:	https://github.com/awslabs/aws-c-mqtt/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7402112fd438f1a4a1d7ffdb69b48749
URL:		https://github.com/awslabs/aws-c-mqtt
BuildRequires:	aws-c-common-devel >= 1.0
BuildRequires:	aws-c-http-devel >= 1.0
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
Requires:	aws-c-common-devel >= 1.0
Requires:	aws-c-http-devel >= 1.0

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
	-DCMAKE_PREFIX_PATH=%{_prefix} \
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
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{elastipubsub,elastipubsub5,elastishadow,mqtt5canary}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NOTICE README.md
%{_libdir}/libaws-c-mqtt.so.*.*.*
%ghost %{_libdir}/libaws-c-mqtt.so.1.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libaws-c-mqtt.so
%{_includedir}/aws/mqtt
%{_libdir}/cmake/aws-c-mqtt
