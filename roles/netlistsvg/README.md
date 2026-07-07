# netlistsvg

Installs [netlistsvg](https://github.com/nturley/netlistsvg) — renders yosys
JSON netlists (`write_json`) as SVG schematics. **Optional / nice-to-have**;
nothing in the toolchain depends on it.

## Pin

npm package `netlistsvg@1.0.2`, installed globally with
`npm --prefix /opt/eda`, so the package lives under
`/opt/eda/lib/node_modules` and the bin link at `/opt/eda/bin/netlistsvg` —
inside the EDA prefix, not the system npm root.

The top-level package is exactly pinned; npm resolves transitive
dependencies per its package.json ranges. The old MacPorts port vendored the
entire flat dependency tree (~70 tarballs) to make the build fully offline —
deliberately not carried forward for an optional visualization tool.

## Verification

The role renders a minimal yosys-JSON AND-gate netlist to SVG and asserts
real SVG output. The play fails otherwise.

## Usage

```sh
yosys -p "read_verilog design.v; prep -top top; write_json design.json"
netlistsvg design.json -o design.svg
```
