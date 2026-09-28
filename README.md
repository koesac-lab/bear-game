# Fat Bear Family — complete performance and UX build

This is a complete build, not an upgrade or a patch. It extracts to `/home/bear-game/` and does not alter the old `/home/fatbear-family/`. Its dynamic join QR uses **Segno**, a pure-Python QR generator; it does not need the unavailable `libqrencode-tools` package. Python 3.9+ is required. All app code uses Python's standard library apart from Segno for QR.

## iPhone installation

1. Stop the old server with Ctrl-C. Leave its folder untouched.
2. Save the supplied archive to the iSH Files location, e.g. `/home`. iOS may append `.tar` to the archive name. Run `ls -1 /home` and use the **exact visible filename** in this command:

   ```sh
   cd /home
   tar -xzf bear-game.tar.gz
   cd bear-game
   sh setup.sh
   python3 cache_photos.py
   python3 server.py 4
   ```

   If Files named it `bear-game.tar.gz.tar`, use that after `tar -xzf` instead. Replace `4` with the actual number of players (2–30). If you already installed Python in iSH, no reinstall is needed. If `sh setup.sh` cannot find pip, it attempts `apk add py3-pip` and then installs Segno from PyPI. The setup script checks the import before reporting success. Internet is required for this first setup and photo prefetch.
3. Keep iSH in the foreground and the phone awake, ideally charging. Find the iPhone IP in Settings → Wi-Fi → ⓘ. Open `http://<IPHONE-IP>:8765/display` on the communal browser and `http://<IPHONE-IP>:8765/` on player phones. The communal screen has the join QR. If you use `localhost` to open it, the QR intentionally warns rather than encoding a link no other device can open.
4. Type the correct Wi-Fi name into the communal screen once; it is saved in that browser, not guessed from iOS. The QR encodes **only** the game URL, not Wi-Fi credentials. If a QR is absent, visit `http://<IPHONE-IP>:8765/join-qr.svg` to see the exact server error. If it says Segno is missing, rerun `sh setup.sh`.
5. Select **View all 16 photos** on the communal screen to inspect a side-by-side overview of every contender’s bracket image and alternate source. It shows how many of the 20 photo assets cached successfully. Tap an image for a larger view.

## Game behaviour

The game begins when the configured number of named players join; this freezes the roster. Players can change picks until all have voted or the default 180-second timeout ends. Then a 3-second suspense lock, automatic reveal, 12-second results display and automatic next match. The communal screen shows both bears, player submission count, scoreboard, ✓/✕ history and spoiler-safe bracket. The first 12 known results give one point per correct pick. The three future matches are unscored family predictions; a tie is labelled a coin toss, never an official result. `VOTE_SECONDS=240 python3 server.py 4` extends the time limit if needed.

## Photo honesty and cache

The archive has stories and URLs for four 2026 bracket grids plus one alternate photo or profile graphic for each of 16 entries. It does **not** contain third-party binary photos. `cache_photos.py` downloads any reachable images into local `media/`; the player UI falls back to the bracket grid if an alternate source fails and then to a labelled placeholder if both fail. The overview shows missing thumbnails rather than silently substituting another bear. It cannot promise all 20 sources will remain online—verify the cache count before an offline event.

Photos have no verified dates in this build and must not be called “before” or “after”. Player cards link to official Explore.org bios, source photo pages and the official tournament page for dated comparison photographs. Photo source credits and URLs are in `data.py`; private family use does not imply a licence to redistribute them.

## State and files

This fresh folder starts a new game and writes its own `game.json` on first launch. Keep the original folder to retain its old game. The new build will not overwrite that game or its image cache. To continue an old game later, stop the new server, back up both state files and copy the old `game.json` into this folder before restarting; leave the old folder in place.

- `server.py`: LAN game, timer, spoiler-safe results, QR SVG and photo cache.
- `data.py`: 16 richer profiles, image attribution/source links and bracket results.
- `index.html`: player photos, stories, links and private votes.
- `display.html`: communal screen, Wi-Fi-name label, QR, current bears and scoreboard.
- `photos.html`: all-16 photo overview and enlargements.
- `cache_photos.py`: prefetch of 20 photo sources.
- `setup.sh`: installs/checks the Segno QR dependency.

This is a trusted-LAN HTTP app, not a public-internet deployment. All browsers must be on a mutually reachable Wi-Fi network; guest/client isolation can block the connection.

## Performance and experience update

The 16 static bear profiles load once per browser session from `/api/profiles`. `/api/state` carries only live game data and remains uncached. Player tabs stop polling while hidden and fetch immediately on return; the communal display keeps updating. Vote counts, phase changes and score updates no longer replace the current photo cards. The shared display switches its two images every nine seconds without replacing surrounding cards. Media responses allow browser caching for one day.

The current game stays visible through brief connection problems; after two missed polls the UI shows a reconnecting message. Vote submissions disable buttons while saving and show success/failure inline. The shared-screen lobby shows whether the join QR loaded and how many photo files are cached. Check the QR with a second phone and use the all-photos view to inspect missing images.
