import os
import subprocess
import sys

TEST_CASES = [
    {
        "input": "x = 10\nx + 5\nx / 0\n3 ** 2\nquit\n",
        "expected": "15\nDivisionByZeroError\nUnsupportedOperatorError"
    },
    {
        "input": "a = 20\nb = 4\na / b\na % b\nquit\n",
        "expected": "5\n0"
    },
    {
        "input": "y + 10\nquit\n",
        "expected": "UnknownVariableError"
    },
    {
        "input": "val = 15\nval * 3\nval - 5\n100 + 200\nquit\n",
        "expected": "45\n10\n300"
    }
]

def run_all_tests():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Q7_Interactive_Formula_Validator.py"))
    
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
