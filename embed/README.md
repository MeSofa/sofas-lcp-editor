# Self-hosting as a standalone page

`index.html` is fully self-contained, so hosting it is trivial — drop the file
anywhere static and open it. These helpers are for serving it from a WordPress
site at a clean path (e.g. `/lcp-editor`) with no theme wrapper, via the
**Code Snippets** plugin.

## Option A — bake the HTML into the snippet

```
python3 embed/make-snippet.py
```

Paste the generated `lcp-editor.snippet.php` into a new snippet (scope: run
everywhere), activate it, and the app is served at `/lcp-editor`. Re-run and
re-paste after every change to `index.html`.

## Option B — fetch from a public GitHub repo

```
python3 embed/make-snippet-remote.py USER/REPO
```

This snippet fetches `index.html` from the repo at request time and caches it
for 5 minutes (`?refresh=1` on the URL busts the cache; the last good copy is
served if the fetch fails). After the one-time paste, updating the live site is
just `git push`.

## How the snippet works

It hooks `template_redirect`, and when the request path ends in `lcp-editor`
(or a Page with that slug is being viewed) it prints the HTML and `exit`s
before the theme loads. Path matching, not a rewrite rule, so no permalink
flush is needed. Optionally publish an empty Page with that slug so it appears
in an auto-generated nav.
