# Embedding on WordPress

`index.html` is self-contained, so the embed is just an iframe of it served
from your own domain.

## One-time setup

1. **Snippets → Add New** (Code Snippets plugin). Title it `Sofa's LCP Editor`.
2. Paste the entire contents of **`lcp-editor.snippet.php`**.
3. Scope: **Run snippet everywhere**. **Save Changes and Activate**.
4. On the page where you want the editor, add a **Custom HTML** block:

   ```
   [lcp_editor]
   ```

   Optional height: `[lcp_editor height="1000px"]` (default `88vh`).

## How it works

- The snippet serves `index.html` verbatim at `/?lcp_editor_app=1` (a query
  param, so no rewrite-rule flush needed).
- `[lcp_editor]` renders a same-origin `<iframe>` pointing at that URL, so the
  app runs fully isolated — its own CSS/JS, its own `localStorage` (settings
  persist per visitor), no theme conflicts, downloads work.

## Updating

After any change to `index.html`:

```
python3 embed/make-snippet.py
```

then paste the regenerated `lcp-editor.snippet.php` over the existing snippet.
