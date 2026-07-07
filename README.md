# icanalytica.eda — Ansible collection for the open-source EDA toolchain

Installs open-source EDA tools from **pinned, checksum-verified sources**
into `/opt/eda` on **Rocky Linux 9** and **macOS** workstations. One Ansible
role per tool.

**v1.0 toolchain** (synthesis + formal verification + static timing):

| Role | Tool | Pin |
|---|---|---|
| `yosys` | Yosys RTL synthesis (bundled, statically-tied ABC) | 0.66 (release src tarball) |
| `sby` | SymbiYosys formal verification front-end | commit `d3e72d26` |
| `opensta` | OpenSTA gate-level static timing analyzer | commit `bfdd2be0` (v3.1.0) |
| `cudd` | CUDD decision-diagram library (for OpenSTA) | 3.0.0 |
| `netlistsvg` | Netlist SVG schematic renderer (optional) | npm 1.0.2 |

The rest of the old port tree (iverilog, verilator, magic, netgen, xschem,
gtkwave, xyce/trilinos, openvaf, klayout, OpenROAD, volare) lands in
post-1.0 phases, one tagged minor release per tier.

> **Status: transition in progress.** This repo is being converted from a
> MacPorts port tree to this collection. The legacy tree (`aqua/ cad/ python/
> science/ x11/` and [README-macports.md](README-macports.md)) is **frozen for
> reference** — do not edit it — and will be deleted once all roles have
> landed.

## Using the collection

Add to your control repo's `collections/requirements.yml`:

```yaml
- name: git+ssh://git@github.com/icanalytica/eda-tools.git
  type: git
  version: v1.0.0   # pin a tag
```

Then run the shipped playbook (installs the whole v1.0 toolchain via role
meta-dependencies — opensta pulls cudd, sby pulls yosys):

```yaml
ansible-playbook icanalytica.eda.toolchain -l my_hosts
```

or reference roles by FQCN in your own plays:

```yaml
- hosts: workstations
  roles:
    - role: icanalytica.eda.opensta   # pulls in cudd + eda_common
    - role: icanalytica.eda.sby       # pulls in yosys + eda_common
```

Every tool role depends on `icanalytica.eda.eda_common`, which sets up the
`/opt/eda` prefix, PATH/ldconfig integration, and (on RedHat) CRB+EPEL.
Playbook-level knobs: `eda_prefix`, `eda_src_root`, `eda_make_jobs`,
`eda_mirror_base` (flat mirror for the pinned tarballs), `eda_manage_repos`.

Per-role documentation lives in `roles/<name>/README.md`, including the
upstream pin, its rationale, and the role's self-verification.

## Design in one paragraph

Tools build from pinned upstream tarballs (sha256-verified `get_url`, with a
`file://`/mirror override) into the dedicated prefix `/opt/eda` — never into
`/usr` or Homebrew's prefix, so nothing fights the system package manager and
there is no shared-prefix header shadowing (the problem that forced the old
MacPorts tree's "deactivation gates"). Pins are exact — a version bump is
always a deliberate `<tool>_version` + `<tool>_checksum` diff. Dependencies
come from dnf on RedHat and Homebrew on macOS (`vars/redhat.yml` /
`vars/darwin.yml` per role). Builds are idempotent via versioned stamp files.
Every role ends by running the tool it built and failing the play if it
doesn't work — yosys synthesizes a counter through its bundled ABC, sby must
PASS a true assertion *and* FAIL a false one, OpenSTA must load its Tcl
command layer, cudd must evaluate a real BDD. The flow is fully headless — no
X server required.

## Developing

```bash
asdf install          # pinned uv
uv sync               # python deps into .venv
make lint             # ansible-lint
make yamllint
make test-<role>      # molecule test for one role (Docker, Rocky 9)
make build            # ansible-galaxy collection build sanity
```

CI runs lint on every PR. Molecule tests run locally (the yosys/sby
scenarios build real compilers-and-hours workloads; their converge caps
`eda_make_jobs: 4` because Docker Desktop offers many CPUs but little RAM).
