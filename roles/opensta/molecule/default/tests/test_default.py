def test_sta_binary_installed(host):
    f = host.file("/opt/eda/bin/sta")
    assert f.exists
    assert f.mode & 0o111


def test_sta_reports_pinned_version(host):
    out = host.run("/opt/eda/bin/sta -version")
    assert out.rc == 0
    assert "3.1.0" in out.stdout


def test_sta_tcl_commands_registered(host):
    script = (
        'if {[info commands report_checks] eq ""} {exit 1}; '
        'puts "sta-ok"; exit 0'
    )
    host.run("printf '%s' '" + script + "' > /tmp/sta_smoke.tcl")
    out = host.run("/opt/eda/bin/sta -no_init -no_splash -exit /tmp/sta_smoke.tcl")
    assert out.rc == 0
    assert "sta-ok" in out.stdout


def test_cudd_dependency_installed(host):
    # opensta meta-depends on cudd; a converged host must have both.
    assert host.file("/opt/eda/include/cudd.h").exists
