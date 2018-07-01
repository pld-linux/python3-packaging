#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	tests	# py.test tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Core utilities for Python packages
Summary(pl.UTF-8):	Bazowe funkcje narzędziowe do pakietów Pythona
Name:		python-packaging
Version:	16.8
Release:	3
License:	Apache v2.0 or BSD
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/packaging
Source0:	https://files.pythonhosted.org/packages/source/p/packaging/packaging-%{version}.tar.gz
# Source0-md5:	53895cdca04ecff80b54128e475b5d3b
URL:		https://github.com/pypa/packaging
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pretend
BuildRequires:	python-pyparsing
BuildRequires:	python-pytest
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pretend
BuildRequires:	python3-pyparsing
BuildRequires:	python3-pytest
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Core utilities for Python packages.

%description -l pl.UTF-8
Bazowe funkcje narzędziowe do pakietów Pythona.

%package -n python3-packaging
Summary:	Core utilities for Python packages
Summary(pl.UTF-8):	Bazowe funkcje narzędziowe do pakietów Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-packaging
Core utilities for Python packages.

%description -n python3-packaging -l pl.UTF-8
Bazowe funkcje narzędziowe do pakietów Pythona.

%package apidocs
Summary:	API documentation for Python packaging library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Pythona packaging
Group:		Documentation

%description apidocs
API documentation for Python packaging library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Pythona packaging.

%prep
%setup -q -n packaging-%{version}

%build
%if %{with python2}
%py_build

%{?with_tests:%{__python} -m pytest}
%endif

%if %{with python3}
%py3_build

%{?with_tests:%{__python3} -m pytest}
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE LICENSE.BSD README.rst
%{py_sitescriptdir}/packaging
%{py_sitescriptdir}/packaging-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-packaging
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE LICENSE.BSD README.rst
%{py3_sitescriptdir}/packaging
%{py3_sitescriptdir}/packaging-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,development,*.html,*.js}
%endif
