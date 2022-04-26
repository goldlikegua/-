
def delete_num(inp):
    nums = [0] * 14
    print(nums)
    for num in inp:
        if nums[14-num]:
            nums[14-num] -= 1
        else:
            nums[num] += 1
    res = []
    for i in range(14):
        res += [i] * nums[i]
    return res

if __name__ == '__main__':
    inp = [1,4,4,7,1,5,8,4,5,10,12,13,13,4,5,4,2,12,13,11,9]
    nums = delete_num(inp)
    print(nums)