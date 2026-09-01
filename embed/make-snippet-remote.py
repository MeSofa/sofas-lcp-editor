#!/usr/bin/env python3
"""
Generate the "thin" Code Snippet that serves the editor by fetching index.html
from a *public* GitHub repo at request time (cached ~5 min).

    python3 embed/make-snippet-remote.py USER/REPO [branch]

e.g.  python3 embed/make-snippet-remote.py sofadoesstuff/sofas-lcp-editor

Writes embed/lcp-editor.remote.snippet.php. Paste into Code Snippet id 10 (or a
new snippet, scope "global", active). After that, updating the live site is just
`git push`; add ?refresh=1 to /lcp-editor to bust the cache immediately.
"""
import datetime
import pathlib
import re
import sys

if len(sys.argv) < 2 or "/" not in sys.argv[1]:
    sys.exit("usage: make-snippet-remote.py USER/REPO [branch]")

repo = sys.argv[1].strip("/")
branch = sys.argv[2] if len(sys.argv) > 2 else "main"
if not re.fullmatch(r"[A-Za-z0-9._-]+/[A-Za-z0-9._-]+", repo):
    sys.exit(f"bad repo slug: {repo!r}")

raw = f"https://raw.githubusercontent.com/{repo}/{branch}/index.html"
stamp = datetime.date.today().isoformat()
SLUG = "lcp-editor"

php = f"""<?php
/**
 * Sofa's LCP Editor -- serves index.html from GitHub ({repo}@{branch}).
 * Generated {stamp}. Paste into Code Snippet, scope "Run everywhere", activate.
 *
 * Update the live site by pushing to the repo. /{SLUG}?refresh=1 forces a
 * re-fetch; otherwise it caches for 5 minutes. If GitHub is unreachable the
 * last successfully-fetched copy is served.
 */

if ( ! defined( 'ABSPATH' ) ) {{ exit; }}

add_action( 'template_redirect', function () {{

	$path = trim( (string) wp_parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ), '/' );
	$last = strtolower( substr( strrchr( '/' . $path, '/' ), 1 ) );
	if ( '{SLUG}' !== $last && ! ( function_exists( 'is_page' ) && is_page( '{SLUG}' ) ) ) {{
		return;
	}}

	$src   = '{raw}';
	$t_key = 'lcp_editor_html';
	$o_key = 'lcp_editor_html_lastgood';
	$html  = isset( $_GET['refresh'] ) ? false : get_transient( $t_key );

	if ( false === $html ) {{
		$resp = wp_remote_get( $src, array( 'timeout' => 8, 'headers' => array( 'Accept' => 'text/html' ) ) );
		if ( ! is_wp_error( $resp ) && 200 === (int) wp_remote_retrieve_response_code( $resp ) ) {{
			$html = wp_remote_retrieve_body( $resp );
			set_transient( $t_key, $html, 5 * MINUTE_IN_SECONDS );
			update_option( $o_key, $html, false );
		}} else {{
			$html = get_option( $o_key );          // serve stale rather than nothing
		}}
	}}

	if ( ! $html ) {{
		status_header( 502 );
		echo 'LCP Editor is temporarily unavailable.';
		exit;
	}}

	nocache_headers();
	status_header( 200 );
	header( 'Content-Type: text/html; charset=utf-8' );
	header( 'X-Frame-Options: SAMEORIGIN' );
	echo $html;
	exit;
}}, 0 );
"""

out = pathlib.Path(__file__).resolve().parent / "lcp-editor.remote.snippet.php"
out.write_text(php)
print(f"wrote {out}  ({len(php)} bytes)")
print(f"source: {raw}")
