### RPM external xrootd 4.12.3
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define tag b122d662f80a46a570876afd32cdaa9f4370dc1d
%define branch stable-4.12.x
%define github_user xrootd
Source: git+https://github.com/%github_user/xrootd.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake
Requires: zlib
Requires: openssl
Requires: python python3
Requires: libxml2

%prep
%setup -n %n-%{realversion}

# need to fix these from xrootd git
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/cleanup.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/loadRTDataToMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonCollector.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/prepareMySQLStats.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonCreateMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonLoadMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonPrepareStats.pl
%build
# By default xrootd has perl, fuse, krb5, readline, and crypto enabled. 
# libfuse and libperl are not produced by CMSDIST.

CMAKE_ARGS="-DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DOPENSSL_ROOT_DIR:PATH=${OPENSSL_ROOT} \
  -DZLIB_ROOT:PATH=${ZLIB_ROOT} \
  -DENABLE_PYTHON=FALSE \
  -DENABLE_FUSE=FALSE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=FALSE \
  -DENABLE_CRYPTO=TRUE \
  -DCMAKE_SKIP_RPATH=TRUE \
  -DENABLE_PYTHON=TRUE"

#Configure and build with python2
rm -rf build; mkdir build; cd build
cmake .. $CMAKE_ARGS -DXRD_PYTHON_REQ_VERSION=2 -DCMAKE_PREFIX_PATH="${PYTHON_ROOT};${LIBXML2_ROOT}"
make %makeprocesses VERBOSE=1
make install
%{relocatePy2SitePackages}

#Configure and build with python3
cd ..; rm -rf build3; mkdir build3; cd build3
cmake .. $CMAKE_ARGS -DXRD_PYTHON_REQ_VERSION=3 -DCMAKE_PREFIX_PATH="${PYTHON3_ROOT};${LIBXML2_ROOT}"
cd bindings
make %makeprocesses VERBOSE=1
make install
%{relocatePy3SitePackages}

%install
%define strip_files %i/lib
%define keep_archives true

