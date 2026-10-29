import os

REQUIRED_FILES = [
    # Task 1
    "planning-repository-done.jpg",
    "planning-storytemplate-done.jpg",
    "planning-userstories-done.jpg",
    "planning-productbacklog-done.jpg",
    "planning-labels-done.jpg",
    "planning-kanban-done.jpg",
    # Task 2
    "rest-setupcfg-done.jpg",
    "rest-techdebt-done.jpg",
    "read-accounts.jpg",
    "list-accounts.jpg",
    "update-accounts.jpg",
    "delete-accounts.jpg",
    "rest-create-done.jpg",
    "rest-read-done.jpg",
    "rest-list-done.jpg",
    "rest-update-done.jpg",
    "rest-delete-done.jpg",
    # Task 3
    "sprint2-plan.jpg",
    "ci-workflow-done.jpg",
    "ci-badge-done.jpg",
    "ci-kanban-done.jpg",
    "security-code-done.jpg",
    "security-headers-done.jpg",
    "security-kanban-done.jpg",
    # Task 4
    "sprint3-plan.jpg",
    "kube-app-output.jpg",
    "kube-docker-done.jpg",
    "kube-images.jpg",
    "kube-deploy-accounts.jpg",
    "kube-kubernetes-done.jpg",
    # Task 5
    "pipelinerun.txt",
    "cd-pipeline-done.jpg"
]

sub_dir = "submission_files"
existing = os.listdir(sub_dir)

print(f"Checking {len(REQUIRED_FILES)} required items in {sub_dir}:\n")
missing = []
present = []
for req in REQUIRED_FILES:
    if req in existing:
        sz = os.path.getsize(os.path.join(sub_dir, req))
        present.append((req, sz))
        print(f"  [OK] {req} ({sz} bytes)")
    else:
        # Check if there is a version without .jpg or .png
        base = os.path.splitext(req)[0]
        alt_matches = [f for f in existing if f.startswith(base)]
        missing.append((req, alt_matches))
        print(f"  [MISSING] {req} -> alternate in folder: {alt_matches}")

print(f"\nSummary: {len(present)} present, {len(missing)} missing.")
