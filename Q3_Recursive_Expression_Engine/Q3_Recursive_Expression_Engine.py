import sys
from typing import Dict, List, Union, Set, Optional, Tuple

class CycleException(Exception):
    pass

class InvalidSyntaxException(Exception):
    pass

class Tokenizer:
    def __init__(self, expr_str: str):
        self.expr_str = expr_str
        self.length = len(expr_str)
        self.pos = 0

    def tokenize(self) -> List[Tuple[str, str]]:
        tokens = []
        i = 0
        n = len(self.expr_str)
        while i < n:
            ch = self.expr_str[i]
            if ch.isspace():
                i += 1
                continue
            if ch.isdigit():
                start = i
                while i < n and self.expr_str[i].isdigit():
                    i += 1
                tokens.append(('INT', self.expr_str[start:i]))
            elif ch.isalpha() or ch == '_':
                start = i
                while i < n and (self.expr_str[i].isalnum() or self.expr_str[i] == '_'):
                    i += 1
                tokens.append(('VAR', self.expr_str[start:i]))
            elif ch in '+-*':
                tokens.append(('OP', ch))
                i += 1
            elif ch == '(':
                tokens.append(('LPAREN', '('))
                i += 1
            elif ch == ')':
                tokens.append(('RPAREN', ')'))
                i += 1
            else:
                raise InvalidSyntaxException(f"Unexpected character: {ch}")
        return tokens

class Parser:
    def __init__(self, tokens: List[Tuple[str, str]], engine: 'ExpressionEngine'):
        self.tokens = tokens
        self.pos = 0
        self.length = len(tokens)
        self.engine = engine

    def peek(self) -> Optional[Tuple[str, str]]:
        if self.pos < self.length:
            return self.tokens[self.pos]
        return None

    def consume(self) -> Tuple[str, str]:
        tok = self.peek()
        if tok is None:
            raise InvalidSyntaxException("Unexpected end of expression")
        self.pos += 1
        return tok

    def parse_expr(self) -> int:
        val = self.parse_term()
        while True:
            tok = self.peek()
            if tok and tok[0] == 'OP' and tok[1] in ('+', '-'):
                op_type, op_val = self.consume()
                right_val = self.parse_term()
                if op_val == '+':
                    val += right_val
                else:
                    val -= right_val
            else:
                break
        return val

    def parse_term(self) -> int:
        val = self.parse_factor()
        while True:
            tok = self.peek()
            if tok and tok[0] == 'OP' and tok[1] == '*':
                self.consume()
                right_val = self.parse_factor()
                val *= right_val
            else:
                break
        return val

    def parse_factor(self) -> int:
        tok = self.peek()
        if tok is None:
            raise InvalidSyntaxException("Expected factor")

        if tok[0] == 'INT':
            self.consume()
            return int(tok[1])
        elif tok[0] == 'VAR':
            var_name = self.consume()[1]
            return self.engine.evaluate_variable(var_name)
        elif tok[0] == 'LPAREN':
            self.consume()
            val = self.parse_expr()
            close_tok = self.peek()
            if close_tok is None or close_tok[0] != 'RPAREN':
                raise InvalidSyntaxException("Missing closing parenthesis")
            self.consume()
            return val
        elif tok[0] == 'OP' and tok[1] == '-':
            self.consume()
            return -self.parse_factor()
        else:
            raise InvalidSyntaxException(f"Unexpected token: {tok[1]}")

class ExpressionEngine:
    def __init__(self, var_defs: Dict[str, str]):
        self.var_defs = var_defs
        self.memo: Dict[str, int] = {}
        self.visiting: Set[str] = set()

    def evaluate_variable(self, var_name: str) -> int:
        if var_name in self.memo:
            return self.memo[var_name]

        if var_name not in self.var_defs:
            raise InvalidSyntaxException(f"Undefined variable: {var_name}")

        if var_name in self.visiting:
            raise CycleException(f"Cycle detected: {var_name}")

        self.visiting.add(var_name)
        try:
            expr_str = self.var_defs[var_name]
            tokenizer = Tokenizer(expr_str)
            tokens = tokenizer.tokenize()
            parser = Parser(tokens, self)
            val = parser.parse_expr()
            if parser.pos < parser.length:
                raise InvalidSyntaxException("Extra unparsed tokens")
            self.memo[var_name] = val
            return val
        finally:
            self.visiting.remove(var_name)

    def evaluate_expression(self, expr_str: str) -> str:
        try:
            tokenizer = Tokenizer(expr_str)
            tokens = tokenizer.tokenize()
            if not tokens:
                return "INVALID"
            parser = Parser(tokens, self)
            val = parser.parse_expr()
            if parser.pos < parser.length:
                return "INVALID"
            return str(val)
        except CycleException:
            return "CYCLE"
        except InvalidSyntaxException:
            return "INVALID"
        except Exception:
            return "INVALID"

if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if lines:
        v = int(lines[0])
        var_defs = {}
        for i in range(1, 1 + v):
            parts = lines[i].split('=', 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                expr = parts[1].strip()
                var_defs[var_name] = expr
        expr_to_eval = lines[1 + v] if len(lines) > 1 + v else ""
        engine = ExpressionEngine(var_defs)
        print(engine.evaluate_expression(expr_to_eval))
