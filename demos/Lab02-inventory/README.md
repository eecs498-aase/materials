# Inventory example

Run `./reset` to create a disposable exercise copy under the containing repository's
`demo-scratch/Lab02-inventory/`. Run commands from the printed directory. Use
`./reset --stage solution --dest /tmp/inventory-solution` for the worked solution,
or `--stage starter` for ordinary application code without the supplied AI example.
Reset refuses to overwrite a directory. The pristine source is never the workspace.

```sh
bin/inventory smoke
bin/inventory test
bin/inventory start scripted
```

The exercise intentionally fails the feedback tests until the missing observation
is delivered. The scripted mode is a code demonstration, not an LLM rehearsal.
It demonstrates an unsuccessful five-marker reservation, clarification, and a
successful three-marker reservation. Use a fresh reset for each demonstration.

For live use, configure MODEL_BASE_URL (ending /v1), MODEL_NAME, and optionally
MODEL_API_KEY and MODEL_TIMEOUT in the environment. Then:

```sh
bin/inventory start categorize
bin/inventory start agent 'Prepare markers for five workshop participants.'
```

Aider has separate configuration. Use the permitted classroom model and existing
course setup. The example does not change model policy or assume a larger model
is available. `start --build` checks compilation from source; there are no third
party dependencies. `stop`, `restart`, and `status` manage the foreground process.

The worked documents are illustrative, authored alongside the example. Their
reset commit does not purport to be a student's design-before-code history.
A real submission must preserve its own initial design and increment commits.
