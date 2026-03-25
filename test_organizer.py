import os
import shutil
import tempfile
import random
import string
import contextlib
import io
from organizer import organize_folder, undo

EXTENSIONS = [".jpg", ".txt", ".py", ".pdf", ".png"]

def random_name(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def setup_test_dir():
    temp_dir = tempfile.mkdtemp()

    for _ in range(10):  # Create 10 random files
        name = random_name()
        ext = random.choice(EXTENSIONS)
        filename = name + ext
        open(os.path.join(temp_dir, filename), "w").close()

    return temp_dir

def test_organize_and_undo():
    folder = setup_test_dir()
    try:
        before = set(os.listdir(folder))

        # Dry-run should not change anything
        organize_folder(folder, dry_run=True)
        assert set(os.listdir(folder)) == before, "Dry-run mutated state"

        # Actual run
        organize_folder(folder)
        undo(folder)

        after = set(os.listdir(folder))

        assert before == after, f"Mismatch!\nBefore: {before}\nAfter: {after}"

    finally:
        shutil.rmtree(folder)

if __name__ == "__main__":
    for i in range(5):
        print(f"Run {i+1}: ", end="")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                test_organize_and_undo()
            print("PASS")
        except AssertionError as e:
            print("FAIL")
            print(e)
            
