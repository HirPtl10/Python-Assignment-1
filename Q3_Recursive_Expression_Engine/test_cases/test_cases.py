import os
import subprocess
import sys

TEST_CASES = [
    {
        "input": "3\na = 2 + 3\nb = a * 4\nc = b - (a + 1)\nc + 10\n",
        "expected": "24"
    },
    {
        "input": "2\nx = y + 1\ny = x * 2\nx + 5\n",
        "expected": "CYCLE"
    },
    {
        "input": "0\n2 + * 3\n",
        "expected": "INVALID"
    },
    {
        "input": "4\np = 10\nq = p + 5\nr = q * 2\ns = r - 10\ns + (p * 2)\n",
        "expected": "40"
    }
]

def run_all_tests():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Q3_Recursive_Expression_Engine.py"))
    
    for idx, tc in enumerate(TEST_CASES, 1):
        proc = subprocess.run([sys.executable, script_path], input=tc["input"], capture_output=True, text=True)
        actual = proc.stdout.strip()
        expected = tc["expected"].strip()
        
        print(f"--- Test Case {idx} ---")
        if actual == expected:
            print("STATUS: PASSED")
            print(f"OUTPUT: {actual}")
        else:
            print("STATUS: FAILED")
            print(f"EXPECTED: {expected}")
            print(f"ACTUAL: {actual}")

if __name__ == "__main__":
    run_all_tests()
