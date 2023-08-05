import numpy as np

def find_max_sum_drop_location(array):
    # 计算每一列的总和
    column_sums = np.sum(array, axis=0)
    print(column_sums)
    # 计算每一列与前一列总和的差值
    sum_drops = np.diff(column_sums)
    print(sum_drops)

    # 找到总和下降最多的位置
    max_drop_index = np.argmin(sum_drops)

    return max_drop_index

if __name__ == "__main__":
    # 示例 2D NumPy数组
    example_array = np.array([[2, 1, 255, 0],
                              [6, 5, 255, 0],
                              [10, 9, 255, 0],
                              [14, 13, 255, 0]])

    max_drop_location = find_max_sum_drop_location(example_array)
    print(example_array)
    print("列与列之间总和下降最多的地方在第", max_drop_location, "列")
