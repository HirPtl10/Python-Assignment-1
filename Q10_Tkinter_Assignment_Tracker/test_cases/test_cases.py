import os
import sys

def run_all_tests():
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, script_dir)
    
    from Q10_Tkinter_Assignment_Tracker import AssignmentTrackerModel, SubmissionRecord

    test_db = os.path.join(os.path.dirname(__file__), "test_db.json")
    test_csv = os.path.join(os.path.dirname(__file__), "test_export.csv")

    if os.path.exists(test_db):
        os.remove(test_db)
    if os.path.exists(test_csv):
        os.remove(test_csv)

    model = AssignmentTrackerModel(db_path=test_db)

    # Test Case 1: Add record 1
    rec1 = SubmissionRecord("2201", "Asha", "Assignment 1", "Completed", 18.0, "Good job", True)
    model.add_record(rec1)
    print("--- Test Case 1 (Add Record) ---")
    print("STATUS: PASSED" if len(model.records) == 1 else "STATUS: FAILED")
    print(f"RECORDS: {len(model.records)}")

    # Test Case 2: Add record 2 and filter Pending
    rec2 = SubmissionRecord("2202", "Bharat", "Assignment 1", "Pending", 0.0, "Under review", False)
    model.add_record(rec2)
    pending_recs = model.get_filtered_records(status_filter="Pending")
    print("--- Test Case 2 (Filter Pending) ---")
    print("STATUS: PASSED" if len(pending_recs) == 1 and pending_recs[0][1].name == "Bharat" else "STATUS: FAILED")
    print(f"PENDING COUNT: {len(pending_recs)}")

    # Test Case 3: Update Record
    updated_rec2 = SubmissionRecord("2202", "Bharat", "Assignment 1", "Completed", 19.5, "Reviewed & Passed", True)
    model.update_record(1, updated_rec2)
    completed_recs = model.get_filtered_records(status_filter="Completed")
    print("--- Test Case 3 (Update Record) ---")
    print("STATUS: PASSED" if len(completed_recs) == 2 else "STATUS: FAILED")
    print(f"COMPLETED COUNT: {len(completed_recs)}")

    # Test Case 4: Export CSV
    exported_file = model.export_csv(test_csv)
    print("--- Test Case 4 (Export CSV) ---")
    print("STATUS: PASSED" if os.path.exists(exported_file) else "STATUS: FAILED")
    if os.path.exists(exported_file):
        with open(exported_file, "r") as f:
            print("CSV CONTENT:\n" + f.read().strip())

    if os.path.exists(test_db):
        os.remove(test_db)
    if os.path.exists(test_csv):
        os.remove(test_csv)

if __name__ == "__main__":
    run_all_tests()
