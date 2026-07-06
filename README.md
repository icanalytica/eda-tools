# icanalytica.eda — Ansible collection for the open-source EDA toolchain

Installs the open-source sky130-capable EDA toolchain (yosys, OpenSTA,
OpenROAD, magic, netgen, xschem, xyce, openvaf, klayout, ...) from **pinned,
checksum-verified sources** into `/opt/eda` on **Rocky Linux 9** and
**macOS** workstations. One Ansible role per tool.

> **Status: transition in progress.** This repo is being converted from a
> MacPorts port tree to this collection. The legacy tree (`aqua/ cad/ python/
> science/ x11/` and [README-macports.md](README-macports.md)) is **frozen for
> reference** — do not edit it — and will be deleted once all roles have
> landed. Roles arrive in phases; see the issues/PRs.

## Using the collection

Add to your control repo's `collections/requirements.yml`:

```yaml
- name: git+ssh://git@github.com/icanalytica/eda-tools.git
  type: git
  version: v1.0.0   # pin a tag
```

Then reference roles by FQCN:

```yaml
- hosts: workstations
  roles:
    - role: icanalytica.eda.yosys
    - role: icanalytica.eda.magic
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
MacPorts tree's "deactivation gates"). Dependencies come from dnf on RedHat
and Homebrew on macOS (`vars/redhat.yml` / `vars/darwin.yml` per role). Builds
are idempotent via versioned stamp files. Every role ends by running the tool
it built and failing the play if it doesn't work. The flow is fully headless —
no XQuartz/X server required (magic `-dnull -noconsole`, netgen `-batch`,
xschem `--no_x`); klayout provides the native layout GUI.

## Developing

```bash
asdf install          # pinned uv
uv sync               # python deps into .venv
make lint             # ansible-lint
make yamllint
make test-eda_common  # molecule test for one role (Docker, Rocky 9)
make build            # ansible-galaxy collection build sanity
```

CI runs lint on every PR, molecule for cheap roles (path-filtered), macOS
converges on GitHub macos runners for macOS-enabled roles, and multi-hour
builds (OpenROAD, klayout, xyce) on a weekly `heavy-builds` workflow.
