import os
import shutil
import subprocess
import sys

def run_all_tests():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Q8_Compressed_Log_Index.py"))
    
    test_dir = os.path.join(os.path.dirname(__file__), "temp_logs")
    zip_path = os.path.join(os.path.dirname(__file__), "temp_archive.zip")

    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir, exist_ok=True)

    with open(os.path.join(test_dir, "app.log"), "w") as f:
        f.write("ERROR Database connection failed\nINFO Retrying connection\n")
    with open(os.path.join(test_dir, "sys.log"), "w") as f:
        f.write("INFO System booted successfully\nWARNING Low memory\n")

    try:
        # Test Case 1: BUILD mode
        proc1 = subprocess.run([sys.executable, script_path, "BUILD", test_dir, zip_path], capture_output=True, text=True)
        print("--- Test Case 1 (BUILD Mode) ---")
        print("STATUS: PASSED" if proc1.returncode == 0 else "STATUS: FAILED")
        print("OUTPUT:\n" + proc1.stdout.strip())

        # Test Case 2: SEARCH mode (error)
        proc2 = subprocess.run([sys.executable, script_path, "SEARCH", zip_path, "error"], capture_output=True, text=True)
        print("--- Test Case 2 (SEARCH 'error') ---")
        print("STATUS: PASSED" if proc2.returncode == 0 else "STATUS: FAILED")
        print("OUTPUT:\n" + proc2.stdout.strip())

        # Test Case 3: SEARCH mode (connection)
        proc3 = subprocess.run([sys.executable, script_path, "SEARCH", zip_path, "connection"], capture_output=True, text=True)
        print("--- Test Case 3 (SEARCH 'connection') ---")
        print("STATUS: PASSED" if proc3.returncode == 0 else "STATUS: FAILED")
        print("OUTPUT:\n" + proc3.stdout.strip())

        # Test Case 4: SEARCH mode (memory)
        proc4 = subprocess.run([sys.executable, script_path, "SEARCH", zip_path, "memory"], capture_output=True, text=True)
        print("--- Test Case 4 (SEARCH 'memory') ---")
        print("STATUS: PASSED" if proc4.returncode == 0 else "STATUS: FAILED")
        print("OUTPUT:\n" + proc4.stdout.strip())

    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        if os.path.exists(zip_path):
            os.remove(zip_path)

if __name__ == "__main__":
    run_all_tests()
