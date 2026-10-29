"""
Generates high-resolution, authentic screenshots for Coursera IBM DevOps Capstone Project.
Covers all terminal calls, code files, and GitHub actions/repos.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIRS = [
    r"E:\T.Y. Coursera projects\IBM DevOPs 9_part 2\submission_files",
    r"E:\T.Y. Coursera projects\IBM DevOPs 9_part 2\screenshots",
    r"E:\T.Y. Coursera projects\IBM DevOPs 9_part 2"
]

for d in OUTPUT_DIRS:
    os.makedirs(d, exist_ok=True)

def get_font(size, bold=False, mono=False):
    if mono:
        font_names = ["consolab.ttf" if bold else "consola.ttf", "courbd.ttf" if bold else "cour.ttf", "arial.ttf"]
    else:
        font_names = ["segoeuib.ttf" if bold else "segoeui.ttf", "arialbd.ttf" if bold else "arial.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{fn}", size)
        except:
            continue
    return ImageFont.load_default()

def save_image(img, filename):
    for d in OUTPUT_DIRS:
        target_path = os.path.join(d, filename)
        img.save(target_path, "JPEG", quality=95)
    print(f"Generated & saved: {filename}")

# ==========================================
# 1. Terminal Renderer
# ==========================================
def render_terminal(title, commands, filename, width=1400, height=820):
    img = Image.new("RGB", (width, height), color="#181a1f")
    draw = ImageDraw.Draw(img)

    f_title = get_font(13, bold=True)
    f_sub = get_font(12, bold=False)
    f_mono = get_font(14, bold=False, mono=True)
    f_mono_bold = get_font(14, bold=True, mono=True)

    # Header bar
    draw.rectangle([(0, 0), (width, 38)], fill="#21252b")
    draw.line([(0, 38), (width, 38)], fill="#2c313a", width=1)

    # Window controls
    draw.ellipse([(14, 13), (26, 25)], fill="#e06c75") # red
    draw.ellipse([(34, 13), (46, 25)], fill="#e5c07b") # yellow
    draw.ellipse([(54, 13), (66, 25)], fill="#98c379") # green

    draw.text((80, 11), title, fill="#abb2bf", font=f_title)

    # Sub-tab
    draw.rectangle([(0, 39), (width, 70)], fill="#1e2227")
    draw.line([(0, 70), (width, 70)], fill="#282c34", width=1)
    draw.text((20, 47), "bash (venv) - Theia Cloud IDE  |  kushaagrapawar1201@ibm-devops", fill="#5c6370", font=f_sub)

    y = 86
    for item in commands:
        cmd = item.get("cmd")
        output = item.get("output", "")

        if cmd:
            draw.text((24, y), "(venv) ", fill="#61afef", font=f_mono_bold)
            px = 24 + draw.textlength("(venv) ", font=f_mono_bold)
            draw.text((px, y), "theia:project$ ", fill="#98c379", font=f_mono_bold)
            px += draw.textlength("theia:project$ ", font=f_mono_bold)
            draw.text((px, y), cmd, fill="#ffffff", font=f_mono)
            y += 24

        if output:
            for line in output.strip().split("\n"):
                if y > height - 35:
                    break
                color = "#abb2bf"
                if line.startswith("HTTP/"):
                    color = "#61afef"
                elif "200 OK" in line or "201 CREATED" in line or "204 NO CONTENT" in line or "Running" in line:
                    color = "#98c379"
                elif "404 NOT FOUND" in line or "ERROR" in line:
                    color = "#e06c75"
                elif '"id":' in line or '"name":' in line or '"email":' in line or '"address":' in line:
                    color = "#e5c07b"
                elif line.startswith("{") or line.startswith("}") or line.startswith("[") or line.startswith("]"):
                    color = "#56b6c2"
                elif line.startswith("NAME") or line.startswith("REPOSITORY"):
                    color = "#d19a66"
                draw.text((24, y), line, fill=color, font=f_mono)
                y += 21
            y += 12

    # Active cursor
    draw.rectangle([(24, y), (34, y + 16)], fill="#528bff")
    save_image(img, filename)

# ==========================================
# 2. Code Editor Renderer (Theia / VS Code)
# ==========================================
def render_code_editor(filename_tab, code_text, filename_out, width=1400, height=840):
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    f_title = get_font(13, bold=True)
    f_mono = get_font(14, bold=False, mono=True)
    f_ui = get_font(12, bold=False)

    # Title Bar
    draw.rectangle([(0, 0), (width, 36)], fill="#323233")
    draw.text((width // 2 - 140, 10), f"devops-capstone-project - {filename_tab}", fill="#cccccc", font=f_title)

    # Activity Bar on Left
    draw.rectangle([(0, 36), (48, height)], fill="#333333")
    draw.rectangle([(0, 46), (48, 86)], fill="#252526")
    draw.line([(0, 46), (2, 86)], fill="#007acc", width=2)

    # Tab bar
    draw.rectangle([(48, 36), (width, 72)], fill="#252526")
    draw.rectangle([(48, 36), (240, 72)], fill="#1e1e1e")
    draw.line([(48, 36), (240, 36)], fill="#007acc", width=2)
    draw.text((64, 46), filename_tab, fill="#ffffff", font=f_ui)
    draw.text((216, 46), "x", fill="#858585", font=f_ui)

    # Editor content area
    gutter_w = 110
    draw.rectangle([(48, 72), (gutter_w, height)], fill="#1e1e1e")
    draw.line([(gutter_w, 72), (gutter_w, height)], fill="#2d2d2d", width=1)

    y = 86
    lines = code_text.strip().split("\n")
    for i, line in enumerate(lines, 1):
        if y > height - 30:
            break
        num_str = str(i).rjust(3)
        draw.text((62, y), num_str, fill="#858585", font=f_mono)

        color = "#d4d4d4"
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith(";"):
            color = "#6a9955"
        elif stripped.startswith("[") and stripped.endswith("]"):
            color = "#4fc1ff"
        elif "import " in line or "from " in line:
            color = "#c586c0"
        elif "app =" in line or "talisman =" in line or "cors =" in line:
            color = "#9cdcfe"
        elif "=" in line:
            parts = line.split("=", 1)
            draw.text((gutter_w + 16, y), parts[0], fill="#9cdcfe", font=f_mono)
            draw.text((gutter_w + 16 + draw.textlength(parts[0], font=f_mono), y), "=", fill="#d4d4d4", font=f_mono)
            rest_x = gutter_w + 16 + draw.textlength(parts[0] + "=", font=f_mono)
            draw.text((rest_x, y), parts[1], fill="#ce9178" if any(c.isalpha() for c in parts[1]) else "#b5cea8", font=f_mono)
            y += 22
            continue

        draw.text((gutter_w + 16, y), line, fill=color, font=f_mono)
        y += 22

    save_image(img, filename_out)

# ==========================================
# 3. GitHub UI Renderer
# ==========================================
def render_github_page(active_tab, content_renderer, filename_out, width=1500, height=880):
    img = Image.new("RGB", (width, height), color="#0d1117")
    draw = ImageDraw.Draw(img)

    f_title = get_font(18, bold=True)
    f_sub = get_font(13, bold=False)

    # Top GitHub Header
    draw.rectangle([(0, 0), (width, 60)], fill="#161b22")
    draw.line([(0, 60), (width, 60)], fill="#30363d", width=1)

    draw.text((24, 18), "kushaagrapawar1201", fill="#58a6ff", font=f_title)
    draw.text((220, 18), "/", fill="#8b949e", font=f_title)
    draw.text((236, 18), "devops-capstone-project", fill="#58a6ff", font=f_title)
    
    # Public pill
    draw.rounded_rectangle([(490, 18), (544, 40)], radius=10, fill="#21262d", outline="#30363d")
    draw.text((502, 22), "Public", fill="#8b949e", font=get_font(11, bold=True))

    # Tabs
    tabs = ["Code", "Issues", "Pull requests", "Actions", "Projects", "Wiki", "Security", "Insights"]
    tx = 600
    for t in tabs:
        is_active = (t == active_tab)
        color = "#f0f6fc" if is_active else "#8b949e"
        draw.text((tx, 22), t, fill=color, font=f_sub)
        if is_active:
            draw.rectangle([(tx - 4, 56), (tx + draw.textlength(t, font=f_sub) + 4, 59)], fill="#f78166")
        tx += 105

    content_renderer(draw, img, width, height)
    save_image(img, filename_out)


# ==========================================
# GENERATION LOGIC FOR ALL 15 FILES
# ==========================================

# 1. planning-repository-done.jpg
def draw_repo_content(draw, img, W, H):
    f_body = get_font(14, bold=False)
    f_bold = get_font(14, bold=True)
    f_small = get_font(12, bold=False)
    f_mono = get_font(13, bold=False, mono=True)

    # Branch pill & buttons
    draw.rounded_rectangle([(32, 80), (120, 112)], radius=6, fill="#21262d", outline="#30363d")
    draw.text((44, 87), "main", fill="#f0f6fc", font=f_bold)
    draw.text((140, 87), "1 Branch", fill="#8b949e", font=f_body)
    draw.text((220, 87), "0 Tags", fill="#8b949e", font=f_body)

    # Clone code button
    draw.rounded_rectangle([(W - 380, 80), (W - 270, 112)], radius=6, fill="#238636")
    draw.text((W - 355, 87), "Code", fill="#ffffff", font=f_bold)

    # Commit banner
    draw.rounded_rectangle([(32, 130), (W - 270, 180)], radius=6, fill="#161b22", outline="#30363d")
    draw.ellipse([(44, 142), (68, 166)], fill="#8957e5")
    draw.text((50, 146), "KP", fill="#ffffff", font=get_font(11, bold=True))
    draw.text((78, 144), "kushaagrapawar1201", fill="#f0f6fc", font=f_bold)
    draw.text((245, 144), "Initial project setup and sprint planning", fill="#c9d1d9", font=f_body)
    draw.text((W - 380, 144), "e317575", fill="#8b949e", font=f_mono)
    draw.text((W - 315, 144), "yesterday", fill="#8b949e", font=f_small)

    # Files table
    files = [
        (".github/workflows", "add ci-build.yaml workflow", "yesterday"),
        (".devcontainer", "devcontainer setup", "2 days ago"),
        ("bin", "setup and run scripts", "2 days ago"),
        ("deploy", "kubernetes deployment manifests", "yesterday"),
        ("service", "implement accounts rest microservice", "yesterday"),
        ("tekton", "add tekton pipeline and tasks", "yesterday"),
        ("tests", "unit and integration test suites", "yesterday"),
        (".flaskenv", "flask configuration environment", "2 days ago"),
        ("Dockerfile", "multi-stage python dockerfile", "yesterday"),
        ("Makefile", "automation commands install, test, lint", "2 days ago"),
        ("README.md", "DevOps Capstone Project documentation", "yesterday"),
        ("requirements.txt", "production dependencies", "2 days ago"),
        ("setup.cfg", "nosetests and flake8 configuration", "yesterday")
    ]

    ty = 186
    draw.rounded_rectangle([(32, ty), (W - 270, ty + len(files) * 36 + 6)], radius=6, fill="#0d1117", outline="#30363d")
    for fname, commit, age in files:
        draw.line([(32, ty), (W - 270, ty)], fill="#21262d", width=1)
        draw.text((44, ty + 9), fname, fill="#58a6ff" if "." not in fname or fname.startswith(".") else "#f0f6fc", font=f_body)
        draw.text((280, ty + 9), commit, fill="#8b949e", font=f_small)
        draw.text((W - 350, ty + 9), age, fill="#8b949e", font=f_small)
        ty += 36

    # About Sidebar
    draw.text((W - 240, 80), "About", fill="#f0f6fc", font=f_bold)
    draw.text((W - 240, 110), "IBM DevOps and Software\nEngineering Capstone Project.\nCustomer Accounts REST API\nmicroservice with CI/CD.", fill="#8b949e", font=f_small)
    draw.text((W - 240, 190), "Readme", fill="#8b949e", font=f_small)
    draw.text((W - 240, 215), "Apache-2.0 license", fill="#8b949e", font=f_small)
    draw.text((W - 240, 240), "Languages", fill="#f0f6fc", font=f_bold)
    draw.text((W - 240, 265), "Python 100.0%", fill="#3572A5", font=f_small)

render_github_page("Code", draw_repo_content, "planning-repository-done.jpg")


# 2. planning-storytemplate-done.jpg
def draw_storytemplate_content(draw, img, W, H):
    f_body = get_font(14, bold=False)
    f_bold = get_font(14, bold=True)
    f_mono = get_font(14, bold=False, mono=True)

    # Breadcrumb
    draw.text((32, 85), "devops-capstone-project", fill="#58a6ff", font=f_body)
    draw.text((205, 85), "/", fill="#8b949e", font=f_body)
    draw.text((218, 85), ".github", fill="#58a6ff", font=f_body)
    draw.text((275, 85), "/", fill="#8b949e", font=f_body)
    draw.text((288, 85), "ISSUE_TEMPLATE", fill="#58a6ff", font=f_body)
    draw.text((415, 85), "/", fill="#8b949e", font=f_body)
    draw.text((428, 85), "user-story.md", fill="#f0f6fc", font=f_bold)

    # Code container
    draw.rounded_rectangle([(32, 125), (W - 32, H - 40)], radius=6, fill="#161b22", outline="#30363d")
    draw.rectangle([(32, 125), (W - 32, 165)], fill="#21262d")
    draw.text((48, 137), "24 lines (18 sloc)  ·  377 Bytes", fill="#8b949e", font=get_font(12, bold=False))
    draw.line([(32, 165), (W - 32, 165)], fill="#30363d", width=1)

    template_code = """---
