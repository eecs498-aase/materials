#!/usr/bin/env python3
"""Run the four enforced scans from /mean-review Step 3 and print every hit.

Rules (thresholds are the skill's, not tunable per run):
  10-line        a run of 10 or more non-trivial code lines with no comment
  fn-length      a function whose body is longer than 50 non-blank lines
  weak-name      a name bound as data, tmp, result, ret, res, helper, handle,
                 doit/do_it, process, util, utils, temp, or obj
  silent-except  an except/catch block that swallows the error

Python files are parsed with the standard library (ast and tokenize), so
those findings come from the syntax tree rather than pattern matching, and
declarative code (imports, literal tables, field lists, docstrings) is
already exempt from the 10-line rule. Weak names are reported once per name
per scope, at the line that first binds them. An except body "surfaces" the
error if it raises, calls anything on a logger, or calls print, warn,
exit, report, and similar names; a custom error helper needs a human read. Other
languages use line rules and are marked "heuristic": read the span before
you report it, and drop any declarative span by hand. Config formats
(YAML, TOML, JSON) are declarative by nature and are skipped.

Usage:
  python3 enforced_scans.py FILE_OR_DIR [FILE_OR_DIR ...]
  python3 enforced_scans.py --json FILE_OR_DIR [...]
  git diff --name-only main...HEAD | python3 enforced_scans.py --stdin

Exit codes:
  0  the scan ran (with or without findings)
  2  bad arguments, or none of the inputs could be scanned
"""

import argparse
import ast
import io
import json
import os
import re
import sys
import tokenize

# Rensin's rule: flag any place that goes 10 lines without a comment.
COMMENT_SPAN_LIMIT = 10
# The skill's threshold. Length alone is not a defect; it earns a look.
FUNCTION_BODY_LIMIT = 50
WEAK_ALTERNATION = r"(data|tmp|result|ret|res|helper|handle|do_?it|process|util|utils|temp|obj)"
WEAK_NAME = re.compile(r"^" + WEAK_ALTERNATION + r"$")

# Comment syntax by file extension. Python is handled separately with ast.
COMMENT_STYLE = {}
for _ext in (".sh", ".bash", ".zsh", ".rb", ".pl", ".r", ".ps1", ".mk"):
    COMMENT_STYLE[_ext] = "hash"
for _ext in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".java", ".c", ".h",
             ".cc", ".cpp", ".hpp", ".cs", ".go", ".rs", ".swift", ".kt", ".kts",
             ".scala", ".dart", ".php"):
    COMMENT_STYLE[_ext] = "slash"
for _ext in (".sql", ".lua", ".hs"):
    COMMENT_STYLE[_ext] = "dash"
# Functions in these languages close with a brace, so a brace count works.
BRACE_FUNCTIONS = {ext for ext, style in COMMENT_STYLE.items() if style == "slash"} | {".sh", ".bash", ".zsh"}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "target",
             ".venv", "venv", "__pycache__", ".mypy_cache", ".tox"}

# A line made only of brackets and separators carries no logic of its own.
TRIVIAL_LINE = re.compile(r"^[\[\]\(\)\{\};,]*$|^(end|fi|done|esac)$")
CONTROL_WORDS = {"if", "for", "while", "switch", "catch", "else", "return",
                 "do", "try", "with", "elif", "until", "foreach", "using", "lock"}
# What counts as surfacing an error in an except body: re-raising, any call
# on a logger (logger.debug counts, it still records the error), or a call
# with one of these exact names. A helper named mark_error_flag() does not.
SURFACING_NAMES = {"print", "warn", "warning", "error", "exception", "critical", "info", "debug",
                   "log", "fatal", "report", "abort", "exit", "_exit", "fail", "notify", "alert", "print_exc"}
LOGGER_NAME = re.compile(r"log", re.I)


def finding(path, line, rule, detail, method, end_line=None):
    """Build one finding record. end_line differs from line only for spans."""
    return {"file": path, "line": line, "end_line": end_line or line,
            "rule": rule, "detail": detail, "method": method}


