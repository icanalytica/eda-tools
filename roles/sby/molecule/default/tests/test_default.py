def test_sby_installed(host):
    f = host.file("/opt/eda/bin/sby")
    assert f.exists
    assert f.mode & 0o111


def test_sby_runs(host):
    out = host.run("/opt/eda/bin/sby --help")
    assert out.rc == 0


def test_z3_solver_present(host):
    assert host.exists("z3")


def test_yosys_dependency_installed(host):
    # sby meta-depends on yosys; a converged host must have both.
    assert host.file("/opt/eda/bin/yosys").exists
    assert host.file("/opt/eda/bin/yosys-smtbmc").exists


def test_formal_flow_end_to_end(host):
    # The converge already ran the in-role pass/fail smoke tasks; their
    # workdirs prove the whole sby -> yosys -> smtbmc -> z3 stack executed.
    assert host.file("/opt/eda/src/sby/verify/smoke_pass/PASS").exists
    assert host.file("/opt/eda/src/sby/verify/smoke_fail/FAIL").exists