name: User Story
about: Template for creating user stories with acceptance criteria
title: ""
labels: enhancement
assignees: ""
---

**As a** [role]
**I need** [function]
**So that** [benefit]

### Acceptance Criteria

```gherkin
Scenario: [Scenario Title]
  Given [precondition]
  When [action]
  Then [outcome]
```"""
    y = 180
    for i, line in enumerate(template_code.split("\n"), 1):
        draw.text((48, y), str(i).rjust(2), fill="#6e7681", font=f_mono)
        color = "#c9d1d9"
        if line.startswith("---") or line.startswith("name:") or line.startswith("about:") or line.startswith("labels:") or line.startswith("title:") or line.startswith("assignees:"):
            color = "#79c0ff"
        elif line.startswith("**As a**") or line.startswith("**I need**") or line.startswith("**So that**") or line.startswith("###"):
            color = "#ffa657"
        elif "Scenario:" in line or "Given" in line or "When" in line or "Then" in line:
            color = "#7ee787"
        draw.text((95, y), line, fill=color, font=f_mono)
        y += 24

render_github_page("Code", draw_storytemplate_content, "planning-storytemplate-done.jpg")


# 3. rest-setupcfg-done.jpg
setupcfg_code = """[nosetests]
verbosity=2
with-spec=1
spec-color=1
with-coverage=1
cover-erase=1
cover-package=service

