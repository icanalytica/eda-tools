import re


def test_yosys_binary_installed(host):
    f = host.file("/opt/eda/bin/yosys")
    assert f.exists
    assert f.mode & 0o111


def test_bundled_abc_installed(host):
    f = host.file("/opt/eda/bin/yosys-abc")
    assert f.exists
    assert f.mode & 0o111


def test_yosys_reports_pinned_version(host):
    out = host.run("/opt/eda/bin/yosys -V")
    assert out.rc == 0
    assert "Yosys 0.66" in out.stdout


def test_yosys_synthesizes_with_abc(host):
    host.run(
        "printf 'module t(input a, input b, output y);"
        "assign y = a & b; endmodule' > /tmp/t.v"
    )
    out = host.run(
        '/opt/eda/bin/yosys -p "read_verilog /tmp/t.v; synth -top t; stat"'
    )
    assert out.rc == 0
    # yosys 0.66's stat prints a count table ("1 cells"), not the old
    # "Number of cells" wording.
    assert re.search(r"[1-9][0-9]* cells", out.stdout)


def test_yosys_smtbmc_installed(host):
    # sby drives yosys-smtbmc; it ships with yosys.
    f = host.file("/opt/eda/bin/yosys-smtbmc")
    assert f.exists
