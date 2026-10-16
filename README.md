# outreach-trigger

Starts the "Send due emails" workflow in a private repository a few times
shortly after each region's 08:30 morning window, because GitHub's own
scheduler ran that private job too rarely. Nothing else lives here.

- Secret `OUTREACH_TOKEN`: a fine-grained token limited to the private repo,
  with only *Actions: read and write*. Replace it before it expires.
- Run it by hand: Actions -> Start outreach sender -> Run workflow.
- GitHub switches off schedules in public repos after 60 days without commits;
  if that happens, re-enable the workflow on the Actions tab.