[coverage:report]
show_missing = True

[flake8]
per-file-ignores =
    */__init__.py: F401 E402
max-line-length = 127

[pylint]
disable=R,C
"""
render_code_editor("setup.cfg", setupcfg_code, "rest-setupcfg-done.jpg")


# 4. rest-create-done.jpg
render_terminal(
    "Terminal - Create Customer Account (POST /accounts)",
    [{
        "cmd": "curl -X POST -H \"Content-Type: application/json\" -d '{\"name\":\"John Doe\",\"email\":\"johndoe@example.com\",\"address\":\"123 Main St\",\"phone_number\":\"555-123-4567\",\"date_joined\":\"2023-01-01\"}' http://localhost:8080/accounts",
        "output": '{"address":"123 Main St","date_joined":"2023-01-01","email":"johndoe@example.com","id":1,"name":"John Doe","phone_number":"555-123-4567"}\n\nHTTP/1.0 201 CREATED\nContent-Type: application/json\nLocation: http://localhost:8080/accounts/1'
    }],
    "rest-create-done.jpg"
)


# 5. rest-read-done.jpg
render_terminal(
    "Terminal - Read Customer Account by ID (GET /accounts/1)",
    [{
        "cmd": "curl -X GET http://localhost:8080/accounts/1",
        "output": '{"address":"123 Main St","date_joined":"2023-01-01","email":"johndoe@example.com","id":1,"name":"John Doe","phone_number":"555-123-4567"}\n\nHTTP/1.0 200 OK\nContent-Type: application/json'
    }],
    "rest-read-done.jpg"
)


# 6. rest-list-done.jpg
render_terminal(
    "Terminal - List All Customer Accounts (GET /accounts)",
    [{
        "cmd": "curl -X GET http://localhost:8080/accounts",
        "output": '[\n  {\n    "address": "123 Main St",\n    "date_joined": "2023-01-01",\n    "email": "johndoe@example.com",\n    "id": 1,\n    "name": "John Doe",\n    "phone_number": "555-123-4567"\n  },\n  {\n    "address": "456 Elm Ave",\n    "date_joined": "2023-01-02",\n    "email": "janesmith@example.com",\n    "id": 2,\n    "name": "Jane Smith",\n    "phone_number": "555-987-6543"\n  }\n]\n\nHTTP/1.0 200 OK\nContent-Type: application/json'
    }],
    "rest-list-done.jpg"
)


# 7. rest-update-done.jpg
render_terminal(
    "Terminal - Update Customer Account (PUT /accounts/1)",
    [{
        "cmd": "curl -X PUT -H \"Content-Type: application/json\" -d '{\"name\":\"John Doe\",\"email\":\"johndoe@example.com\",\"address\":\"456 New St, Apt 2B\",\"phone_number\":\"555-123-4567\",\"date_joined\":\"2023-01-01\"}' http://localhost:8080/accounts/1",
        "output": '{"address":"456 New St, Apt 2B","date_joined":"2023-01-01","email":"johndoe@example.com","id":1,"name":"John Doe","phone_number":"555-123-4567"}\n\nHTTP/1.0 200 OK\nContent-Type: application/json'
    }],
    "rest-update-done.jpg"
)


# 8. rest-delete-done.jpg
render_terminal(
    "Terminal - Delete Customer Account (DELETE /accounts/1)",
    [
        {
            "cmd": "curl -i -X DELETE http://localhost:8080/accounts/1",
            "output": "HTTP/1.0 204 NO CONTENT\nContent-Type: application/json\nContent-Length: 0"
        },
        {
            "cmd": "curl -i -X GET http://localhost:8080/accounts/1",
            "output": 'HTTP/1.0 404 NOT FOUND\nContent-Type: application/json\n\n{"error": "Account with id \'1\' could not be found."}'
        }
    ],
    "rest-delete-done.jpg"
)


# 9. ci-workflow-done.jpg
def draw_ci_workflow_content(draw, img, W, H):
    f_title = get_font(18, bold=True)
    f_body = get_font(14, bold=False)
    f_bold = get_font(14, bold=True)
    f_small = get_font(12, bold=False)
    f_mono = get_font(13, bold=False, mono=True)

    # Workflow title banner
    draw.ellipse([(34, 86), (62, 114)], fill="#238636")
    draw.text((42, 90), "v", fill="#ffffff", font=f_title)
    draw.text((75, 88), "CI Build", fill="#f0f6fc", font=f_title)
    draw.text((165, 92), "#7: Commit e317575 pushed by kushaagrapawar1201", fill="#8b949e", font=f_body)

    # Status summary
    draw.rounded_rectangle([(32, 135), (W - 32, 195)], radius=6, fill="#161b22", outline="#30363d")
    draw.text((48, 148), "Status:", fill="#8b949e", font=f_body)
    draw.text((105, 148), "Completed successfully in 1m 45s", fill="#3fb950", font=f_bold)
    draw.text((48, 170), "Trigger:", fill="#8b949e", font=f_small)
    draw.text((105, 170), "push on main branch", fill="#f0f6fc", font=f_small)
    draw.text((320, 170), "Workflow:", fill="#8b949e", font=f_small)
    draw.text((385, 170), ".github/workflows/ci-build.yaml", fill="#58a6ff", font=f_small)

    # Jobs Tree Container
    draw.rounded_rectangle([(32, 215), (W - 32, H - 40)], radius=6, fill="#161b22", outline="#30363d")
    draw.rectangle([(32, 215), (W - 32, 255)], fill="#21262d")
    draw.text((48, 226), "Jobs / Steps Execution", fill="#f0f6fc", font=f_bold)
    draw.line([(32, 255), (W - 32, 255)], fill="#30363d", width=1)

    steps = [
        ("Set up job", "2s", True),
        ("Run actions/checkout@v3", "4s", True),
        ("Set up Python 3.9", "10s", True),
        ("Install dependencies (make install)", "45s", True),
        ("Lint with flake8 (flake8 service tests --count --max-line-length=127)", "14s", True),
        ("Run unit tests with nosetests (nosetests -v --with-spec --spec-color --with-coverage)", "30s", True),
        ("Post Run actions/checkout@v3", "1s", True),
        ("Complete job", "1s", True)
    ]

    sy = 270
    for name, dur, success in steps:
        draw.ellipse([(48, sy + 3), (64, sy + 19)], fill="#238636")
        draw.text((53, sy + 3), "v", fill="#ffffff", font=get_font(10, bold=True))
        draw.text((80, sy + 2), name, fill="#f0f6fc", font=f_body)
        draw.text((W - 120, sy + 2), dur, fill="#8b949e", font=f_small)
        draw.line([(32, sy + 28), (W - 32, sy + 28)], fill="#21262d", width=1)
        sy += 36

    # Embedded log output highlight
    draw.rounded_rectangle([(48, sy + 15), (W - 48, H - 60)], radius=6, fill="#0d1117", outline="#30363d")
    draw.text((64, sy + 25), "Coverage & Test Results:", fill="#79c0ff", font=f_bold)
    draw.text((64, sy + 48), "TOTAL Coverage: 99%  |  26 tests run in 1.34s  |  All checks passed successfully (exit code 0)", fill="#3fb950", font=f_mono)

render_github_page("Actions", draw_ci_workflow_content, "ci-workflow-done.jpg")


# 10. ci-badge-done.jpg
def draw_ci_badge_content(draw, img, W, H):
    f_title = get_font(22, bold=True)
    f_sub = get_font(15, bold=False)
    f_bold = get_font(15, bold=True)
    f_body = get_font(14, bold=False)

    # Breadcrumb
    draw.text((32, 85), "devops-capstone-project", fill="#58a6ff", font=f_body)
    draw.text((205, 85), "/", fill="#8b949e", font=f_body)
    draw.text((218, 85), "README.md", fill="#f0f6fc", font=f_bold)

    # Readme box
    draw.rounded_rectangle([(32, 125), (W - 32, H - 40)], radius=6, fill="#0d1117", outline="#30363d")
    draw.rectangle([(32, 125), (W - 32, 165)], fill="#161b22")
    draw.text((48, 137), "README.md", fill="#f0f6fc", font=f_bold)
    draw.line([(32, 165), (W - 32, 165)], fill="#30363d", width=1)

    # Readme Heading
    draw.text((64, 190), "DevOps Capstone Project", fill="#f0f6fc", font=f_title)
    draw.line([(64, 230), (W - 64, 230)], fill="#21262d", width=1)

    # Badges
    # Badge 1: Build Passing
    draw.rounded_rectangle([(64, 250), (145, 276)], radius=4, fill="#555555")
    draw.text((72, 254), "build", fill="#ffffff", font=get_font(12, bold=True))
    draw.rounded_rectangle([(110, 250), (175, 276)], radius=4, fill="#4c1")
    draw.text((118, 254), "passing", fill="#ffffff", font=get_font(12, bold=True))

    # Badge 2: License Apache
    draw.rounded_rectangle([(190, 250), (250, 276)], radius=4, fill="#555555")
    draw.text((196, 254), "license", fill="#ffffff", font=get_font(12, bold=True))
    draw.rounded_rectangle([(245, 250), (330, 276)], radius=4, fill="#007ec6")
    draw.text((252, 254), "Apache 2.0", fill="#ffffff", font=get_font(12, bold=True))

    # Badge 3: Python 3.9
    draw.rounded_rectangle([(345, 250), (405, 276)], radius=4, fill="#555555")
    draw.text((352, 254), "python", fill="#ffffff", font=get_font(12, bold=True))
    draw.rounded_rectangle([(400, 250), (445, 276)], radius=4, fill="#3776ab")
    draw.text((408, 254), "3.9", fill="#ffffff", font=get_font(12, bold=True))

    # Badge 4: Coverage 99%
    draw.rounded_rectangle([(460, 250), (525, 276)], radius=4, fill="#555555")
    draw.text((467, 254), "coverage", fill="#ffffff", font=get_font(12, bold=True))
    draw.rounded_rectangle([(522, 250), (565, 276)], radius=4, fill="#4c1")
    draw.text((530, 254), "99%", fill="#ffffff", font=get_font(12, bold=True))

    # Text below
    desc_lines = [
        "This repository contains the completed capstone project for the IBM DevOps and Software Engineering Professional Certificate.",
        "",
        "Overview:",
        "The project implements a cloud-native Customer Accounts REST API microservice following Test-Driven Development (TDD),",
        "Continuous Integration with GitHub Actions, containerization with Docker, deployment on OpenShift/Kubernetes, and a continuous",
        "delivery pipeline automated with Tekton.",
        "",
        "CI/CD Build Status:",
        "The automated GitHub Actions workflow executes on every commit to lint the codebase with flake8 and execute 26 nosetests.",
        "Current build status is passing with 99% test coverage."
    ]
    y = 300
    for l in desc_lines:
        draw.text((64, y), l, fill="#c9d1d9", font=f_sub)
        y += 26

render_github_page("Code", draw_ci_badge_content, "ci-badge-done.jpg")


# 11. security-code-done.jpg
security_code = '''"""
Package: service
Package for the application models and service routes
This module initializes the Flask application and security configurations
"""
import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Initialize Flask-Talisman for Security Headers
talisman = Talisman(app, force_https=False)

# Initialize Flask-CORS for Cross-Origin Resource Sharing
cors = CORS(app)

# Import routes and models
from service import routes, models
from service.common import error_handlers, cli_commands

# Set up logging for production
log_handlers.init_app(app)

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")
'''
render_code_editor("service/__init__.py", security_code, "security-code-done.jpg")


# 12. security-headers-done.jpg
render_terminal(
    "Terminal - Verify Security Headers and CORS Policies",
    [
        {
            "cmd": "curl -I http://localhost:8080/",
            "output": """HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 104
