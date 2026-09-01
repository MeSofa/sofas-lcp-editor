# Deploying to WordPress (standalone page)

`index.html` is served **as-is** at `/lcp-editor` — no theme header, footer or
nav, exactly like opening the file directly.

## One-time setup

1. **Snippets → Add New** (Code Snippets plugin). Title: `Sofa's LCP Editor`.
2. Paste the entire contents of **`lcp-editor.snippet.php`**.
3. Scope: **Run snippet everywhere**. **Save Changes and Activate.**
4. Visit `yoursite.com/lcp-editor`.

Optionally create a published **Page** with slug `lcp-editor` (any title, content
ignored) so it shows up in the auto-generated nav — the snippet intercepts that
slug and serves the raw app instead of the themed page.

## How it works

The snippet hooks `template_redirect`; when the request path ends in `lcp-editor`
(or a Page with that slug is being viewed) it prints `index.html` verbatim and
`exit`s before the theme loads. It matches on the request path, not a rewrite
rule, so there's no permalink flush.

## Updating

After any change to `index.html`:

```
python3 embed/make-snippet.py
```

then paste the regenerated `lcp-editor.snippet.php` over the existing snippet.
