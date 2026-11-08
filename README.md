# PrivateLabel for Deluge 2.x

### Allows labeling torrents by the private flag of the torrent.

Ever wanted to set **all** your public torrents to seed until meeting a ratio while leaving the seeds for your private trackers to seed indefinitely with just a couple clicks?

<img width="376" height="379" alt="image" src="https://github.com/user-attachments/assets/fc5a5998-4cce-457b-aa74-49499bc07373" />

PrivateLabel is a fork of Deluge's built-in **Label** plugin. It adds two checkboxes to a label's **Trackers** tab: apply the label to torrents **with** the private flag, and/or to torrents **without** it. The original tracker-substring auto-add still works, and the two combine (a torrent matching either one gets the label).

Because torrents that are not private may not include `private=0`, anything not explicitly flagged private is treated as public. If your favorite private tracker doesn't set the private flag on its torrents, those torrents will be treated as public.

## Example: stop public seeds at a ratio, let private seeds run forever

1. Leave Deluge's global "stop seeding at ratio" **off**.
2. Create a label, e.g. `public`, and open its options.
3. On the **Queue** tab tick **Apply Queue settings**, tick **Stop seed at ratio**, and set the ratio.
4. On the **Trackers** tab tick **Automatically apply label** and **Torrents without the private flag (public)**.
5. Click OK.

Private torrents match nothing, so they stay unlabeled and keep the global setting (off) — or mark them as private for symmetry. 

> [!CAUTION]
> ## Behavior to know about:
>
> **If you already use labels, this plugin is _probably_ not for you. Please read the following:**
> - **Saving a label re-sweeps your whole queue.** When you save a label that has auto-apply on, every existing torrent that matches is assigned that label, **including torrents already in another label**. This is intentional (set it once and it applies to everything), but if you use several labels, be aware a broad rule like "without the private flag" will pull matching torrents into its label.
> - **Magnet links** have no private flag until their metadata arrives, so they are skipped until then and labeled afterwards. Not yet verified on a live daemon.
> - If more than one label matches a new torrent, the first one wins.


## Installation

PrivateLabel installs as a separate plugin and **replaces** the built-in Label plugin rather than extending it:

- Enable **PrivateLabel** and disable **Label**. Both register the same sidebar category and Label column, so don't run them together.
- It uses its own config file, `privatelabel.conf`, and its own RPC namespace (`privatelabel`). Your existing labels are not carried over. To keep them, copy `label.conf` to `privatelabel.conf` in the daemon's config folder before enabling the plugin (the format is the same).
- The Web UI part of Label is not included. GTK client only.

The plugin has a daemon half and a GTK half, so it must be installed on both the machine running `deluged` and the machine running `deluge-gtk`. Eggs are tied to a Python version: the `pyX.Y` in the filename must match the Python that runs the daemon or client, or Deluge will not list the plugin. The repo includes a prebuilt `PrivateLabel-0.3-py3.14.egg`; it is pure Python, so the tag can be changed by renaming the file. To check, run `deluged --version`, which prints the Python version.

- **Local:** copy the egg into Deluge's `plugins` folder (`~/.config/deluge/plugins` on Linux), then enable it in Preferences → Plugins.
- **Remote daemon:** connect `deluge-gtk` to the daemon and use Preferences → Plugins → **Install**; the client uploads the egg to the daemon.
- **Build from source:** `python setup.py bdist_egg`, and the egg lands in `dist/`.

See also the [official Deluge plugin installation instructions](https://deluge-torrent.org/plugins/#install).

## Status

Written against Deluge 2.2.0 and current master. The private-flag matching logic has been tested against mock torrents; it has had limited testing in a live client. Provided as-is; I use it myself and and plan only limited support going forward.

## License

GPL-3.0-or-later with Deluge's OpenSSL linking exception, as with Deluge itself (see `LICENSE`). Based on the Label plugin by Martijn Voncken and Andrew Resch.
