import json
import html
import argparse
from pathlib import Path


def e(text: str) -> str:
    """HTML-escape a string."""
    return html.escape(str(text)) if text else ""


def render_tag_tables(data: dict, data_info: dict) -> str:
    """Render the summary tables grouped by tag."""
    parts = []
    for tag, operations in data.items():
        tag_escaped = e(tag)
        rows = []
        for op in operations:
            op_escaped = e(op)
            desc = data_info.get(op, {}).get("description", "")
            rows.append(
                f'<tr>'
                f'<td><a href="#operation--{op_escaped}">{op_escaped}</a></td>'
                f'<td><p>{e(desc)}</p></td>'
                f'</tr>'
            )
        parts.append(
            f'<h3 id="tag-{tag_escaped}" class="swagger-summary-tag">Tag: {tag_escaped}</h3>\n'
            f'<table class="table table-bordered table-condensed swagger--summary">\n'
            f'<thead><tr><th>Operation</th><th>Description</th></tr></thead>\n'
            f'<tbody>\n{"".join(rows)}\n</tbody>\n</table>'
        )
    return "\n".join(parts)


def render_operation_panels(data_info: dict) -> str:
    """Render the detailed panel for each operation."""
    parameters = data_info.get("parameters", {})
    parts = []

    for key, info in data_info.items():
        if key == "parameters":
            continue

        method = key.split(" ")[0].lower() if " " in key else key.lower()
        key_escaped = e(key)

        # Tags
        tags_html = ", ".join(
            f'<a href="#tag-{e(t)}">{e(t)}</a>' for t in info.get("tags", [])
        )

        # Description
        desc = e(info.get("description", ""))

        # Arguments table
        args = info.get("arguments", [])
        args_html = ""
        if args:
            arg_rows = []
            for arg in args:
                arg_type = arg.get("type", {}).get("type", "")
                arg_rows.append(
                    f'<tr>'
                    f'<td>{e(arg.get("name", ""))}</td>'
                    f'<td>{e(arg.get("description", ""))}</td>'
                    f'<td>{e(arg_type)}</td>'
                    f'<td>{str(not arg.get("optional", False)).lower()}</td>'
                    f'</tr>'
                )
                # Expand parameter type fields
                param_def = parameters.get(arg_type, {})
                for field in param_def.get("fields", []):
                    field_type = field.get("type", {}).get("type", "")
                    arg_rows.append(
                        f'<tr>'
                        f'<td>{e(field.get("name", ""))}</td>'
                        f'<td>{e(arg_type)}</td>'
                        f'<td>{e(field_type)}</td>'
                        f'<td>{str(not field.get("optional", False)).lower()}</td>'
                        f'</tr>'
                    )

            args_html = (
                '<section class="sw-request-params">\n'
                '<table class="table">\n'
                '<thead><tr><th>Name</th><th>Description</th><th>Type</th><th>Required</th></tr></thead>\n'
                f'<tbody>\n{"".join(arg_rows)}\n</tbody>\n</table>\n</section>'
            )

        parts.append(
            f'<div id="operation--{key_escaped}" class="swagger--panel-operation-{e(method)} panel">\n'
            f'<div class="panel-heading">\n'
            f'<h3 class="panel-title"><strong>{key_escaped}</strong></h3>\n'
            f'Tags: {tags_html}\n'
            f'</div>\n'
            f'<div class="panel-body">\n'
            f'<section class="sw-operation-description"><p>{desc}</p></section>\n'
            f'{args_html}\n'
            f'</div>\n</div>'
        )

    return "\n".join(parts)


def generate(input_dir: Path, version: str):
    print(f"Patch {version}")
    data_path = input_dir / "data.json"
    data_info_path = input_dir / "data_info.json"

    print(f"Reading {data_path} ...")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Reading {data_info_path} ...")
    with open(data_info_path, "r", encoding="utf-8") as f:
        data_info = json.load(f)

    print("Rendering tag tables ...")
    tag_tables = render_tag_tables(data, data_info)

    print("Rendering operation panels ...")
    panels = render_operation_panels(data_info)

    html_out = f"""\
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>LCU API Docs</title>
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
<div class="container">
<h1>League of Legends LCU API Docs</h1>
<p>Client Version: {e(version)}</p>
<a href="https://github.com/KebsCS/lcu-and-riotclient-api">GitHub repository</a>
| <a href="https://lcu.kebs.dev/swagger.html">Original Swagger</a>
<div id="output">
{tag_tables}
{panels}
</div>
</div>
</body>
</html>"""

    output_file = input_dir / "index.html"
    print(f"Writing {output_file} ...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_out)

    size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"Done! Generated {output_file} ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Generate static LCU API docs")
    parser.add_argument(
        "-i", "--input-dir",
        type=Path,
        default=Path("lcu"),
        help="Directory containing data.json and data_info.json (default: lcu)",
    )
    parser.add_argument(
        "-v", "--version",
        default="26.05",
        help="Client version string",
    )
    args = parser.parse_args()

    generate(args.input_dir, args.version)


if __name__ == "__main__":
    main()
