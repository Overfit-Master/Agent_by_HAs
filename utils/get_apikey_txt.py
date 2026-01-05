# 本文件用于整合读取以txt格式存储的api key

def get_api(txt_path):
    with open(txt_path) as f:
        return f.read()