def test_cudd_header_installed(host):
    assert host.file("/opt/eda/include/cudd.h").exists


def test_cudd_shared_library_installed(host):
    assert host.file("/opt/eda/lib/libcudd.so").exists


def test_cudd_known_to_dynamic_linker(host):
    assert host.run("ldconfig -p | grep -q libcudd").rc == 0


def test_cudd_install_stamp(host):
    stamp = host.file("/opt/eda/src/cudd/.installed-3.0.0")
    assert stamp.exists
    assert stamp.content_string.strip() == "3.0.0"