def comment_spans(path, lines, comment_lines, skip_lines, method):
    """Find runs of COMMENT_SPAN_LIMIT or more code lines with no comment.
    Blank, trivial, and skipped lines neither count toward a run nor end it;
    a comment line ends it."""
    results = []
    run = {"start": None, "end": None, "size": 0}

    def close_run():
        # A run only becomes a finding once it reaches the limit.
        if run["size"] >= COMMENT_SPAN_LIMIT:
            results.append(finding(path, run["start"], "10-line",
                                   "{} code lines with no comment".format(run["size"]),
                                   method, run["end"]))
        run.update(start=None, end=None, size=0)

    # Blank, trivial, and declarative lines are invisible to the rule.
    for number, raw in enumerate(lines, start=1):
        text = raw.strip()
        if not text or TRIVIAL_LINE.match(text) or number in skip_lines:
            continue
        if number in comment_lines:
            close_run()
            continue
        # Any other line is logic: it extends the current run.
        if run["start"] is None:
            run["start"] = number
        run["end"] = number
        run["size"] += 1
    close_run()
    return results


# ---------------------------------------------------------------- Python ---

def python_comment_lines(source):
    """Line numbers carrying a # comment. tokenize is used so that a '#'
    inside a string literal is never mistaken for a comment."""
    lines = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.COMMENT:
                lines.add(tok.start[0])
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass  # a partial set is still useful; ast reports the real error
    return lines


def is_docstring(node):
    """A bare string as the first statement of a module, class, or def."""
    return (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str))


def is_declarative_value(node):
    """Literal tables and field declarations: the shape is the explanation,
    so the 10-line rule does not apply to them."""
    if node is None or isinstance(node, (ast.Constant, ast.Name, ast.Attribute)):
        return True
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return all(is_declarative_value(e) for e in node.elts)
    if isinstance(node, ast.Dict):
        return all(is_declarative_value(v) for v in node.values) and all(
            k is None or is_declarative_value(k) for k in node.keys)
    # dataclass field(...) and pydantic Field(...) declare, they do not compute.
    if isinstance(node, ast.Call):
        return call_name(node) in {"field", "Field", "frozenset", "namedtuple"}
    return False


def call_name(node):
    """The bare name of a call: foo() -> foo, log.warning() -> warning."""
    func = node.func
    return getattr(func, "id", None) or getattr(func, "attr", None) or ""


def python_exempt_lines(tree):
    """Return (docstring_lines, declarative_lines). Docstrings count as
    comments; declarative statements at module or class level are skipped."""
    docstrings, declarative = set(), set()

    def lines_of(node):
        return range(node.lineno, (node.end_lineno or node.lineno) + 1)

    def visit(body, top_level):
        # Only module and class bodies hold declarations; a function body
        # is logic even when a statement in it looks like a table.
        for index, stmt in enumerate(body):
            if index == 0 and is_docstring(stmt):
                docstrings.update(lines_of(stmt))
            elif top_level and (
                    isinstance(stmt, (ast.Import, ast.ImportFrom))
                    or (isinstance(stmt, (ast.Assign, ast.AnnAssign)) and is_declarative_value(stmt.value))):
                declarative.update(lines_of(stmt))
            # Class bodies stay top level (fields are declarations); defs do not.
            if isinstance(stmt, ast.ClassDef):
                visit(stmt.body, top_level=True)
            elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit(stmt.body, top_level=False)

    visit(tree.body, top_level=True)
    return docstrings, declarative


def catches_everything(handler):
    """Bare except, except Exception, except BaseException, or a tuple with one."""
    if handler.type is None:
        return True
    kinds = handler.type.elts if isinstance(handler.type, ast.Tuple) else [handler.type]
    return any((getattr(k, "id", None) or getattr(k, "attr", None)) in {"Exception", "BaseException"}
               for k in kinds)


def surfaces_error(handler):
    """True when the except body re-raises, logs, prints, or exits."""
    for stmt in handler.body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Raise):
                return True
            if not isinstance(node, ast.Call):
                continue
            # logger.info(...), self.log.debug(...), logging.warning(...)
            receiver = getattr(node.func, "value", None)
            receiver_name = getattr(receiver, "id", None) or getattr(receiver, "attr", None) or ""
            if call_name(node) in SURFACING_NAMES or LOGGER_NAME.search(receiver_name):
                return True
    return False


