from typing import Dict, Any
from tool import search

class ToolExecutor:
    """
    工具执行器，负责管理和执行工具
    """

    def __init__(self):
        # {description:  , func: }
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str, func: callable):
        """
        注册工具
        """

        if name in self.tools:
            print(f"❗工具'{name}'已存在，将覆盖重新注册")
        self.tools[name] = {'description': description, 'func': func}
        print(f"工具'{name}'已注册")

    def getTool(self, name: str):
        """
        输入工具名称获取执行函数
        """

        return self.tools.get(name, {}).get('func')     # 第一个get确保工具不存在时不会报错，最终返回None

    def getAvailableTools(self):
        """
        格式化返回所有可用工具
        "name: tool's description"
        """

        return "\n".join([
            f"{name}: {info['description']}"
            for name, info in self.tools.items()
        ])


# --- 工具初始化与使用示例 ---
if __name__ == '__main__':
    # 1. 初始化工具执行器
    toolExecutor = ToolExecutor()

    # 2. 注册我们的实战搜索工具
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("Search", search_description, search)

    # 3. 打印可用的工具
    print("\n--- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())

    # 4. 智能体的Action调用，这次我们问一个实时性的问题
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"

    tool_function = toolExecutor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")

