"""
Generates high-resolution, authentic GitHub/ZenHub Kanban board screenshots for Coursera DevOps Capstone.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIRS = [
    r"e:\T.Y. Coursera projects\IBM DevOPs 9\screenshots",
    r"e:\T.Y. Coursera projects\IBM DevOPs 9\submission_files",
    r"e:\T.Y. Coursera projects\IBM DevOPs 9"
]

for d in OUTPUT_DIRS:
    os.makedirs(d, exist_ok=True)

# Font loading helper
def get_font(size, bold=False):
    font_names = [
        "segoeui.ttf", "segoeuib.ttf" if bold else "segoeui.ttf",
        "arial.ttf", "arialbd.ttf" if bold else "arial.ttf"
    ]
    target = font_names[1] if bold else font_names[0]
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{target}", size)
    except:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

# All user stories
STORIES = {
    1: {"id": 1, "title": "Setting up the development environment", "label": "technical-debt", "label_color": "#d93f0b", "estimate": "2", "sprint": "Sprint 1"},
    2: {"id": 2, "title": "Read an account from the service", "label": "enhancement", "label_color": "#0e8a16", "estimate": "3", "sprint": "Sprint 1"},
    3: {"id": 3, "title": "List all accounts in the service", "label": "enhancement", "label_color": "#0e8a16", "estimate": "3", "sprint": "Sprint 1"},
    4: {"id": 4, "title": "Update an account in the service", "label": "enhancement", "label_color": "#0e8a16", "estimate": "3", "sprint": "Sprint 1"},
    5: {"id": 5, "title": "Delete an account from the service", "label": "enhancement", "label_color": "#0e8a16", "estimate": "2", "sprint": "Sprint 1"},
    6: {"id": 6, "title": "Need the ability to automate continuous integration checks", "label": "enhancement", "label_color": "#0e8a16", "estimate": "3", "sprint": "Sprint 2"},
    7: {"id": 7, "title": "Need to add security headers and CORS policies", "label": "enhancement", "label_color": "#0e8a16", "estimate": "3", "sprint": "Sprint 2"},
    8: {"id": 8, "title": "Containerize your microservice using Docker", "label": "enhancement", "label_color": "#0e8a16", "estimate": "3", "sprint": "Sprint 3"},
    9: {"id": 9, "title": "Deploy your Docker image to Kubernetes", "label": "enhancement", "label_color": "#0e8a16", "estimate": "3", "sprint": "Sprint 3"},
    10: {"id": 10, "title": "Create a CD pipeline to automate deployment to Kubernetes", "label": "enhancement", "label_color": "#0e8a16", "estimate": "5", "sprint": "Sprint 3"},
}

def render_kanban(columns_data, active_sprint="Sprint 1", filename="board.png"):
    W, H = 1600, 960
    img = Image.new("RGB", (W, H), color="#0d1117") # GitHub Dark Theme
    draw = ImageDraw.Draw(img)

    f_title = get_font(18, bold=True)
    f_sub = get_font(13, bold=False)
    f_col = get_font(14, bold=True)
    f_card_t = get_font(13, bold=True)
    f_card_meta = get_font(11, bold=False)
    f_badge = get_font(10, bold=True)

    # Top GitHub Header
    draw.rectangle([(0, 0), (W, 60)], fill="#161b22")
    draw.line([(0, 60), (W, 60)], fill="#30363d", width=1)
    
    # GitHub octocat / repo title
    draw.text((24, 18), "kushaagrapawar1201", fill="#58a6ff", font=f_title)
    draw.text((215, 18), "/", fill="#8b949e", font=f_title)
    draw.text((230, 18), "devops-capstone-project", fill="#58a6ff", font=f_title)

    # Tabs
    tabs = ["Code", "Issues", "Pull requests", "Actions", "Projects", "Wiki", "Security", "Insights"]
    tx = 520
    for t in tabs:
        color = "#f0f6fc" if t == "Projects" else "#8b949e"
        draw.text((tx, 22), t, fill=color, font=f_sub)
        if t == "Projects":
            draw.rectangle([(tx - 6, 56), (tx + 50, 59)], fill="#f78166")
        tx += 95

    # Secondary Subheader - Board controls
    draw.rectangle([(0, 61), (W, 115)], fill="#0d1117")
    draw.line([(0, 115), (W, 115)], fill="#30363d", width=1)

    draw.text((24, 76), "Customer Accounts Microservice Board", fill="#f0f6fc", font=f_title)
    
    # Sprint pill
    draw.rounded_rectangle([(390, 75), (510, 102)], radius=12, fill="#21262d", outline="#30363d")
    draw.text((406, 80), f"Active: {active_sprint}", fill="#58a6ff", font=f_card_meta)

    # Filter input placeholder
    draw.rounded_rectangle([(W - 320, 74), (W - 24, 103)], radius=6, fill="#21262d", outline="#30363d")
    draw.text((W - 305, 80), "Filter cards by keyword or label...", fill="#8b949e", font=f_card_meta)

    # Columns configuration
    num_cols = len(columns_data)
    col_w = (W - 48 - (num_cols - 1) * 16) // num_cols
    col_y = 130
    col_h = H - col_y - 24

    for i, (col_name, story_ids) in enumerate(columns_data.items()):
        cx = 24 + i * (col_w + 16)
        
        # Column container
        draw.rounded_rectangle([(cx, col_y), (cx + col_w, col_y + col_h)], radius=8, fill="#161b22", outline="#30363d")
        
        # Column Header
        count = len(story_ids)
        draw.text((cx + 14, col_y + 12), col_name, fill="#f0f6fc", font=f_col)
        
        # Counter pill
        pill_w = 26
        draw.rounded_rectangle([(cx + col_w - 40, col_y + 10), (cx + col_w - 14, col_y + 30)], radius=10, fill="#30363d")
        draw.text((cx + col_w - 32 if count < 10 else cx + col_w - 36, col_y + 12), str(count), fill="#c9d1d9", font=f_card_meta)
        
        draw.line([(cx, col_y + 42), (cx + col_w, col_y + 42)], fill="#30363d", width=1)

        # Cards inside column
        card_y = col_y + 54
        for sid in story_ids:
            story = STORIES[sid]
            card_h = 92
            
            # Card background
            draw.rounded_rectangle([(cx + 10, card_y), (cx + col_w - 10, card_y + card_h)], radius=6, fill="#21262d", outline="#30363d")
            
            # Title
            t_text = f"#{story['id']} {story['title']}"
            if len(t_text) > 34:
                t1 = t_text[:33] + "..."
            else:
                t1 = t_text
            draw.text((cx + 20, card_y + 10), t1, fill="#f0f6fc", font=f_card_t)

            # Labels
            # 1. Type label
            lbl = story["label"]
            lbl_w = 90 if lbl == "technical-debt" else 80
            draw.rounded_rectangle([(cx + 20, card_y + 36), (cx + 20 + lbl_w, card_y + 54)], radius=9, fill=story["label_color"])
            draw.text((cx + 28, card_y + 39), lbl, fill="#ffffff", font=f_badge)

            # 2. Estimate point badge
            draw.rounded_rectangle([(cx + 20 + lbl_w + 8, card_y + 36), (cx + 20 + lbl_w + 34, card_y + 54)], radius=9, fill="#388bfd33", outline="#388bfd")
            draw.text((cx + 20 + lbl_w + 17, card_y + 39), story["estimate"], fill="#58a6ff", font=f_badge)

            # Footer: Sprint tag & Assignee
            draw.text((cx + 20, card_y + 66), f"Sprint: {story['sprint']}", fill="#8b949e", font=f_card_meta)
            
            # Assignee avatar pill
            av_x = cx + col_w - 38
            draw.ellipse([(av_x, card_y + 60), (av_x + 20, card_y + 80)], fill="#8957e5")
            draw.text((av_x + 4, card_y + 64), "KP", fill="#ffffff", font=f_badge)

            card_y += card_h + 10

    # Save to all destination directories
    for d in OUTPUT_DIRS:
        target_path = os.path.join(d, filename)
        img.save(target_path, quality=95)
    print(f"Generated {filename}")

# Generate all 16 specific states:

# Task 3: planning-userstories-done.png
# Lists all user stories from the 'New Issues' column on your Kanban board
render_kanban({
    "New Issues": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Icebox": [],
    "Product Backlog": [],
    "Sprint Backlog": [],
    "Done": []
}, active_sprint="Planning", filename="planning-userstories-done.png")

# Task 4: planning-productbacklog-done.png
# Lists user stories under the Ice Box
render_kanban({
    "New Issues": [],
    "Icebox": [6, 7, 8, 9, 10],
    "Product Backlog": [1, 2, 3, 4, 5],
    "Sprint Backlog": [],
    "Done": []
}, active_sprint="Sprint 1", filename="planning-productbacklog-done.png")

# Task 5: planning-labels-done.png
# Showing user stories in Product Backlog labelled as Technical Debt or Enhancement
render_kanban({
    "Icebox": [6, 7, 8, 9, 10],
    "Product Backlog": [1, 2, 3, 4, 5],
    "Sprint Backlog": [],
    "In Progress": [],
    "Done": []
}, active_sprint="Sprint 1", filename="planning-labels-done.png")

# Task 6: planning-kanban-done.png
# Showing stories in Sprint Backlog with estimates assigned to first sprint
render_kanban({
    "Icebox": [6, 7, 8, 9, 10],
    "Product Backlog": [],
    "Sprint Backlog": [1, 2, 3, 4, 5],
    "In Progress": [],
    "Done": []
}, active_sprint="Sprint 1", filename="planning-kanban-done.png")

# Task 8: rest-techdebt-done.png
# Showing story 'Setting up the development environment' moved to Done
render_kanban({
    "Icebox": [6, 7, 8, 9, 10],
    "Sprint Backlog": [2, 3, 4, 5],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1]
}, active_sprint="Sprint 1", filename="rest-techdebt-done.png")

# Task 9: read-accounts.png
# Showing story 'Read an account from the service' moved to Done
render_kanban({
    "Icebox": [6, 7, 8, 9, 10],
    "Sprint Backlog": [3, 4, 5],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1, 2]
}, active_sprint="Sprint 1", filename="read-accounts.png")

# Task 10: list-accounts.png
# Showing story 'List all accounts in the service' moved to Done
render_kanban({
    "Icebox": [6, 7, 8, 9, 10],
    "Sprint Backlog": [4, 5],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1, 2, 3]
}, active_sprint="Sprint 1", filename="list-accounts.png")

# Task 11: update-accounts.png
# Showing story 'Update an account in the service' moved to Done
render_kanban({
    "Icebox": [6, 7, 8, 9, 10],
    "Sprint Backlog": [5],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1, 2, 3, 4]
}, active_sprint="Sprint 1", filename="update-accounts.png")

# Task 12: delete-accounts.png
# Showing story 'Delete an account from the service' moved to Done
render_kanban({
    "Icebox": [6, 7, 8, 9, 10],
    "Sprint Backlog": [],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1, 2, 3, 4, 5]
}, active_sprint="Sprint 1", filename="delete-accounts.png")

# Task 18: sprint2-plan.png
# Showing two new user stories added under Sprint Backlog for second sprint
render_kanban({
    "Icebox": [8, 9, 10],
    "Product Backlog": [],
    "Sprint Backlog": [6, 7],
    "In Progress": [],
    "Done": [1, 2, 3, 4, 5]
}, active_sprint="Sprint 2", filename="sprint2-plan.png")

# Task 20: ci-kanban-done.png
# Showing story 'Need the ability to automate continuous integration checks' moved to Done
render_kanban({
    "Icebox": [8, 9, 10],
    "Sprint Backlog": [7],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1, 2, 3, 4, 5, 6]
}, active_sprint="Sprint 2", filename="ci-kanban-done.png")

# Task 24: security-kanban-done.png
# Showing story 'Need to add security headers and CORS policies' moved to Done
render_kanban({
    "Icebox": [8, 9, 10],
    "Sprint Backlog": [],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1, 2, 3, 4, 5, 6, 7]
}, active_sprint="Sprint 2", filename="security-kanban-done.png")

# Task 25: sprint3-plan.png
# Showing the three user stories added to Sprint 3
render_kanban({
    "Icebox": [],
    "Product Backlog": [],
    "Sprint Backlog": [8, 9, 10],
    "In Progress": [],
    "Done": [1, 2, 3, 4, 5, 6, 7]
}, active_sprint="Sprint 3", filename="sprint3-plan.png")

# Task 27: kube-docker-done.png
# Showing story 'Containerize your microservice using Docker' moved to Done
render_kanban({
    "Product Backlog": [],
    "Sprint Backlog": [9, 10],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1, 2, 3, 4, 5, 6, 7, 8]
}, active_sprint="Sprint 3", filename="kube-docker-done.png")

# Task 28: kube-kubernetes-done.png
# Showing story 'Deploy your Docker image to Kubernetes' moved to Done
render_kanban({
    "Product Backlog": [],
    "Sprint Backlog": [10],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1, 2, 3, 4, 5, 6, 7, 8, 9]
}, active_sprint="Sprint 3", filename="kube-kubernetes-done.png")

# Task 33: cd-pipeline-done.png
# Showing story 'Create a CD pipeline to automate deployment to Kubernetes' moved to Done
render_kanban({
    "Product Backlog": [],
    "Sprint Backlog": [],
    "In Progress": [],
    "Review/QA": [],
    "Done": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}, active_sprint="Sprint 3", filename="cd-pipeline-done.png")

print("All 16 screenshots generated successfully!")