class PythonScanner(ast.NodeVisitor):
    """Collects fn-length, weak-name, and silent-except findings. Weak names
    are reported once per name per scope, at the first line that binds them,
    so a loop that reassigns `result` ten times is one finding, not ten."""

    def __init__(self, path, lines):
        self.path, self.lines, self.results = path, lines, []
        self.scope, self.reported = ["<module>"], set()

    def weak(self, name, line, kind):
        """Record a weak name unless this scope already reported it."""
        key = (self.scope[-1], name)
        if name and WEAK_NAME.match(name) and key not in self.reported:
            self.reported.add(key)
            self.results.append(finding(self.path, line, "weak-name", "{} ({})".format(name, kind), "exact"))

    def visit_function(self, node):
        """Check the function's length, then its name and parameters."""
        self.weak(node.name, node.lineno, "function")
        # Measure from the first real statement; the docstring is a comment.
        body = node.body[1:] if node.body and is_docstring(node.body[0]) else node.body
        if body:
            first, last = body[0].lineno, node.end_lineno or body[-1].lineno
            size = sum(1 for n in range(first, last + 1) if self.lines[n - 1].strip())
            if size > FUNCTION_BODY_LIMIT:
                self.results.append(finding(self.path, node.lineno, "fn-length",
                                            "{}() body is {} lines (limit {})".format(node.name, size, FUNCTION_BODY_LIMIT),
                                            "exact"))
        # Parameters belong to the function's own scope, not the caller's.
        self.scope.append(node.name)
        args = node.args
        for arg in args.posonlyargs + args.args + args.kwonlyargs + [a for a in (args.vararg, args.kwarg) if a]:
            self.weak(arg.arg, arg.lineno, "parameter")
        self.generic_visit(node)
        self.scope.pop()

    visit_FunctionDef = visit_function
    visit_AsyncFunctionDef = visit_function

    def visit_ClassDef(self, node):
        """A class name can be weak too, and its body is its own scope."""
        self.weak(node.name, node.lineno, "class")
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_Name(self, node):
        """Only bindings count; reading a weak name is not a new finding."""
        if isinstance(node.ctx, ast.Store):
            self.weak(node.id, node.lineno, "variable")

    def visit_Attribute(self, node):
        """`self.data = ...` binds a weak attribute name just as surely."""
        if isinstance(node.ctx, ast.Store):
            self.weak(node.attr, node.lineno, "attribute")
        self.generic_visit(node)

    def visit_import(self, node):
        """`import pandas as tmp` binds a name too. The line comes from the
        import statement, since aliases carry no line number before 3.10."""
        for alias in node.names:
            if alias.asname:
                self.weak(alias.asname, node.lineno, "import alias")

    visit_Import = visit_import
    visit_ImportFrom = visit_import

    def visit_ExceptHandler(self, node):
        """Flag broad handlers that neither re-raise nor log."""
        if node.name:
            self.weak(node.name, node.lineno, "exception variable")
        if catches_everything(node) and not surfaces_error(node):
            caught = "bare except" if node.type is None else "except " + ast.unparse(node.type)
            self.results.append(finding(self.path, node.lineno, "silent-except",
                                        "{} swallows the error (no raise, no log)".format(caught), "exact"))
        self.generic_visit(node)


def scan_python(path, source):
    """Exact scans via ast. A file that does not parse falls back to the
    line rules so the reviewer still gets something, labeled as such."""
    try:
        tree = ast.parse(source)
    except SyntaxError as err:
        results = scan_by_lines(path, source, "hash", brace_functions=False)
        for item in results:
            item["detail"] += " (file did not parse: {})".format(err.msg)
        return results
    # Docstrings count as comments; declarative lines are skipped entirely.
    lines = source.splitlines()
    docstrings, declarative = python_exempt_lines(tree)
    results = comment_spans(path, lines, python_comment_lines(source) | docstrings, declarative, "exact")
    scanner = PythonScanner(path, lines)
    scanner.visit(tree)
    return results + scanner.results


# ------------------------------------------------------- other languages ---

