# cudd

Builds [CUDD](https://github.com/cuddorg/cudd) 3.0.0 — the CU Decision Diagram
package (BDDs, ADDs, ZDDs) — from a pinned, sha256-verified tarball into
`{{ eda_prefix }}`. Installed for OpenSTA, whose BDD-based conditional-arc,
constant- and power-propagation handling requires it (`icanalytica.eda.opensta`
lists this role as a meta-dependency).

## Pin

| | |
|---|---|
| Version | 3.0.0 (last upstream release) |
| sha256 | `ce2c41c000f4374868ee4d713283a35d3d975a96f1c6f3bcfbee96e79eeb4560` |

**Why the odd source URL:** cuddorg/cudd carries two tags that collide on the
short ref (`3.0.0` and `cudd-3.0.0`), so GitHub's short archive URL
(`archive/3.0.0.tar.gz`) returns an "ambiguous ref" error page instead of a
tarball, and the release asset unpacks into a doubled `cudd-cudd-3.0.0`
directory. The role fetches the fully-qualified `archive/refs/tags/3.0.0.tar.gz`,
which extracts cleanly to `cudd-3.0.0` and ships a committed `./configure`.

Version bumps must change `cudd_version` and `cudd_checksum` together.

## Build

`./configure --enable-shared --enable-dddmp --enable-obj` — the shared library
plus the dddmp and C++ object interfaces, so the package is useful to a range
of EDA consumers. OpenSTA itself only needs the C API (`cudd.h`).

## Verification

The role compiles and runs a real BDD program against the installed library:
the DAG for `x AND y` must have exactly 3 nodes and the manager must report
zero leaked references. The play fails otherwise.

## Variables

See `defaults/main.yml`; the interesting knobs are `cudd_force_rebuild` and
the collection-wide `eda_prefix` / `eda_src_root` / `eda_make_jobs` /
`eda_mirror_base`.
