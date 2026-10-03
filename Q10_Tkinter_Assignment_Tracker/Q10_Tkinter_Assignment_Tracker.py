import csv
import json
import os
import sys
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False
    tk = None
    ttk = None
    messagebox = None
    filedialog = None
from typing import Dict, List, Any, Optional, Tuple

DB_FILE = "assignments_db.json"
EXPORT_CSV = "exported_submissions.csv"

class SubmissionRecord:
    def __init__(self, enrollment: str, name: str, assignment: str, status: str, marks: float, remarks: str, verified: bool = False):
        self.enrollment = enrollment
        self.name = name
        self.assignment = assignment
        self.status = status
        self.marks = marks
        self.remarks = remarks
        self.verified = verified

    def to_dict(self) -> Dict[str, Any]:
        return {
            "enrollment": self.enrollment,
            "name": self.name,
            "assignment": self.assignment,
            "status": self.status,
            "marks": self.marks,
            "remarks": self.remarks,
            "verified": self.verified
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SubmissionRecord':
        return cls(
            enrollment=data["enrollment"],
            name=data["name"],
            assignment=data["assignment"],
            status=data["status"],
            marks=float(data["marks"]),
            remarks=data.get("remarks", ""),
            verified=data.get("verified", False)
        )

class AssignmentTrackerModel:
    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path
        self.records: List[SubmissionRecord] = []
        self.load_data()

    def add_record(self, record: SubmissionRecord):
        self.records.append(record)
        self.save_data()

    def update_record(self, index: int, record: SubmissionRecord):
        if 0 <= index < len(self.records):
            self.records[index] = record
            self.save_data()

    def get_filtered_records(self, status_filter: str = "All", search_query: str = "") -> List[Tuple[int, SubmissionRecord]]:
        results = []
        search_lower = search_query.lower()
        for idx, rec in enumerate(self.records):
            if status_filter != "All" and rec.status != status_filter:
                continue
            if search_query:
                if (search_lower not in rec.enrollment.lower() and 
                    search_lower not in rec.name.lower() and 
                    search_lower not in rec.assignment.lower()):
                    continue
            results.append((idx, rec))
        return results

    def save_data(self):
        data = [r.to_dict() for r in self.records]
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.records = [SubmissionRecord.from_dict(d) for d in data]
            except Exception as e:
                self.records = []

    def export_csv(self, csv_filepath: str = EXPORT_CSV) -> str:
        with open(csv_filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Enrollment", "Name", "Assignment", "Status", "Marks", "Remarks"])
            for rec in self.records:
                writer.writerow([rec.enrollment, rec.name, rec.assignment, rec.status, rec.marks, rec.remarks])
        return csv_filepath

class AssignmentTrackerGUI:
    def __init__(self, root: tk.Tk, model: AssignmentTrackerModel):
        self.root = root
        self.model = model
        self.root.title("Student Assignment Tracker")
        self.root.geometry("900x650")
        self.selected_index: Optional[int] = None

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        header = ttk.Label(self.root, text="Student Assignment Submission Tracker", font=("Helvetica", 16, "bold"))
        header.pack(pady=10)

        form_frame = ttk.LabelFrame(self.root, text=" Submission Details ")
        form_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(form_frame, text="Enrollment No:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_enrollment = ttk.Entry(form_frame, width=20)
        self.ent_enrollment.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame, text="Student Name:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_name = ttk.Entry(form_frame, width=25)
        self.ent_name.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame, text="Assignment Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_assignment = ttk.Entry(form_frame, width=20)
        self.ent_assignment.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame, text="Marks (0-100):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_marks = ttk.Entry(form_frame, width=10)
        self.ent_marks.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame, text="Status:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.var_status = tk.StringVar(value="Completed")
        rb_pending = ttk.Radiobutton(form_frame, text="Pending", variable=self.var_status, value="Pending")
        rb_completed = ttk.Radiobutton(form_frame, text="Completed", variable=self.var_status, value="Completed")
        rb_pending.grid(row=2, column=1, sticky="w", padx=5)
        rb_completed.grid(row=2, column=1, sticky="e", padx=5)

        self.var_verified = tk.BooleanVar(value=True)
        chk_verified = ttk.Checkbutton(form_frame, text="Verified Entry", variable=self.var_verified)
        chk_verified.grid(row=2, column=2, columnspan=2, sticky="w", padx=5)

        ttk.Label(form_frame, text="Remarks:").grid(row=3, column=0, padx=5, pady=5, sticky="ne")
        self.txt_remarks = tk.Text(form_frame, height=3, width=50)
        self.txt_remarks.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=15, pady=5)

        ttk.Button(btn_frame, text="Add Submission", command=self.add_submission).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update Selected", command=self.update_submission).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Export CSV Report", command=self.export_csv).pack(side="right", padx=5)

        filter_frame = ttk.LabelFrame(self.root, text=" Filter & Search ")
        filter_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(filter_frame, text="Filter Status:").pack(side="left", padx=5)
        self.cmb_filter = ttk.Combobox(filter_frame, values=["All", "Completed", "Pending"], state="readonly", width=12)
        self.cmb_filter.set("All")
        self.cmb_filter.pack(side="left", padx=5)
        self.cmb_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        ttk.Label(filter_frame, text="Search:").pack(side="left", padx=(20, 5))
        self.ent_search = ttk.Entry(filter_frame, width=20)
        self.ent_search.pack(side="left", padx=5)
        self.ent_search.bind("<KeyRelease>", lambda e: self.refresh_table())

        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        columns = ("enrollment", "name", "assignment", "status", "marks", "remarks")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("enrollment", text="Enrollment")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("assignment", text="Assignment")
        self.tree.heading("status", text="Status")
        self.tree.heading("marks", text="Marks")
        self.tree.heading("remarks", text="Remarks")

        self.tree.column("enrollment", width=100, anchor="center")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("assignment", width=150, anchor="w")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("marks", width=80, anchor="e")
        self.tree.column("remarks", width=250, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def validate_inputs(self) -> Optional[SubmissionRecord]:
        enrollment = self.ent_enrollment.get().strip()
        name = self.ent_name.get().strip()
        assignment = self.ent_assignment.get().strip()
        marks_str = self.ent_marks.get().strip()
        status = self.var_status.get()
        remarks = self.txt_remarks.get("1.0", tk.END).strip()
        verified = self.var_verified.get()

        if not enrollment or not name or not assignment:
            if messagebox:
                messagebox.showerror("Error", "All fields required")
            return None

        try:
            marks = float(marks_str)
            if not (0 <= marks <= 100):
                if messagebox:
                    messagebox.showerror("Error", "Marks must be between 0 and 100")
                return None
        except ValueError:
            if messagebox:
                messagebox.showerror("Error", "Invalid marks")
            return None

        return SubmissionRecord(enrollment, name, assignment, status, marks, remarks, verified)

    def add_submission(self):
        rec = self.validate_inputs()
        if rec:
            self.model.add_record(rec)
            self.refresh_table()
            self.clear_form()

    def update_submission(self):
        if self.selected_index is not None:
            rec = self.validate_inputs()
            if rec:
                self.model.update_record(self.selected_index, rec)
                self.refresh_table()
                self.clear_form()

    def clear_form(self):
        self.ent_enrollment.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_assignment.delete(0, tk.END)
        self.ent_marks.delete(0, tk.END)
        self.txt_remarks.delete("1.0", tk.END)
        self.var_status.set("Completed")
        self.var_verified.set(True)
        self.selected_index = None

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0]
            values = self.tree.item(item_id, "values")
            tags = self.tree.item(item_id, "tags")
            if tags:
                self.selected_index = int(tags[0])
                self.ent_enrollment.delete(0, tk.END)
                self.ent_enrollment.insert(0, values[0])
                self.ent_name.delete(0, tk.END)
                self.ent_name.insert(0, values[1])
                self.ent_assignment.delete(0, tk.END)
                self.ent_assignment.insert(0, values[2])
                self.var_status.set(values[3])
                self.ent_marks.delete(0, tk.END)
                self.ent_marks.insert(0, values[4])
                self.txt_remarks.delete("1.0", tk.END)
                self.txt_remarks.insert("1.0", values[5])

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        status_flt = self.cmb_filter.get()
        search_q = self.ent_search.get().strip()

        filtered_records = self.model.get_filtered_records(status_flt, search_q)
        for original_idx, rec in filtered_records:
            self.tree.insert(
                "", tk.END,
                values=(rec.enrollment, rec.name, rec.assignment, rec.status, rec.marks, rec.remarks),
                tags=(str(original_idx),)
            )

    def export_csv(self):
        filepath = EXPORT_CSV
        if filedialog:
            fn = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if fn:
                filepath = fn
        self.model.export_csv(filepath)

if __name__ == "__main__":
    if HAS_TKINTER:
        try:
            root = tk.Tk()
            model = AssignmentTrackerModel()
            app = AssignmentTrackerGUI(root, model)
            root.mainloop()
        except Exception:
            pass
