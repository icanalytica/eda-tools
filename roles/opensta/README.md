# opensta

Builds [OpenSTA](https://github.com/parallaxsw/OpenSTA), the gate-level static
timing analyzer, from a pinned, sha256-verified commit tarball into
`{{ eda_prefix }}`. Meta-depends on `icanalytica.eda.cudd` and builds with
`-DCUDD_DIR`, enabling CUDD-backed conditional-arc, constant- and
power-propagation handling.

## Pin

| | |
|---|---|
| Commit | `bfdd2be0ee6214115b20cacdc0a071ca3c737fbb` |
| Declared version | 3.1.0 (the `project()` version in CMakeLists.txt at that commit) |
| sha256 | `1e90d957b3f3bfb1ca03ca4a49b2643cf42b3c6e32c11c5051df5df69187561d` |

parallaxsw/OpenSTA publishes **no git tags and no releases**, so a commit pin
is the only honest pin. When updating, bump `opensta_commit`,
`opensta_version` and `opensta_checksum` together.

## Build notes (ported from the MacPorts Portfile)

- **fmt:** toolchains without `std::format` (gcc 11 on Rocky 9, older macOS
  CLT) make OpenSTA fall back to the fmt library. Without a system fmt,
  OpenSTA's CMake clones fmt via FetchContent *mid-build* (network access) and
  installs that private copy into the prefix, squatting on the canonical fmt
  paths. The role installs `fmt-devel` (EPEL) / `fmt` (Homebrew) so the system
  copy is found instead.
- **Tcl readline** is forced OFF (`-DUSE_TCL_READLINE=OFF`) so the build does
  not silently link a tclreadline that happens to be installed without being
  declared. It only matters for interactive `sta` shells.
- **macOS:** OpenSTA's bundled `FindTCL.cmake` hard-codes Homebrew search
  paths with `NO_DEFAULT_PATH`, and Homebrew's `tcl-tk`/`bison`/`flex` are
  keg-only — `vars/darwin.yml` points CMake at the kegs explicitly. A
  Darwin-only patch replaces C++20 `operator<=>` on `std::string` in
  `network/Network.cc` with `.compare()` (identical sign semantics) because
  older macOS SDK libc++ lacks it.
- bison (>= 3.2), flex and swig (Tcl backend) generate parsers and bindings at
  build time.

## Verification

The role runs the installed binary twice and fails the play on mismatch:
`sta -version` must report the pinned version, and a Tcl script run via
`sta -no_init -no_splash -exit` must find the swig-generated commands
(`read_liberty`, `read_verilog`, `report_checks`) registered.

## Variables

See `defaults/main.yml`; the interesting knobs are `opensta_force_rebuild`,
`opensta_cmake_args`, and the collection-wide `eda_prefix` / `eda_src_root` /
`eda_make_jobs` / `eda_mirror_base`.
