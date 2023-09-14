import os
# 检查并删除指定CSV文件
def delete_csv_file(csv_file):
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"已删除文件：{csv_file}")
    else:
        print(f"文件不存在：{csv_file}")