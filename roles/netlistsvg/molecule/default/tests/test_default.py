def test_netlistsvg_installed_in_prefix(host):
    f = host.file("/opt/eda/bin/netlistsvg")
    assert f.exists


def test_netlistsvg_pinned_version(host):
    out = host.run("npm ls -g --prefix /opt/eda netlistsvg")
    assert out.rc == 0
    assert "netlistsvg@1.0.2" in out.stdout


def test_netlistsvg_rendered_svg(host):
    svg = host.file("/opt/eda/src/netlistsvg/verify/and.svg")
    assert svg.exists
    assert "<svg" in svg.content_string
