import os
import shutil
import sys
import argparse

def undo(folder_path):
    for category in ["Images", "Documents", "Code", "Others"]:
        category_path = os.path.join(folder_path, category)
            
        if os.path.isdir(category_path):
            for file in os.listdir(category_path):
                src = os.path.join(category_path, file)
                dst = os.path.join(folder_path, file)
                
                shutil.move(src, dst)     

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the folder")
    args = parser.parse_args()
    undo(args.path)
    
