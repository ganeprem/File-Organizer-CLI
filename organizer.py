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

def organize_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid directory")
        return
    count = {}

    for item in os.listdir(folder_path):

        if item in CATEGORIES or item == "Others":
            continue

        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            category = get_category(item)
            count[category] = count.get(category, 0) + 1
            target_dir = os.path.join(folder_path, category)

            os.makedirs(target_dir, exist_ok=True)
            shutil.move(item_path, os.path.join(target_dir, item))

    print("Organization complete.")
    for category, c in count.items():
        print(f"{category}: {c} moved")


def undo(folder_path):
    count = 0
    for category in list(CATEGORIES.keys()) + ["Others"]:
        category_path = os.path.join(folder_path, category)
        
        if os.path.isdir(category_path):
            for file in os.listdir(category_path):
                src = os.path.join(category_path, file)
                dst = os.path.join(folder_path, file)
                shutil.move(src, dst)
                count = count + 1
                
        # remove empty folder
            if not os.listdir(category_path):
                os.removedirs(category_path)
    print(f"{count} files moved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files by type")
    parser.add_argument(
        "command", 
        nargs="?", 
        default = "organize", 
        choices = ["organize", "undo"]
    )
    parser.add_argument("path", help="Path to the folder")

    args = parser.parse_args()
    if args.command == "organize":
        organize_folder(args.path)
    elif args.command == "undo":
        undo(args.path)
