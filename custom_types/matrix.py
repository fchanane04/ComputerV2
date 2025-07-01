class Matrix:
    def __init__(self, rows):
        if not rows or not all(len(row) == len(rows[0]) for row in rows):
            raise ValueError("Invalid matrix dimensions")
        self.rows = rows
        self.shape = (len(rows), len(rows[0]))