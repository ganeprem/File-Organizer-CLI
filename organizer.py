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

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            category = get_category(item)
            target_dir = os.path.join(folder_path, category)

            os.makedirs(target_dir, exist_ok=True)
            shutil.move(item_path, os.path.join(target_dir, item))

    print("Organization complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files by type")
    parser.add_argument("path", help="Path to the folder")

    args = parser.parse_args()
    organize_folder(args.path)
