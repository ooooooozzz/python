import argparse
import csv
import json

# 判断文件是否是CSV文件
# 判断的方法就是看，用csv中的读取函数能不能正常的读取数据
def IsCSVFile(filename):
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            cnt = 0
            for row in reader:
                cnt += 1
            return True
    except csv.Error:
        return False
    except Exception as e:
        return False

# 判断文件是否是JSON文件
# 判断的方法就是看，用json中的加载函数，能不能正常加载
def IsJSONFile(filename):
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            # 尝试加载整个 JSON 文件
            json.load(file)
            return True
    except json.JSONDecodeError:
        # 如果 JSON 解码失败，返回 False
        return False
    except Exception as e:
        # 捕获其他异常，返回 False
        print(f"发生错误: {e}")
        return False

# 将CSV转化成JSON文件
# 解决方式，创建一个JSON文件，然后将CSV文件中的内容写入到JSON文件中
def ConvertFileFormatToJSON(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    output_filename = filename.rsplit('.', 1)[0] + '.JSON'
    with open(output_filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file)

    print(f"文件已从 {filename} 转换为 {output_filename}")

# 将JSON转化成CSV文件
# 解决方式，创建一个CSV文件，然后将JSON文件中的内容写入到CSV文件中
def ConvertFileFormatToCSV(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        data = json.load(file)

    fieldnames = data[0].keys()
    output_filename = filename.rsplit('.', 1)[0] + '.CSV'
    with open(output_filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"文件已从 {filename} 转换为 {output_filename}")


if __name__ == '__main__':
    # 创建一个命令行对象，读取参数
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input file')
    args = parser.parse_args()
    filename = args.input

    # 逻辑判断
    # 查看文件是否存在、查看是CSV文件还是JSON文件、如果都不是，则报文件格式错误！
    if (filename):
        print('文件不存在')
    elif (IsJSONFile(filename)):
        ConvertFileFormatToCSV(filename)
    elif (IsCSVFile(filename)):
        # True, 转化
        ConvertFileFormatToJSON(filename)
    else:
        print('文件格式异常！')