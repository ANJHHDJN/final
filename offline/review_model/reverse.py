flag = 0
while flag == 0:
    input_line = input("输入文字:")
    if input_line == 'q':
        flag = 1
    input_line = input_line[::-1]
    print(input_line)