#!/usr/bin/env python3
"""
Generate the WordPress Code Snippet that embeds Sofa's LCP Editor.

    python3 embed/make-snippet.py

Reads ../index.html, writes embed/lcp-editor.snippet.php — paste that into a new
Code Snippet (scope: "Run everywhere" / front-end), activate it, then drop
[lcp_editor] into a Custom HTML block on any page.

The snippet serves index.html verbatim at /?lcp_editor_app=1 and the shortcode
renders a same-origin <iframe> pointing at it, so the app runs fully isolated
(its own CSS/JS/localStorage) with no theme conflicts. Re-run this whenever
index.html changes and re-paste.
"""
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
html = (ROOT / "index.html").read_text()

DELIM = "LCPEDITORAPPHTML"
if DELIM in html:
    sys.exit(f"index.html contains {DELIM!r}; pick another nowdoc delimiter.")
if "\r" in html:
    html = html.replace("\r\n", "\n").replace("\r", "\n")

stamp = datetime.date.today().isoformat()

php = f"""<?php
/**
 * Sofa's LCP Editor -- front-end embed.
 * Generated from index.html on {stamp}.
 *
 * 1. Snippets -> Add New. Title: "Sofa's LCP Editor". Paste this whole file.
 * 2. Scope: "Run snippet everywhere". Save & Activate.
 * 3. On any page, add a *Custom HTML* block containing:  [lcp_editor]
 *    Optional height:  [lcp_editor height="1000px"]   (default 88vh)
 *
 * Re-run embed/make-snippet.py and re-paste after any index.html change.
 */

if ( ! defined( 'ABSPATH' ) ) {{ exit; }}

/* Serve the app itself at /?lcp_editor_app=1 (no rewrite rules, no flush needed). */
add_action( 'template_redirect', function () {{
	if ( ! isset( $_GET['lcp_editor_app'] ) ) {{
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
}} );

/* [lcp_editor] -> a same-origin iframe of the app. */
add_shortcode( 'lcp_editor', function ( $atts ) {{
	$a   = shortcode_atts( array( 'height' => '88vh' ), $atts, 'lcp_editor' );
	$src = esc_url( add_query_arg( 'lcp_editor_app', '1', home_url( '/' ) ) );
	$h   = preg_replace( '/[^0-9a-z%.]/i', '', (string) $a['height'] );
	if ( '' === $h ) {{
		$h = '88vh';
	}}
	return sprintf(
		'<iframe src="%s" title="Sofa&#039;s LCP Editor" loading="lazy" '
		. 'style="display:block;width:100%%;height:%s;min-height:600px;border:0;border-radius:8px;background:#14161c"></iframe>',
		$src,
		esc_attr( $h )
	);
}} );
"""

out = ROOT / "embed" / "lcp-editor.snippet.php"
out.write_text(php)
print(f"wrote {out.relative_to(ROOT)}  ({len(php):,} bytes, from {len(html):,} bytes of HTML)")
