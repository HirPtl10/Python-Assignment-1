import sys
import re
from typing import Dict, Union, Tuple, Optional

class FormulaError(Exception):
    pass

class InvalidFormatError(FormulaError):
    pass

class UnknownVariableError(FormulaError):
    pass

class DivisionByZeroError(FormulaError):
    pass

class UnsupportedOperatorError(FormulaError):
    pass

class FormulaValidatorCalculator:
    SUPPORTED_OPERATORS = {'+', '-', '*', '/', '%'}
    IDENTIFIER_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

    def __init__(self):
        self.variables: Dict[str, float] = {}

    def is_number(self, val_str: str) -> bool:
        try:
            float(val_str)
            return True
        except ValueError:
            return False

    def parse_operand(self, token: str) -> float:
        if self.is_number(token):
            return float(token)
        if self.IDENTIFIER_REGEX.match(token):
            if token in self.variables:
                return self.variables[token]
            raise UnknownVariableError(f"UnknownVariableError: '{token}'")
        raise InvalidFormatError(f"InvalidFormatError: '{token}'")

    def process_line(self, line: str) -> Optional[str]:
        line = line.strip()
        if not line or line.lower() == "quit":
            return None

        if "=" in line:
            parts = [p.strip() for p in line.split("=", 1)]
            var_name = parts[0]
            val_expr = parts[1]

            if not self.IDENTIFIER_REGEX.match(var_name):
                raise InvalidFormatError(f"InvalidFormatError: '{var_name}'")

            if self.is_number(val_expr):
                val = float(val_expr)
            else:
                tokens = val_expr.split()
                if len(tokens) == 1:
                    val = self.parse_operand(tokens[0])
                elif len(tokens) == 3:
                    val = self.evaluate_binary_formula(tokens[0], tokens[1], tokens[2])
                else:
                    raise InvalidFormatError(f"InvalidFormatError: '{val_expr}'")

            self.variables[var_name] = val
            return None

        tokens = line.split()
        if len(tokens) != 3:
            if "**" in line:
                raise UnsupportedOperatorError("UnsupportedOperatorError")
            raise InvalidFormatError("InvalidFormatError")

        op1_str, operator, op2_str = tokens[0], tokens[1], tokens[2]
        res = self.evaluate_binary_formula(op1_str, operator, op2_str)
        
        if res == int(res):
            return str(int(res))
        return str(round(res, 6))

    def evaluate_binary_formula(self, op1_str: str, operator: str, op2_str: str) -> float:
        val1 = self.parse_operand(op1_str)
        val2 = self.parse_operand(op2_str)

        if operator not in self.SUPPORTED_OPERATORS:
            raise UnsupportedOperatorError(f"UnsupportedOperatorError: '{operator}'")

        if operator in ('/', '%') and val2 == 0:
            raise DivisionByZeroError("DivisionByZeroError")

        if operator == '+':
            return val1 + val2
        elif operator == '-':
            return val1 - val2
        elif operator == '*':
            return val1 * val2
        elif operator == '/':
            return val1 / val2
        elif operator == '%':
            return val1 % val2

        raise UnsupportedOperatorError(f"UnsupportedOperatorError: '{operator}'")

def run_calculator_session(lines: List[str]) -> List[str]:
    calc = FormulaValidatorCalculator()
    output = []
    for line in lines:
        if line.strip().lower() == "quit":
            break
        try:
            res = calc.process_line(line)
            if res is not None:
                output.append(res)
        except FormulaError as fe:
            output.append(fe.__class__.__name__)
        except Exception as ex:
            output.append(ex.__class__.__name__)
    return output

if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if lines:
        out = run_calculator_session(lines)
        for line in out:
            print(line)
