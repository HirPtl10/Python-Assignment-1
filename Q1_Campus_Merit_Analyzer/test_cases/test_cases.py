import os
import subprocess
import sys

TEST_CASES = [
    {
        "input": "5 2 3\n2201 Asha 5 8.90 90 82 75\n2202 Bharat 5 8.90 88 95 70\n2203 Chaitra 3 9.10 91 88 92\n2204 Dev 5 7.80 76 80 85\n2205 Esha 3 9.10 91 90 88\n",
        "expected": "Semester 3: 2203 2205\nSemester 5: 2202 2201\nS1: 2203 2205\nS2: 2202\nS3: 2203"
    },
    {
        "input": "3 1 1\n101 Alice 1 9.5 95\n102 Bob 2 8.0 80\n103 Charlie 3 9.8 98\n",
        "expected": "Semester 1: 101\nSemester 2: 102\nSemester 3: 103\nS1: 103"
    },
    {
        "input": "4 2 2\n2209 Zara 4 9.00 85 85\n2201 Alex 4 9.00 85 85\n2205 Bella 4 9.00 85 85\n2203 David 4 9.00 85 85\n",
        "expected": "Semester 4: 2201 2203\nS1: 2201 2203 2205 2209\nS2: 2201 2203 2205 2209"
    },
    {
        "input": "4 5 2\n3001 John 6 7.50 60 70\n3002 Emma 6 8.50 90 80\n3003 Liam 7 9.20 95 95\n3004 Olivia 7 9.20 95 90\n",
        "expected": "Semester 6: 3002 3001\nSemester 7: 3003 3004\nS1: 3003 3004\nS2: 3003"
    }
]

def run_all_tests():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Q1_Campus_Merit_Analyzer.py"))
    
    for idx, tc in enumerate(TEST_CASES, 1):
        proc = subprocess.run([sys.executable, script_path], input=tc["input"], capture_output=True, text=True)
        actual = proc.stdout.strip()
        expected = tc["expected"].strip()
        
        print(f"--- Test Case {idx} ---")
        if actual == expected:
            print("STATUS: PASSED")
            print("OUTPUT:\n" + actual)
        else:
            print("STATUS: FAILED")
            print("EXPECTED:\n" + expected)
            print("ACTUAL:\n" + actual)

if __name__ == "__main__":
    run_all_tests()