def strip_strings(line):
    """Blank out quoted text so comment markers and braces inside string
    literals are ignored."""
    return re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`', '""', line)


# A slash-style comment either starts the line or follows whitespace or ';'.
# A leading '*' only counts with a space after it, so C's `*ptr = 1;` is code.
SLASH_LINE_COMMENT = re.compile(r"^(//|/\*|\*/|\*(\s|$))|(^|\s|;)(//|/\*)")


def comment_lines_for(lines, style):
    """Line numbers that hold a comment, for hash, slash, or dash styles."""
    found, in_block = set(), False
    for number, raw in enumerate(lines, start=1):
        code = strip_strings(raw.strip())
        if style == "slash":
            # Every line inside /* ... */ is a comment line.
            if in_block:
                found.add(number)
                in_block = "*/" not in code
                continue
            if SLASH_LINE_COMMENT.search(code):
                found.add(number)
                opened = code.rfind("/*")
                in_block = opened != -1 and "*/" not in code[opened:]
        # Hash and dash styles have no block form, so one test per line works.
        elif style == "hash" and re.search(r"(^|\s)#", code):
            found.add(number)
        elif style == "dash" and re.search(r"(^|\s)--", code):
            found.add(number)
    return found


FUNCTION_HEADS = [
    re.compile(r"\bfunction\s*\*?\s*(\w+)\s*\("),                    # JS, TS, PHP
    re.compile(r"^\s*func\s+(?:\([^)]*\)\s*)?(\w+)\s*\("),            # Go
    re.compile(r"\bfn\s+(\w+)"),                                       # Rust
    re.compile(r"\b(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{"),     # JS arrow
    re.compile(r"\b(\w+)\s*\([^;{}]*\)[^;{}=]*\{\s*$"),               # C-like, shell
]


def function_name_at(code):
    """Name of the function a line opens, or None. Control-flow keywords
    such as `if (x) {` look like calls with a brace, so they are excluded."""
    for pattern in FUNCTION_HEADS:
        match = pattern.search(code)
        if match:
            return match.group(1) if match.group(1) not in CONTROL_WORDS else None
    return None


def body_extent(lines, head):
    """(open_line, close_line) of the brace block starting at or just below
    `head`, or None. The opening brace may sit up to two lines down."""
    depth, open_line = 0, None
    for offset in range(head, len(lines)):
        stripped = strip_strings(lines[offset])
        if open_line is None:
            if "{" not in stripped:
                if offset - head >= 2:
                    return None
                continue
            open_line = offset
        # Track nesting until the block that opened here closes again.
        depth += stripped.count("{") - stripped.count("}")
        if depth <= 0:
            return open_line, offset
    return None


def function_lengths(path, lines):
    """Brace-count from each function head to its closing brace. Heuristic:
    a brace inside a comment can throw the count off."""
    results = []
    for index, raw in enumerate(lines):
        name = function_name_at(strip_strings(raw))
        extent = body_extent(lines, index) if name else None
        if not extent:
            continue
        # Count non-blank lines strictly between the braces, as for Python.
        body = sum(1 for n in range(extent[0] + 1, extent[1]) if lines[n].strip())
        if body > FUNCTION_BODY_LIMIT:
            results.append(finding(path, index + 1, "fn-length",
                                   "{}() body is about {} lines (limit {})".format(name, body, FUNCTION_BODY_LIMIT),
                                   "heuristic"))
    return results


# Declaration shapes across common languages: keyword declarations, function
# definitions, plain or := assignments, and typed C-family declarations.
WEAK_DECLARATIONS = [
    re.compile(r"\b(?:const|let|var|val|auto|local|my)\s+\$?" + WEAK_ALTERNATION + r"\b"),
    re.compile(r"\b(?:function|def|fn|func)\s+" + WEAK_ALTERNATION + r"\s*\("),
    re.compile(r"^\s*\$?" + WEAK_ALTERNATION + r"\s*(?::=|=(?!=))"),
    re.compile(r"\b(?:int|long|float|double|char|bool|boolean|byte|short|string|String|Object)\s+"
               + WEAK_ALTERNATION + r"\s*[=;,)]"),
]
# An empty catch body, or one holding only comments, swallows the error.
EMPTY_CATCH = re.compile(r"catch\s*(?:\([^)]*\))?\s*\{(?:\s|//[^\n]*|/\*.*?\*/)*\}", re.S)
IGNORED_GO_ERR = re.compile(r"if\s+err\s*!=\s*nil\s*\{\s*\}")


def scan_by_lines(path, source, style, brace_functions):
    """Heuristic versions of all four scans for non-Python files."""
    lines = source.splitlines()
    results = comment_spans(path, lines, comment_lines_for(lines, style), set(), "heuristic")
    if brace_functions:
        results += function_lengths(path, lines)
    # One weak-name finding per name per line, whichever pattern saw it.
    reported = set()
    for number, raw in enumerate(lines, start=1):
        code = strip_strings(raw)
        for pattern in WEAK_DECLARATIONS:
            for match in pattern.finditer(code):
                if (match.group(1), number) not in reported:
                    reported.add((match.group(1), number))
                    results.append(finding(path, number, "weak-name", match.group(1), "heuristic"))
    # Silent catches can span lines, so these patterns run on the whole file.
    for pattern, label in ((EMPTY_CATCH, "empty catch block swallows the error"),
                           (IGNORED_GO_ERR, "err is checked and then ignored")):
        for match in pattern.finditer(source):
            line = source.count("\n", 0, match.start()) + 1
            results.append(finding(path, line, "silent-except", label, "heuristic"))
    return results


# ------------------------------------------------------------------ main ---

def expand(inputs):
    """Turn files and directories into a list of files to scan, skipping
    vendored and generated trees the reviewer did not write."""
    files = []
    for item in inputs:
        # A directory means every file under it; a plain path is taken as given.
        if os.path.isdir(item):
            for root, dirs, names in os.walk(item):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
                files += [os.path.join(root, n) for n in sorted(names)]
        else:
            files.append(item)
    return files


def scan_file(path):
    """Return (findings, skip_reason); skip_reason is None when scanned."""
    ext = os.path.splitext(path)[1].lower()
    if ext != ".py" and ext not in COMMENT_STYLE:
        return [], "no rules for {} files".format(ext or "extensionless")
    # Undecodable bytes mean a binary or an odd encoding: skip, do not crash.
    try:
        with open(path, encoding="utf-8") as source_file:
            source = source_file.read()
    except (OSError, UnicodeDecodeError) as err:
        return [], "could not read ({})".format(err)
    if ext == ".py":
        return scan_python(path, source), None
    return scan_by_lines(path, source, COMMENT_STYLE[ext], ext in BRACE_FUNCTIONS), None


def print_text(findings, skipped, scanned):
    """One line per finding, in punch-list order, then a one-line summary."""
    for item in findings:
        where = "{}:{}".format(item["file"], item["line"])
        if item["end_line"] != item["line"]:
            where += "-{}".format(item["end_line"])
        marker = "  [heuristic]" if item["method"] == "heuristic" else ""
        print("{}  {}  {}{}".format(where, item["rule"], item["detail"], marker))
    # List what the scan never saw, so nobody mistakes silence for a pass.
    for item in skipped:
        print("skipped {}: {}".format(item["file"], item["reason"]))
    print("{} finding(s) in {} scanned file(s); {} skipped".format(len(findings), scanned, len(skipped)))


def main(argv=None):
    # All input arrives as arguments or stdin: an agent cannot answer prompts.
    parser = argparse.ArgumentParser(
        description="Enforced scans for /mean-review: the 10-line comment rule, "
                    "function length, weak names, and silent excepts.")
    parser.add_argument("paths", nargs="*", help="files or directories to scan")
    parser.add_argument("--stdin", action="store_true", help="also read paths from stdin, one per line")
    parser.add_argument("--json", action="store_true", help="print JSON instead of one line per finding")
    args = parser.parse_args(argv)

    # Paths come from the command line, stdin, or both (git diff --name-only).
    inputs = list(args.paths)
    if args.stdin:
        inputs += [line.strip() for line in sys.stdin if line.strip()]
    if not inputs:
        parser.print_usage(sys.stderr)
        print("error: give at least one file or directory, or pipe paths in with --stdin", file=sys.stderr)
        return 2

    findings, skipped, scanned = [], [], 0
    for path in expand(inputs):
        # A path listed by `git diff` may be a file the change deleted.
        if not os.path.exists(path):
            skipped.append({"file": path, "reason": "does not exist (deleted in the diff?)"})
            continue
        results, reason = scan_file(path)
        if reason:
            skipped.append({"file": path, "reason": reason})
            continue
        scanned += 1
        findings += results

    # Nothing scanned means the caller passed the wrong thing; say so loudly.
    if scanned == 0:
        print("error: none of the inputs could be scanned", file=sys.stderr)
        for item in skipped:
            print("  skipped {}: {}".format(item["file"], item["reason"]), file=sys.stderr)
        return 2

    # Same order as the punch list: correctness hits first, names last.
    priority = {"silent-except": 0, "10-line": 1, "fn-length": 2, "weak-name": 3}
    findings.sort(key=lambda f: (priority[f["rule"]], f["file"], f["line"]))
    if args.json:
        print(json.dumps({"scanned": scanned, "findings": findings, "skipped": skipped}, indent=2))
    else:
        print_text(findings, skipped, scanned)
    return 0


if __name__ == "__main__":
    sys.exit(main())
