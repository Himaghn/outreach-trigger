# outreach-trigger

Two small jobs for a private repository:

1. **Start outreach sender** starts the private "Send due emails" workflow a few
   times shortly after each region's 08:30 morning window, because GitHub's own
   scheduler ran that private job too rarely.
2. **Build dashboard** rebuilds a password-protected status page about every
   15 minutes: https://himaghn.github.io/outreach-trigger/
   The data is encrypted (AES-256) with the password before it is published, and
   decrypted in your browser. Without the password the site shows only a login box.

Secrets in this repo:

- `OUTREACH_TOKEN`: a fine-grained token limited to the private repo, with
  *Actions: read and write* and *Contents: read-only*. Replace it before it expires.
- `DASHBOARD_PASSWORD`: the password for the dashboard (8+ characters). Changing it
  logs every device out at the next rebuild.

Run either by hand: Actions -> pick the workflow -> Run workflow.
GitHub switches off schedules in public repos after 60 days without commits;
if that happens, re-enable the workflows on the Actions tab.
