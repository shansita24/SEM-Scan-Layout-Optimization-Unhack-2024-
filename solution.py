import pandas as pd
import numpy as np
import math
import os

# Define the path and list directories of the folder that contains the required datasets
path = "D://KLA//3rd"
dirs = os.listdir(path)

careAreas = None
metadata = None

# Load the CSV files
for file in dirs:
    if file.endswith(".csv") and file not in ['MainFields.csv', 'subFields.csv']:
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path)
        if file == 'CareAreas.csv':
            careAreas = np.loadtxt(file_path, delimiter=',')
        elif file == "metadata.csv":
            metadata = np.loadtxt(file_path, delimiter=',', skiprows=1)

# Remove the existing 'MainFields.csv' file and create a new one
file_path = os.path.join(path, "MainFields.csv")
if os.path.exists(file_path):
    os.remove(file_path)

meta = metadata.flatten()
mainFieldSize = int(meta[0])

final = []
subFieldFinal = []

# Function to check if a point is inside a rectangle
def inside(x1, x2, y1, y2, x_1, x_2, y_1, y_2):
    return (x1 >= x_1 and x1 <= x_2) and (x2 >= x_1 and x2 <= x_2) and (y1 >= y_1 and y1 <= y_2) and (y2 >= y_1 and y2 <= y_2)

# Process care areas to fill the final array
if careAreas is not None and len(careAreas) > 0:
    data = careAreas[0]
    x1, x2, y1, y2 = data[1], data[2], data[3], data[4]
    x_1, y_1 = x1, y1
    x_2, y_2 = x1 + mainFieldSize, y1 + mainFieldSize
    final.append([x_1, x_2, y_1, y_2])

    for i in range(1, len(careAreas)):
        data = careAreas[i]
        x1, x2, y1, y2 = data[1], data[2], data[3], data[4]
        flag = False
        for coord in final:
            x_1, x_2, y_1, y_2 = coord[0], coord[1], coord[2], coord[3]
            if inside(x1, x2, y1, y2, x_1, x_2, y_1, y_2):
                flag = True
                break
        if not flag:
            x_1, y_1 = x1, y1
            x_2, y_2 = x1 + mainFieldSize, y1 + mainFieldSize
            final.append([x_1, x_2, y_1, y_2])

# Convert final list to a NumPy array
final_array = np.array(final)
final_df = pd.DataFrame(final_array, columns=['X1', 'X2', 'Y1', 'Y2'])
final_df.insert(0, 'ID', range(len(final_df)))

output_csv_path = os.path.join(path, "MainFields.csv")
final_df.to_csv(output_csv_path, index=False, header=False)


def singleSubField(n):
    final1 = final_df.to_numpy()
    final = final1.tolist()
    cAreas = careAreas.tolist()
    for coord in final:
        x_1, x_2, y_1, y_2 =  coord[1], coord[2], coord[3], coord[4]
        num1 = math.ceil((x_2 - x_1) / n)
        num2 = math.ceil((y_2 - y_1) / n)
        for i in range(num1):
            for j in range(num2):
                a = x_1 + i * n
                b = y_1 + j * n
                a1 = a + n
                b1 = b + n
                for area in cAreas:
                    e, f, g, h = area[1], area[2], area[3], area[4]
                    if (a >= e and a <= f and b >= g and b <= h) or (a1 >= e and a1 <= f and b1 >= g and b1 <= h):
                        subFieldFinal.append([a, a1, b, b1, int(coord[0])])

def subfield():
    subFieldSize = []
    for i in range(len(meta)):
        if i % 2 != 0:
            subFieldSize.append(meta[i])
    if len(subFieldSize) == 1:
        singleSubField(subFieldSize[0])

subfield()
file_path = os.path.join(path, "subfield.csv")
if os.path.exists(file_path):
    os.remove(file_path)

final_subarray = np.array(subFieldFinal)
final_subdf = pd.DataFrame(final_subarray, columns=['X1', 'Y1', 'X2', 'Y2', 'MainFieldID'])
final_subdf.insert(0, 'ID', range(len(final_subdf)))

final_subdf.to_csv(file_path, index=False, header=False)
 
