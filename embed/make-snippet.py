#!/usr/bin/env python3
"""
Generate the WordPress Code Snippet that serves Sofa's LCP Editor as a
standalone full-page app at /lcp-editor -- no theme header, footer or nav,
exactly like index.html on its own.

    python3 embed/make-snippet.py

Reads ../index.html, writes embed/lcp-editor.snippet.php. Paste that into a new
Code Snippet (scope: "Run everywhere" / front-end), Save & Activate. Then visit
yoursite.com/lcp-editor.

Re-run and re-paste whenever index.html changes.
"""
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
html = (ROOT / "index.html").read_text()
if "\r" in html:
    html = html.replace("\r\n", "\n").replace("\r", "\n")

DELIM = "LCPEDITORAPPHTML"
if DELIM in html:
    sys.exit(f"index.html contains {DELIM!r}; pick another nowdoc delimiter.")

SLUG = "lcp-editor"
stamp = datetime.date.today().isoformat()

php = f"""<?php
/**
 * Sofa's LCP Editor -- standalone full-page app.
 * Generated from index.html on {stamp}.
 *
 * 1. Snippets -> Add New. Title: "Sofa's LCP Editor". Paste this whole file.
 * 2. Scope: "Run snippet everywhere". Save Changes and Activate.
 * 3. Visit  yoursite.com/{SLUG}
 *
 * Serves index.html verbatim -- no theme, no header/footer -- for the request
 * path /{SLUG} (and for a Page with that slug, if one exists, so it can show in
 * the nav). No rewrite rules, so no need to flush permalinks.
 *
 * Re-run embed/make-snippet.py and re-paste after any index.html change.
 */

if ( ! defined( 'ABSPATH' ) ) {{ exit; }}

add_action( 'template_redirect', function () {{

	$path  = trim( wp_parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ) ?? '', '/' );
	$last  = strtolower( substr( strrchr( '/' . $path, '/' ), 1 ) );
	$match = ( '{SLUG}' === $last ) || ( function_exists( 'is_page' ) && is_page( '{SLUG}' ) );

	if ( ! $match ) {{
		return;
	}}

	nocache_headers();
	status_header( 200 );
	header( 'Content-Type: text/html; charset=utf-8' );
	header( 'X-Frame-Options: SAMEORIGIN' );

	echo <<<'{DELIM}'
{html}
{DELIM};
	exit;
}}, 0 );
"""

out = ROOT / "embed" / "lcp-editor.snippet.php"
out.write_text(php)
print(f"wrote {out.relative_to(ROOT)}  ({len(php):,} bytes) -> serves /{SLUG}")
