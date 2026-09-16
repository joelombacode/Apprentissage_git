"""Simple safe calculator REPL and evaluator.

Usage:
 - Run `python exercice.py` to start interactive REPL.
 - Or `python exercice.py 2+3*4` to evaluate an expression and exit.
"""
from __future__ import annotations

import ast
import operator
import sys
from typing import Any


_BIN_OPS = {
	ast.Add: operator.add,
	ast.Sub: operator.sub,
	ast.Mult: operator.mul,
	ast.Div: operator.truediv,
	ast.FloorDiv: operator.floordiv,
	ast.Mod: operator.mod,
	ast.Pow: operator.pow,
}

_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _eval_node(node: ast.AST) -> Any:
	if isinstance(node, ast.Expression):
		return _eval_node(node.body)

	if isinstance(node, ast.BinOp):
		left = _eval_node(node.left)
		right = _eval_node(node.right)
		op_type = type(node.op)
		if op_type in _BIN_OPS:
			try:
				return _BIN_OPS[op_type](left, right)
			except ZeroDivisionError as e:
				raise ValueError("division by zero") from e
		raise ValueError(f"unsupported binary operator: {op_type.__name__}")

	if isinstance(node, ast.UnaryOp):
		operand = _eval_node(node.operand)
		op_type = type(node.op)
		if op_type in _UNARY_OPS:
			return _UNARY_OPS[op_type](operand)
		raise ValueError(f"unsupported unary operator: {op_type.__name__}")

	if isinstance(node, ast.Constant):
		if isinstance(node.value, (int, float)):
			return node.value
		raise ValueError("only int/float constants are allowed")

	# For older Python versions
	if isinstance(node, ast.Num):
		return node.n

	if isinstance(node, ast.Call):
		raise ValueError("function calls are not allowed")

	raise ValueError(f"unsupported expression: {type(node).__name__}")


def evaluate_expr(expr: str) -> float:
	"""Evaluate a mathematical expression safely and return a number.

	Supports +, -, *, /, //, %, ** and unary +/-. Parentheses are allowed.
	"""
	try:
		parsed = ast.parse(expr, mode="eval")
	except SyntaxError as e:
		raise ValueError("invalid syntax") from e

	# Walk the AST to ensure it's safe (only allowed nodes)
	for node in ast.walk(parsed):
		if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.Expression, ast.Constant, ast.Num, ast.Load, ast.Expr)):
			continue
		if isinstance(node, ast.operator) or isinstance(node, ast.unaryop):
			continue
		# disallow names, attributes, subscripts, calls, comprehensions, etc.
		if isinstance(node, (ast.Call, ast.Attribute, ast.Name, ast.Subscript, ast.List, ast.Tuple, ast.Dict, ast.Set)):
			raise ValueError("unsupported expression element")

	return float(_eval_node(parsed))


def repl() -> None:
	print("Simple calculator. Type 'exit' or 'quit' to leave.")
	while True:
		try:
			s = input("expr> ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if not s:
			continue
		if s.lower() in {"exit", "quit"}:
			break
		if s.lower() in {"help", "h", "?"}:
			print("Enter a math expression using + - * / // % ** and parentheses.")
			continue
		try:
			result = evaluate_expr(s)
		except Exception as e:
			print("Error:", e)
		else:
			# Print integers without decimal when possible
			if result.is_integer():
				print(int(result))
			else:
				print(result)


def main() -> None:
	if len(sys.argv) > 1:
		expr = " ".join(sys.argv[1:])
		try:
			print(evaluate_expr(expr))
		except Exception as e:
			print("Error:", e)
			sys.exit(1)
		return

	repl()


if __name__ == "__main__":
	main()
