# yosys

Builds [Yosys](https://yosyshq.net/yosys/) 0.66 — the open synthesis suite
(Verilog RTL synthesis) — from the official **release source tarball** into
`{{ eda_prefix }}`.

## Pin

| | |
|---|---|
| Version | 0.66 |
| Tarball | `yosys-src.tar.gz` from the v0.66 GitHub release |
| sha256 | `ba567ea7fbb1287e996aef8f20fe902f6fd408593aa50cfaea8ae0c9015ab872` |

**Why the src tarball (not the git tag archive):** it bundles ABC — built
from the bundled tree and tied to this exact yosys version, with no network
fetch or git invocation during the build — and it carries `.gitcommit`, so
`yosys -V` reports the right version without a git checkout. The bundled ABC
is a hard requirement here (the whole point of this pin, per the original
MacPorts port). The tarball is flat (no top-level directory); the role
creates the source dir before extracting.

Version bumps must change `yosys_version` and `yosys_checksum` together.

## Build

Plain `make` with `PREFIX={{ eda_prefix }}` baked in (the prefix lands in
the binary's data path, so build and install must agree) and `CONFIG=gcc`
(Linux) / `CONFIG=clang` (macOS). `ENABLE_PYOSYS` stays off — the Python
bindings only matter for OpenLane/LibreLane native mode, which is out of
scope.

Installs `yosys`, `yosys-abc`, `yosys-smtbmc` (the SMT backend driver that
`sby` orchestrates), `yosys-config`, and the share tree.

## Verification

`yosys -V` must report the pinned version, and the role synthesizes a real
8-bit counter with `synth` — which runs the bundled ABC — and asserts the
flow produced cells. The play fails otherwise.

## Variables

See `defaults/main.yml`; the interesting knobs are `yosys_force_rebuild`,
`yosys_make_args`, and the collection-wide `eda_prefix` / `eda_src_root` /
`eda_make_jobs` / `eda_mirror_base`.
