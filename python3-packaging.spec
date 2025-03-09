#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	tests		# py.test tests
%bcond_without	setuptools	# build without setuptools (for bootstraping)
%bcond_with	bootstrap	# bootstraping for python-rpm-packaging (rpm-pythonprov)

%if %{with boostrap}
%undefine	with_doc
%undefine	with_tests
%undefine	with_setuptools
%endif

Summary:	Core utilities for Python packages
Summary(pl.UTF-8):	Bazowe funkcje narzędziowe do pakietów Pythona
Name:		python3-packaging
Version:	24.2
Release:	1
License:	Apache v2.0 or BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/packaging/
Source0:	https://pypi.debian.net/packaging/packaging-%{version}.tar.gz
# Source0-md5:	97dbaca91e00d6b9fd86866e8c7897ae
URL:		https://github.com/pypa/packaging
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
%{?with_setuptools:BuildRequires:	python3-setuptools >= 1:61.0.0}
%if %{with tests}
BuildRequires:	python3-pretend
BuildRequires:	python3-pyparsing >= 2.0.2
BuildRequires:	python3-pytest
%endif
%{!?with_bootstrap:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
Requires:	python3-pyparsing >= 2.0.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Core utilities for Python packages.

%description -l pl.UTF-8
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
cat > setup.py <<EOF
from setuptools import setup
setup(version='%{version}')
EOF

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} -m pytest
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.BSD README.rst
%{py3_sitescriptdir}/packaging
%{py3_sitescriptdir}/packaging-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,development,*.html,*.js}
%endif
