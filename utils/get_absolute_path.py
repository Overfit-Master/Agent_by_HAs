"""
此文件用于解决windows系统相对路径无法获取的问题
不使用绝对路径保证代码的兼容性
"""

import os

def from_project_root(*path):
    """
    :param path: 传入相对于根路径--PolyU_NLP_RAG的逐级路径
    :return: 拼接好的路径
    """
    # 多层嵌套，从当前文件路径-->utils路径-->项目根路径
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.normpath(os.path.join(root, *path))
    return target_path

if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(__file__)))
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))