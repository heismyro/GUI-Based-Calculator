import tkinter as tk
from tkinter import messagebox
import ast
import operator as op

# ---------------- Safe calculator engine ----------------
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def safe_eval(expression):
    """Evaluate only basic arithmetic entered by the calculator."""
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.left), evaluate(node.right))
        raise ValueError("Invalid expression")

    return evaluate(tree)


# ---------------- Calculator functions ----------------
def add_to_expression(value):
    current = display_var.get()
    if current == "Error":
        current = ""
    display_var.set(current + value)

def clear_display():
    display_var.set("")

def calculate():
    expression = display_var.get().strip()
    if not expression:
        return
    try:
        result = safe_eval(expression)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        display_var.set(str(result))
    except ZeroDivisionError:
        display_var.set("Error")
        messagebox.showerror("Calculation Error", "Cannot divide by zero.")
    except Exception:
        display_var.set("Error")
        messagebox.showerror("Calculation Error", "Invalid calculation.")

def keyboard_input(event):
    if event.char in "0123456789.+-*/%":
        add_to_expression(event.char)
    elif event.keysym in ("Return", "KP_Enter"):
        calculate()
    elif event.keysym == "BackSpace":
        display_var.set(display_var.get()[:-1])
    elif event.keysym == "Escape":
        clear_display()


# ---------------- Main window ----------------
root = tk.Tk()
root.title("GUI-Based Calculator")
root.geometry("430x650")
root.resizable(False, False)
root.configure(bg="black")

display_var = tk.StringVar()

# Display area
display = tk.Entry(
    root,
    textvariable=display_var,
    font=("Arial", 30, "bold"),
    justify="right",
    bd=4,
    relief="sunken",
    bg="white",
    fg="black",
    insertbackground="black"
)
display.pack(fill="x", padx=22, pady=(22, 16), ipady=24)
display.focus_set()

# Calculator button area
button_frame = tk.Frame(root, bg="black")
button_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# Exact layout from the hand-drawn design:
#
#       7    8    9    ÷
#       4    5    6    ×
#       1    2    3    −
#       C    0    =    +
#
# Numeric buttons = RED
# Action/operator buttons = YELLOW
numeric_bg = "#d90000"
numeric_active = "#ff2222"
action_bg = "#ffd600"
action_active = "#ffe94a"

button_specs = [
    ("7", 0, 0, lambda: add_to_expression("7"), numeric_bg, numeric_active),
    ("8", 0, 1, lambda: add_to_expression("8"), numeric_bg, numeric_active),
    ("9", 0, 2, lambda: add_to_expression("9"), numeric_bg, numeric_active),
    ("÷", 0, 3, lambda: add_to_expression("/"), action_bg, action_active),

    ("4", 1, 0, lambda: add_to_expression("4"), numeric_bg, numeric_active),
    ("5", 1, 1, lambda: add_to_expression("5"), numeric_bg, numeric_active),
    ("6", 1, 2, lambda: add_to_expression("6"), numeric_bg, numeric_active),
    ("×", 1, 3, lambda: add_to_expression("*"), action_bg, action_active),

    ("1", 2, 0, lambda: add_to_expression("1"), numeric_bg, numeric_active),
    ("2", 2, 1, lambda: add_to_expression("2"), numeric_bg, numeric_active),
    ("3", 2, 2, lambda: add_to_expression("3"), numeric_bg, numeric_active),
    ("−", 2, 3, lambda: add_to_expression("-"), action_bg, action_active),

    ("C", 3, 0, clear_display, action_bg, action_active),
    ("0", 3, 1, lambda: add_to_expression("0"), numeric_bg, numeric_active),
    ("=", 3, 2, calculate, action_bg, action_active),
    ("+", 3, 3, lambda: add_to_expression("+"), action_bg, action_active),
]

for text, row, col, command, bg, active_bg in button_specs:
    button = tk.Button(
        button_frame,
        text=text,
        command=command,
        font=("Arial", 22, "bold"),
        bg=bg,
        fg="black",
        activebackground=active_bg,
        activeforeground="black",
        bd=2,
        relief="raised",
        cursor="hand2"
    )
    button.grid(
        row=row,
        column=col,
        sticky="nsew",
        padx=4,
        pady=4,
        ipadx=4,
        ipady=20
    )

# Equal-sized columns/rows reproduce the hand-drawn four-column arrangement.
for i in range(4):
    button_frame.columnconfigure(i, weight=1)
    button_frame.rowconfigure(i, weight=1)

root.bind("<Key>", keyboard_input)
root.mainloop()
