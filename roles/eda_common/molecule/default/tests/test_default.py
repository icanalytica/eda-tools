def test_prefix_directories(host):
    for path in ["/opt/eda", "/opt/eda/bin", "/opt/eda/vendor", "/opt/eda/src"]:
        d = host.file(path)
        assert d.is_directory
        assert d.mode == 0o755


def test_profile_adds_path(host):
    f = host.file("/etc/profile.d/eda.sh")
    assert f.exists
    assert "/opt/eda/bin" in f.content_string
    out = host.run("bash -lc 'echo $PATH'")
    assert "/opt/eda/bin" in out.stdout


def test_dynamic_linker_config(host):
    f = host.file("/etc/ld.so.conf.d/eda.conf")
    assert f.exists
    assert "/opt/eda/lib" in f.content_string


def test_base_toolchain_present(host):
    for tool in ["gcc", "g++", "make", "autoconf", "libtool", "git", "patch"]:
        assert host.exists(tool)


def test_repos_enabled(host):
    crb = host.run("dnf repolist --enabled")
    assert "crb" in crb.stdout.lower()
    assert "epel" in crb.stdout.lower()
