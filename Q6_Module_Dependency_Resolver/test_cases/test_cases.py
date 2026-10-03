import os
import subprocess
import sys

TEST_CASES = [
    {
        "input": "4 3\ncore\ndb\nui\nauth\nui auth\nauth db\ndb core\n",
        "expected": "core db auth ui"
    },
    {
        "input": "3 3\nm1\nm2\nm3\nm1 m2\nm2 m3\nm3 m1\n",
        "expected": "CYCLE m1 m3 m2 m1"
    },
    {
        "input": "5 0\na\nb\nc\nd\ne\n",
        "expected": "a b c d e"
    },
    {
        "input": "4 4\napp\nconfig\nlogger\nutils\napp config\napp logger\nconfig utils\nlogger utils\n",
        "expected": "utils config logger app"
    }
]

def run_all_tests():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Q6_Module_Dependency_Resolver.py"))
    
    for idx, tc in enumerate(TEST_CASES, 1):
        proc = subprocess.run([sys.executable, script_path], input=tc["input"], capture_output=True, text=True)
        actual = proc.stdout.strip()
        expected = tc["expected"].strip()
        
        print(f"--- Test Case {idx} ---")
        if actual == expected:
            print("STATUS: PASSED")
            print(f"OUTPUT:\n{actual}")
        else:
            print("STATUS: FAILED")
            print(f"EXPECTED:\n{expected}")
            print(f"ACTUAL:\n{actual}")

if __name__ == "__main__":
    run_all_tests()
