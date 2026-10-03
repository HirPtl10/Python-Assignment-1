import os
import subprocess
import sys

TEST_CASES = [
    {
        "input": "3\nA 1000\nB 200\nC 0\n5\nTRANSFER A B 300\nBATCH_BEGIN\nWITHDRAW B 1000\nDEPOSIT C 50\nBATCH_END\n",
        "expected": "FAILED 1\nA 700\nB 500\nC 0"
    },
    {
        "input": "2\nX 500\nY 500\n4\nBATCH_BEGIN\nTRANSFER X Y 200\nDEPOSIT Y 100\nBATCH_END\n",
        "expected": "X 300\nY 800"
    },
    {
        "input": "1\nACC1 100\n3\nWITHDRAW ACC1 150\nDEPOSIT ACC1 50\nWITHDRAW ACC1 100\n",
        "expected": "ACC1 50"
    },
    {
        "input": "3\nA 100\nB 100\nC 100\n8\nBATCH_BEGIN\nTRANSFER A B 50\nWITHDRAW B 500\nBATCH_END\nBATCH_BEGIN\nTRANSFER B C 50\nDEPOSIT A 50\nBATCH_END\n",
        "expected": "FAILED 1\nA 150\nB 50\nC 150"
    }
]

def run_all_tests():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Q5_Bank_Settlement_System.py"))
    
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
