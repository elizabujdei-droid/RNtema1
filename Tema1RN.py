import pathlib
import re
import math

#1 sis de ec

def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A = []
    B = []
    
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace(' ', '').strip()
            if not line:
                continue
            left_side, right_side = line.split('=')
            B.append(float(right_side))
            
            left_side = re.sub(r'(?<!\d)x', '1x', left_side)
            left_side = re.sub(r'(?<!\d)y', '1y', left_side)
            left_side = re.sub(r'(?<!\d)z', '1z', left_side)
            
            coefs = re.findall(r'[+-]?\d+(?:\.\d+)?', left_side)
            
            A.append([float(c) for c in coefs])
            
    return A, B

cale_fisier = pathlib.Path("idk.txt")
A, B = load_system(cale_fisier)

print()
print("mat a:", A)
print()
print("vect B:", B)
print()

#2 mat & vect

#2.1 det
def determinant(matrix: list[list[float]]) -> float:
    a11, a12, a13 = matrix[0]
    a21, a22, a23 = matrix[1]
    a31, a32, a33 = matrix[2]
    
    return (a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31))

print(f"{determinant(A)=}")
print()

#2.2 trace
def trace(matrix: list[list[float]]) -> float:
    return matrix[0][0] + matrix[1][1] + matrix[2][2]

print(f"{trace(A)=}")
print()

#2.3 norm
def norm(vector: list[float]) -> float:
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

print(f"{norm(B)=}")
print()

#2.4 transp mat
def transpose(matrix: list[list[float]]) -> list[list[float]]:
    transpusa = []
    for j in range(3):
        rand_nou = []
        for i in range(3):
            rand_nou.append(matrix[i][j])
        transpusa.append(rand_nou)
    return transpusa

print(f"{transpose(A)=}")
print()

#2.5 
def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    result = []
    for i in range(3):
        row_sum = 0.0
        for j in range(3):
            row_sum = row_sum + (matrix[i][j] * vector[j])
        result.append(row_sum)
    return result

print(f"{multiply(A, B)=}")
print()

#3 

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)

    if det_A == 0:
        raise ValueError("det=0 => sist nu are sol unica")
        
    solutions = []
    for col in range(3):
        A_modified = []
        for i in range(3):
            rand_nou = []
            for j in range(3):
                rand_nou.append(matrix[i][j])
            A_modified.append(rand_nou)
            
        for i in range(3):
            A_modified[i][col] = vector[i]
        
        solutions.append(determinant(A_modified) / det_A)
        
    return solutions

print(f"{solve_cramer(A, B)=}")
print()



#4


def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    result = []
    for row in range(3):
        if row != i:
            new_row = []
            for col in range(3):
                if col != j:
                    new_row.append(matrix[row][col])
            result.append(new_row)
    return result

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    cof_matrix = []
    for i in range(3):
        row_list = []
        for j in range(3):
            sign = (-1) ** (i + j)
            minor_matrix = minor(matrix, i, j)
            
            det_m = minor_matrix[0][0] * minor_matrix[1][1] - minor_matrix[0][1] * minor_matrix[1][0]
            
            row_list.append(sign * det_m)
        cof_matrix.append(row_list)
    return cof_matrix

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    if det_A == 0:
        raise ValueError("det=0 => sist nu are sol unica")
        
    adj = adjoint(matrix)
    inverse = []
    
    for i in range(3):
        inv_row = []
        for j in range(3):
            inv_row.append(adj[i][j] / det_A)
        inverse.append(inv_row)
        
    return multiply(inverse, vector)

print(f"{solve(A, B)=}")