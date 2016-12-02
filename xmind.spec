%define __jar_repack 0

%define upstream_version 8

Name:           xmind
Version:        %{upstream_version}
Release:        1%{?dist}
Summary:        Brainstorming and Mind Mapping
Group:          Applications/Productivity
License:        EPL or LGPLv3
URL:            http://www.xmind.net
Source0:        http://www.xmind.net/xmind/downloads/%{name}-%{upstream_version}-linux.zip
Source1:        xmind.sh
Source2:        xmind.png
Source3:        xmind.xml
Source4:        xmind.desktop
ExcludeArch:    ppc ppc64 arm s390x sparc
BuildRequires:  unzip
BuildRequires:  desktop-file-utils
BuildRequires:  chrpath
BuildRequires:  java-devel
AutoReqProv:    no
Requires:       java
Requires:       gtk3

%description
XMind is an open source project that contributes to building a cutting-edge brainstorming/mind-mapping facility, focused on both usability and extendability. It helps people in capturing ideas into visually self-organized charts and sharing them for collaboration and communication. Currently supporting mind maps, fishbone diagrams, tree diagrams, org-charts, logic charts, and even spreadsheets. Often used for knowledge management, meeting minutes, task management, and GTD. 


%prep
%setup -q -c

%ifarch x86_64
    rm -r XMind_i386
    mv XMind{_amd64,}
%else
    rm -r XMind_amd64
    mv XMind{_i386,}
%endif


%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_bindir}

# delete rpath from libcairo-swt.so
# chrpath --delete XMind_Linux/libcairo-swt.so

# hack to get rid of the splash screen
# https://xmind.desk.com/customer/portal/questions/5667621-xmind-startup-bug-in-ubuntu-13-4

# mkdir -p icons
# touch icons/progress.gif
# jar -uf Commons/plugins/org.xmind.cathy_%{version}.%{version_suffix}.jar icons/progress.gif
# chmod 0644 Commons/plugins/org.xmind.cathy_%{version}.%{version_suffix}.jar
# rm -rf icons

sed -i -e 's@^../workspace@./workspace@g' -e 's@^../plugins@./plugins@g' ./XMind/XMind.ini
cp -af ./plugins ./XMind/{XMind,configuration,XMind.ini} %{buildroot}%{_datadir}/%{name}/
cp -af %{SOURCE1} %{buildroot}%{_bindir}/%{name}
cp -af %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/%{name}.png
cp -af %{SOURCE3} %{buildroot}%{_datadir}/mime/packages/%{name}.xml

bash


cp -af %{SOURCE4} %{buildroot}/xmind.desktop
desktop-file-install                          \
--add-category="Office"                       \
--delete-original                             \
--dir=%{buildroot}%{_datadir}/applications    \
%{buildroot}/xmind.desktop


%files
%defattr(-,root,root)
%doc *.txt *.html
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}


%changelog
* Fri Sep 16 2016 Tomas Tomecek <ttomecek@redhat.com> - 3.6.51-1
- 3.6.51 update

* Tue Mar 08 2016 Tomas Tomecek <ttomecek@redhat.com> - 3.6.1-1
- 3.6.1 update

* Fri Aug 15 2014 Tomas Hozza <thozza@redhat.com> - 3.4.1-1
- Update to 3.4.1

* Tue Jan 14 2014 Tomas Tomecek <ttomecek@redhat.com> - 3.4.0-1
- rebase to 3.4.0


