import os
import shutil
import tempfile
from organizer import organize_folder, undo

def setup_test_dir():
    temp_dir = tempfile.mkdtemp()

    # create sample files
    open(os.path.join(temp_dir, "a.jpg"), "w").close()
    open(os.path.join(temp_dir, "b.txt"), "w").close()
    open(os.path.join(temp_dir, "c.py"), "w").close()

    return temp_dir

def test_organize_and_undo():
    folder = setup_test_dir()

    print("Before:", os.listdir(folder))

    organize_folder(folder)
    print("After organize:", os.listdir(folder))

    undo(folder)
    print("After undo:", os.listdir(folder))

    shutil.rmtree(folder)

if __name__ == "__main__":
    test_organize_and_undo()