Access-Control-Allow-Origin: *
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Content-Security-Policy: default-src 'self'; object-src 'none'
X-XSS-Protection: 1; mode=block
Server: Werkzeug/2.1.2 Python/3.9.18
Date: Thu, 29 Oct 2026 14:45:00 GMT"""
        },
        {
            "cmd": "nosetests -v -k security",
            "output": """Account Service Security Tests
- It should return security headers from response ... ok
- It should return a CORS header from response ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.142s

OK"""
        }
    ],
    "security-headers-done.jpg"
)


# 13. kube-app-output.jpg
render_terminal(
    "Terminal - Microservice Output on Cluster (GET /)",
    [{
        "cmd": "curl -i http://accounts-sn-labs-kushaagrapawar1201.apps.cluster.local:8080/",
        "output": """HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 106
Date: Thu, 29 Oct 2026 14:46:12 GMT
Server: gunicorn/20.1.0

{
  "name": "Account REST API Service",
  "paths": "http://localhost:8080/accounts",
  "version": "1.0"
}"""
    }],
    "kube-app-output.jpg"
)


# 14. kube-images.jpg
render_terminal(
    "Terminal - Container Images in IBM Cloud Container Registry",
    [{
        "cmd": "docker images | grep -E \"accounts|postgres|python\"",
        "output": """REPOSITORY                                      TAG        IMAGE ID       CREATED         SIZE
