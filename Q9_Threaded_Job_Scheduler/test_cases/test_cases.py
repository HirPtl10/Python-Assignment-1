import os
import subprocess
import sys

TEST_CASES = [
    {
        "input": "2 3\n0 J1 2 5 1\n1 J2 5 3 1\n2 J3 2 2 1\n",
        "expected": "J1 W1 0 5\nJ2 W2 1 4\nJ3 W2 4 6\nAVG_WAIT 0.67"
    },
    {
        "input": "1 2\n0 JOB1 10 3 1\n0 JOB2 5 2 1\n",
        "expected": "JOB1 W1 0 3\nJOB2 W1 3 5\nAVG_WAIT 1.50"
    },
    {
        "input": "3 3\n0 T1 1 5 1\n0 T2 1 5 1\n0 T3 1 5 1\n",
        "expected": "T1 W1 0 5\nT2 W2 0 5\nT3 W3 0 5\nAVG_WAIT 0.00"
    },
    {
        "input": "2 4\n0 P1 1 2 1\n0 P2 10 4 1\n1 P3 20 2 1\n2 P4 5 1 1\n",
        "expected": "P1 W2 0 2\nP2 W1 0 4\nP3 W2 2 4\nP4 W1 4 5\nAVG_WAIT 0.75"
    }
]

def run_all_tests():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Q9_Threaded_Job_Scheduler.py"))
    
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
