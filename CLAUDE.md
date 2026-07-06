# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A local **MacPorts port tree** ("macportseda") of open-source EDA/IC-design tools for macOS 13 and 15. There is no application code: every unit of work is a `Portfile` (Tcl) under `<category>/<portname>/`, optionally with a `files/` directory of patches and helper scripts. Categories follow MacPorts conventions: `cad/`, `science/`, `x11/`, `python/`, `aqua/`.

The tree is registered in `/opt/local/etc/macports/sources.conf` with a `file://` line **above** the rsync line, so these ports shadow stock MacPorts ports of the same name.

`README.md` is the authoritative documentation — it has a per-port notes section for nearly every port (build quirks, verification steps, upstream pinning rationale). Keep it in sync when changing ports.

## Common commands

```bash
# REQUIRED after any Portfile change — MacPorts reads PortIndex, not Portfiles.
# Run from the repo root:
portindex

port lint <port>                  # style/dependency check
sudo port install <port>
sudo port -v install <port>       # verbose build (see actual compiler errors)
port notes <port>                 # post-install caveats a port declares
port test netlistsvg              # a few ports define a test phase

# Version bump workflow: edit version/commit in the Portfile, then
sudo port clean <port>
port -v checksum <port>           # fails but prints correct rmd160/sha256/size
# ...paste the reported values into the Portfile's checksums block, portindex, rebuild.

# Refresh the (gitignored) offline distfiles archive after adding/bumping a port:
sudo port mirror <port>
rsync -a /opt/local/var/macports/distfiles/<port> distfiles/
```

`port lint` reporting `Unknown dependency: <local port>` just means `portindex` hasn't run since that port was added.

## Architecture of the tree

- **`cad/eda-icall`** is a metaport that installs the whole sky130 toolchain in one shot. Its `notes` block summarizes the manual prerequisites MacPorts can't automate.

- **Private-prefix strategy for conflicting pins**: ports named `eda-*` (`eda-or-tools`, `eda-lemon`, `eda-fmt`, `eda-spdlog`), plus `openroad-ll`, `trilinos-charon`, and `charon`, install into private prefixes under `${prefix}/libexec/` instead of `${prefix}`. This lets version-pinned dependencies (e.g. fmt 12 for OpenROAD vs MacPorts' fmt-10-bound spdlog) coexist with the stock MacPorts copies.

- **Everything is pinned; builds never touch the network.** Ports pin exact upstream commits/tags, and language-ecosystem deps are checksummed distfiles too: `openvaf` pins all 147 crates inline, `netlistsvg` pins all 70 npm tarballs (no cargo/npm resolution at build time). A gitignored `distfiles/` archive (also on the GitHub release `distfiles-2026-07`) holds every tarball because upstream URLs rot; Portfile checksums authenticate it.

- **Vendored stock snapshots**: `gtkwave`, `xcircuit`, `iverilog`, `magic`, `verilator` are copies of the stock MacPorts ports, frozen at known-good revisions (two carry local fixes: xcircuit's Xcode 16 `-Wno-error` flags, magic's 8.3.660 bump + gsed fix). This is deliberate pinning, not a fork to maintain — refresh by re-copying from the rsync tree and re-running `portindex`. `ngspice` and `openEMS` are deliberately left on stock MacPorts.

- **Name collisions with stock ports are avoided by renaming**: `netgen-lvs` (stock `netgen` is a FEM mesher), `skim-app` (stock `skim` is a fuzzy finder).

- **Build-time deactivation gates** — some builds fail unless an unrelated active port is deactivated first, because its `/opt/local/include` headers shadow vendored/private copies. MacPorts cannot express this; it's manual:
  - `kicad`: deactivate `boost`
  - `charon` / `trilinos-charon`: deactivate `trilinos16` (its stub `mpi.h`)
  - `openroad` / `openroad-ll`: deactivate `boost spdlog protobuf3-cpp OpenSTA`

  Reactivate after the build. Beware: MacPorts rev-upgrade can re-activate ports on its own mid-batch.

- **Dependency variants are load-bearing** (macOS 15 especially): X11 GUI ports need `tk +x11`, gtkwave needs `gtk2 +quartz`, lepton-eda needs `libepoxy +x11` and `glib2 +x11`, and `cairo`/`pango` must keep **both** `+quartz+x11` — an `--enforce-variants` sweep that strips one backend silently breaks every already-built port on the other. Details in README's macOS 15 and lepton-eda sections.

- **Out-of-tree companions** (Python venvs, not ports): LibreLane (`~/.venvs/librelane`, drives the RTL-to-GDS flow, needs `yosys +pyosys` and the `openroad-ll` pin) and cocotb (`~/.venvs/cocotb`). See README's LibreLane and cocotb sections before touching yosys, magic, openroad-ll, netgen-lvs, or klayout versions — those pins match LibreLane's.

## Portfile conventions

- Every Portfile starts with the standard MacPorts modeline comment and uses `maintainers {icanalytica.com:degnan @bpdegnan} openmaintainer`.
- Comments explain *why* (upstream has no tags, header X shadows Y, SDK Z lacks a symbol) — keep that habit; the build gotchas are the whole value of this tree.
- Nontrivial fixes go in `files/` as patchfiles; runtime caveats users must know go in a `notes` block (surfaced by `port notes`).
- `.gitignore` already covers port-phase droppings (`Checksumming`, `Configuring`, `PortIndex`, `work/`, etc.) — don't commit them.
