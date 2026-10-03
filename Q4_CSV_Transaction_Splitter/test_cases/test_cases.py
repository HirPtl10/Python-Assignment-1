import os
import subprocess
import sys
import tempfile

TEST_CASES = [
    {
        "csv": "tid,acc,type,amount,time\nT1,A1,CREDIT,500,2026-01-01T10:00:00\nT2,A1,DEBIT,abc,2026-01-01T10:05:00\nT3,A2,DEBIT,100,2026-01-01T10:10:00\n",
        "expected": "A1 500\nA2 -100"
    },
    {
        "csv": "tid,acc,type,amount,time\nT1,ACC1,CREDIT,1000,2026-02-01T12:00:00\nT2,ACC2,CREDIT,1500,2026-02-01T12:05:00\nT3,ACC1,DEBIT,200,2026-02-01T12:10:00\n",
        "expected": "ACC2 1500\nACC1 800"
    },
    {
        "csv": "tid,acc,type,amount,time\nT1,X1,INVALID,500,2026-01-01T10:00:00\nT2,X1,CREDIT,-50,2026-01-01T10:05:00\nT3,X1,DEBIT,100,invalid-time\n",
        "expected": ""
    },
    {
        "csv": "tid,acc,type,amount,time\nT1,B1,CREDIT,300,2026-03-01T08:00:00\nT2,B2,DEBIT,300,2026-03-01T08:05:00\nT3,B3,CREDIT,500,2026-03-01T08:10:00\n",
        "expected": "B3 500\nB1 300\nB2 -300"
    }
]

def run_all_tests():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Q4_CSV_Transaction_Splitter.py"))
    
    for idx, tc in enumerate(TEST_CASES, 1):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
            tmp.write(tc["csv"])
            tmp_path = tmp.name

        try:
            proc = subprocess.run([sys.executable, script_path, tmp_path], capture_output=True, text=True)
            actual = proc.stdout.strip()
            expected = tc["expected"].strip()

            print(f"--- Test Case {idx} ---")
            if actual == expected:
                print("STATUS: PASSED")
                print(f"OUTPUT:\n{actual}" if actual else "OUTPUT: (No valid rows)")
            else:
                print("STATUS: FAILED")
                print(f"EXPECTED:\n{expected}")
                print(f"ACTUAL:\n{actual}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

if __name__ == "__main__":
    run_all_tests()
