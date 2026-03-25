import os
import shutil
import argparse

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".txt", ".docx"],
    "Code": [".py", ".cpp", ".js", ".java"]
}

def get_category(filename):
    for category, extensions in CATEGORIES.items():
        if any(filename.lower().endswith(ext) for ext in extensions):
            return category
    return "Others"

def organize_folder(folder_path, dry_run = False):
    if not os.path.isdir(folder_path):
        print("Invalid directory")
        return
    count = {}

    for item in os.listdir(folder_path):

        if item.startswith(".") or item in CATEGORIES or item == "Others":
            continue

        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            category = get_category(item)
            count[category] = count.get(category, 0) + 1
            target_dir = os.path.join(folder_path, category)

            os.makedirs(target_dir, exist_ok=True)
            move_file(item_path, os.path.join(target_dir, item), dry_run)

    print("Organization complete.")
    for category in sorted(count):
        print(f"{category}: {count[category]} moved")


def undo(folder_path, dry_run = False):
    count = 0
    for category in list(CATEGORIES.keys()) + ["Others"]:
        category_path = os.path.join(folder_path, category)
        
        if os.path.isdir(category_path):
            for file in os.listdir(category_path):
                src = os.path.join(category_path, file)
                dst = os.path.join(folder_path, file)
                move_file(src, dst, dry_run)
                count += 1
                
            # remove empty folder
            if not dry_run and not os.listdir(category_path):
                os.rmdir(category_path)
    print(f"{count} files moved.")


def move_file(src, dst, dry_run):
    if os.path.exists(dst):
        print(f"Skipping {src}, destination exists: {dst}")
        return

    if dry_run:
        print(f"Would move {src} -> {dst}")
    else:
        shutil.move(src, dst)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files by type")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "command", 
        nargs="?", 
        default = "organize", 
        choices = ["organize", "undo"]
    )
    parser.add_argument("path", help="Path to the folder")

    args = parser.parse_args()

    if args.command == "organize":
        organize_folder(args.path, dry_run = args.dry_run)
    elif args.command == "undo":
        undo(args.path, dry_run = args.dry_run)