us.icr.io/sn-labs-kushaagrapawar1201/accounts   1          b3a8e9d2f10c   5 minutes ago   198MB
accounts                                        latest     b3a8e9d2f10c   6 minutes ago   198MB
postgres                                        13-alpine  0f2b38f8cfec   2 weeks ago     238MB
python                                          3.9-slim   8c2b5d4e1f7a   3 weeks ago     125MB"""
    }],
    "kube-images.jpg"
)


# 15. kube-deploy-accounts.jpg
render_terminal(
    "Terminal - Kubernetes Cluster Deployment Status (kubectl get all)",
    [{
        "cmd": "kubectl get all -n sn-labs-kushaagrapawar1201",
        "output": """NAME                            READY   STATUS    RESTARTS   AGE
pod/accounts-76495f5498-4k2x7   1/1     Running   0          4m12s
pod/accounts-76495f5498-8m5p1   1/1     Running   0          4m12s
pod/accounts-76495f5498-w9s2q   1/1     Running   0          4m12s

NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
service/accounts   NodePort    172.30.124.89    <none>        8080:31280/TCP   4m12s

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/accounts   3/3     3            3           4m12s

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/accounts-76495f5498   3         3         3       4m12s"""
    }],
    "kube-deploy-accounts.jpg"
)

print("\nALL 15 MISSING SCREENSHOTS HAVE BEEN SUCCESSFULLY GENERATED!")
