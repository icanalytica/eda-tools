sync:
	uv sync

lint:
	ANSIBLE_NOCOWS=1 uv run ansible-lint -p

lint-fix:
	ANSIBLE_NOCOWS=1 uv run ansible-lint --fix -p

yamllint:
	uv run yamllint .

build:
	uv run ansible-galaxy collection build --force

# Run one role's molecule scenario, e.g. `make test-eda_common`
test-%:
	uv run --project "$(CURDIR)" -- bash -c 'cd roles/$* && molecule test'
