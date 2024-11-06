# import rerun as rr

# from typing import List
# import numpy as np


# class Solution:
#     def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
#         rows = [m[0] for m in matrix]
#         row = self.search_lin(rows, target)
#         print("row", row)
#         if matrix[row][0] == target:
#             return True

#         col = self.search_lin(matrix[row], target)
#         print("col", col)

#         if matrix[row][col] == target:
#             return True

#         return False

#     def search_lin(self, lst, target):
#         left = 0
#         right = len(lst) - 1

#         i = 0

#         print(lst)
#         while left <= right:
#             i += 1
#             piv = (left + right) // 2
#             val = lst[piv]

#             disp = [np.nan] * len(lst)
#             disp[left] = -1
#             disp[piv] = 0
#             disp[right] = 1
#             rr.log("trans", rr.Transform3D([0, 0, i]))
#             rr.log("trans/array", rr.Tensor(np.asarray(lst)))
#             rr.log("trans/ptrs", rr.Tensor(np.asarray(disp)))

#             print("left", left)
#             print("piv", piv)
#             print("right", right)
#             print("val", val)
#             if val == target:
#                 print("found index", piv)
#                 return piv
#             if val < target:
#                 print("val < target")
#                 left = piv + 1
#             else:
#                 print("val > target")
#                 right = piv - 1
#         print("not in array")
#         print("left", left)
#         print("piv", piv)
#         print("right", right)
#         print("val", val)
#         return right


# rr.init("mat", spawn=True)
# # rr.set_time_sequence()

# matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
# Solution().searchMatrix(matrix, 3)
