# sby

Installs [SymbiYosys (sby)](https://github.com/YosysHQ/sby), the formal
verification front-end for Yosys (bounded/unbounded model checking,
k-induction, cover, equivalence), from a pinned, sha256-verified commit
tarball into `{{ eda_prefix }}`. Meta-depends on `icanalytica.eda.yosys` —
sby orchestrates `yosys` and `yosys-smtbmc` with SMT solvers such as z3.

## Pin

| | |
|---|---|
| Commit | `d3e72d26e8634bca4ca16f3e4d84331481f06ab6` |
| Assigned version | 20260616 (date-based; upstream has no recent tags) |
| sha256 | `db9ed202a0ee56466c7b819011581e141b4bfb10dc8a915d6c2a95847bfdc547` |

sby has no recent version tags aligned with current yosys, so a main-commit
pin is the only honest pin. It is loosely coupled to yosys (drives it over
PATH), so it works with our yosys 0.66. When updating, bump `sby_commit`,
`sby_version` and `sby_checksum` together.

**The `.gittag` trick (ported from the Portfile):** sby's Makefile derives
its version from `.gittag`, falling back to `git describe` — which fails in
a tarball checkout. The role writes a clean `.gittag` after extraction so no
git is invoked.

sby is pure Python (noarch): no build, just `make install`. The installed
script uses `#!/usr/bin/env python3` (needs Python ≥ 3.8; dnf `python3` on
Rocky, Xcode CLT or Homebrew on macOS). The z3 solver comes from EPEL (dnf)
or Homebrew.

## Verification

The role runs two real formal tasks through the whole stack
(sby → yosys → yosys-smtbmc → z3): a true assertion that must **PASS** and a
false one that must **FAIL**. Requiring the failing verdict catches a broken
solver hookup that silently "proves" everything. The play fails on either
wrong verdict.

## Variables

See `defaults/main.yml`; the interesting knobs are `sby_force_rebuild` and
the collection-wide `eda_prefix` / `eda_src_root` / `eda_mirror_base`.
