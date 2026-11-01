# Authoritative Remote-Source Identity Rule

Status: pre-freeze rule adopted 2026-11-01

The repository does not redistribute the authoritative Robodebt PDFs. Freeze identity therefore uses a closed remote-source record rather than pretending that `content_hash: null` is a byte archive.

For every selected source, the freeze manifest must hash the local source-manifest record containing:

1. stable `source_id`;
2. authoritative publisher and document title;
3. publication date and corrected-edition date where applicable;
4. authoritative HTTPS URL;
5. citation-level anchor ID, locator, and bounded summary;
6. authority and permitted-use classification;
7. retrieval-through date;
8. local-copy status and any available remote-byte hash; and
9. caveat, exclusion, or hash note.

The source identity is the canonical serialized local record plus the frozen authoritative URL and metadata. A later remote-byte change does not silently mutate the frozen study: it triggers a source-drift report, retrieval of both available versions where lawful, and a determination whether the cited proposition changed. Redirects, inaccessible URLs, or changed landing-page layout do not alter identity when publisher, title, date, and citation locator remain unambiguous; they do require a logged availability warning.

## Freeze procedure

- Hash `data/sources/robodebt/source_manifest.yaml` and both dated application profiles.
- Store the retrieval date, URL, HTTP outcome if checked, content type, and any byte hash obtainable without bypassing access controls in the freeze manifest's source-identity section.
- Never infer a historical numeric value from successful retrieval or from a missing hash.
- Preserve `content_hash: null` when bytes are not archived; do not replace it with the hash of an HTML error page, consent page, redirect wrapper, or locally transformed text.
- If the authoritative source becomes unavailable, use an official archive or library copy only through a versioned manifest amendment before confirmatory execution. After freeze, any source-identity amendment invalidates the affected run and requires a new freeze version.

This rule establishes reproducible citation identity, not permanent custody of third-party documents.
