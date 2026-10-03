from collections import defaultdict
from typing import Dict, List, Tuple

class StudentRecord:
    def __init__(self, enrollment: str, name: str, semester: int, cpi: float, marks: List[int]):
        self.enrollment = enrollment
        self.name = name
        self.semester = semester
        self.cpi = cpi
        self.marks = marks
        self.avg_marks = sum(marks) / len(marks) if marks else 0.0

    def sort_key(self) -> Tuple[float, float, str]:
        return (-self.cpi, -self.avg_marks, self.enrollment)

def validate_and_parse_input(raw_lines: List[str]) -> Tuple[int, int, int, List[StudentRecord]]:
    if not raw_lines:
        raise ValueError("Input data is empty.")
    
    first_line = raw_lines[0].strip().split()
    if len(first_line) != 3:
        raise ValueError("First line must contain exactly 3 integers: n k m")
    
    n, k, m = map(int, first_line)
    if n <= 0 or k <= 0 or m <= 0:
        raise ValueError("n, k, m must be positive integers.")
    
    students: List[StudentRecord] = []
    for idx in range(1, n + 1):
        if idx >= len(raw_lines):
            raise ValueError("Insufficient student records")
        tokens = raw_lines[idx].strip().split()
        if len(tokens) != 4 + m:
            raise ValueError("Invalid line format")
        
        enrollment = tokens[0]
        name = tokens[1]
        semester = int(tokens[2])
        cpi = float(tokens[3])
        marks = [int(x) for x in tokens[4:]]
        
        if not (1 <= semester <= 8):
            raise ValueError("Invalid semester")
        if not (0.0 <= cpi <= 10.0):
            raise ValueError("Invalid CPI")
        for mark in marks:
            if not (0 <= mark <= 100):
                raise ValueError("Invalid marks")
                
        students.append(StudentRecord(enrollment, name, semester, cpi, marks))
        
    return n, k, m, students

def analyze_merit(n: int, k: int, m: int, students: List[StudentRecord]) -> List[str]:
    output_lines: List[str] = []
    
    sem_map: Dict[int, List[StudentRecord]] = defaultdict(list)
    for s in students:
        sem_map[s.semester].append(s)
        
    for sem in sorted(sem_map.keys()):
        sem_students = sem_map[sem]
        sem_students.sort(key=lambda x: x.sort_key())
        top_k = sem_students[:k]
        top_enrollments = " ".join(s.enrollment for s in top_k)
        output_lines.append(f"Semester {sem}: {top_enrollments}")
        
    for subj_idx in range(m):
        subj_code = f"S{subj_idx + 1}"
        max_mark = -1
        toppers: List[str] = []
        
        for s in students:
            mark = s.marks[subj_idx]
            if mark > max_mark:
                max_mark = mark
                toppers = [s.enrollment]
            elif mark == max_mark:
                toppers.append(s.enrollment)
                
        toppers.sort()
        output_lines.append(f"{subj_code}: {' '.join(toppers)}")
        
    return output_lines

if __name__ == "__main__":
    import sys
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if lines:
        n, k, m, students = validate_and_parse_input(lines)
        output = analyze_merit(n, k, m, students)
        for line in output:
            print(line)
