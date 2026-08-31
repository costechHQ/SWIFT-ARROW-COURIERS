def read_float(prompt):
    """a safe helper function for post handling"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please enter a valid decimal value (e.g, 4.5)!!")