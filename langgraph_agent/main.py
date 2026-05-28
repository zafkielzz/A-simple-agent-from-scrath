from typing import Optional
def nice_message(name = None):
    if name is None:
        print("Hello random person")
    else:
        print(f"hello {name}")

nice_message("Nam")