#!/usr/bin/awk -f

# Removes comments and empty lines from Python files.
# If -d option is given, removes docstrings (triple-quoted block strings)
# that start at the beginning of a statement (ignoring indentation and
# optional string prefixes like r, u, f, b).
#
# Usage:
#   awk -f truncate.awk [-d] file.py

BEGIN {
    # Parse options: support -d to remove docstrings
    docDel = 0
    for (i = 1; i < ARGC; i++) {
        if (ARGV[i] == "-d") {
            docDel = 1
            ARGV[i] = ""  # remove from ARGV so awk doesn't treat it as filename
        }
    }

    in_triple = 0         # inside any triple-quoted string
    in_docstring = 0      # inside a docstring block to be removed
    triple_delim = ""    # """ or '''
}

# Trim helper
function trim(s) {
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", s)
    return s
}

# Process a single line: remove trailing comments outside strings
function strip_inline_comment(s,    out, i, c, in_single, in_double) {
    out = ""
    in_single = 0
    in_double = 0
    i = 1
    while (i <= length(s)) {
        # Handle triple-quoted string context
        if (in_triple) {
            if (substr(s, i, 3) == triple_delim) {
                out = out substr(s, i, 3)
                in_triple = 0
                i += 3
                continue
            } else {
                out = out substr(s, i, 1)
                i++
                continue
            }
        }

        c = substr(s, i, 1)

        # Detect triple-quote start (prefer this before single/double toggles)
        if (substr(s, i, 3) == "\"\"\"" || substr(s, i, 3) == "'''") {
            triple_delim = substr(s, i, 3)
            in_triple = 1
            out = out triple_delim
            i += 3
            continue
        }

        # Toggle single/double quoted strings
        if (c == "'" && !in_double) {
            in_single = (in_single ? 0 : 1)
            out = out c
            i++
            continue
        }
        if (c == "\"" && !in_single) {
            in_double = (in_double ? 0 : 1)
            out = out c
            i++
            continue
        }

        # Comment start outside any string -> cut off rest
        if (c == "#" && !in_single && !in_double) {
            break
        }

        out = out c
        i++
    }
    return out
}

{
    line = $0

    # If currently inside a docstring block to be removed, seek closing and skip
    if (docDel && in_docstring) {
        # Find closing delimiter on this line
        ci = index(line, triple_delim)
        if (ci > 0) {
            # Close docstring and continue with remainder after closing
            in_docstring = 0
            in_triple = 0
            line = substr(line, ci + 3)
        } else {
            next
        }
    }

    # Detect docstring start at beginning of statement (indent + optional prefix)
    if (docDel && !in_docstring) {
        i3 = index(line, "\"\"\"")
        i1 = index(line, "'''")
        earliest = 0
        delim = ""
        if (i3 > 0) { earliest = i3; delim = "\"\"\"" }
        if (i1 > 0 && (earliest == 0 || i1 < earliest)) { earliest = i1; delim = "'''" }
        if (earliest > 0) {
            prefix = substr(line, 1, earliest - 1)
            # Allow indentation and optional string prefixes (r, u, f, b in any case)
            if (prefix ~ /^[[:space:]]*([rRuUfFbB]+)?[[:space:]]*$/) {
                # Start removing docstring
                triple_delim = delim
                after = substr(line, earliest + 3)
                ci2 = index(after, triple_delim)
                if (ci2 > 0) {
                    # Docstring ends on the same line; remove the whole block
                    remainder = substr(after, ci2 + 3)
                    line = prefix remainder
                } else {
                    in_docstring = 1
                    in_triple = 1
                    line = prefix
                }
            }
        }
    }

    # Remove full-line comments and blanks after processing docstring logic
    tmp = trim(line)
    if (tmp ~ /^#/) {
        next
    }

    # Strip trailing comments outside strings
    processed = strip_inline_comment(line)
    if (trim(processed) == "") {
        next
    }
    print processed
}
