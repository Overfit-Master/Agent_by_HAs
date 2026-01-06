import re

# 导入之前定义好的相关工具和服务
from Classic_Agents.general_llm import HelloAgentsLLM
from tool import search
from tool_executor import ToolExecutor
from react_prompt import REACT_PROMPT_TEMPLATE


class ReActAgent:
    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self, question: str):
        """
        运行智能体解答用户的单个问题
        """

        # 单轮对话，历史记录每次运行时重置
        # 历史记录仅服务于ReAct的过程
        self.history = []
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"=== 智能体正在执行第{current_step}步 ===")

            # 格式化提示词补全所需信息
            tools_description = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_description,
                question=question,
                history=history_str
            )

            messages = [{"role": 'user', "content": prompt}]
            response_text = self.llm_client.think(messages)

            if not response_text:
                print("❌ 错误: LLM未能返回有效响应")
                break

            # LLM有响应则调用类内方法解析返回结果
            thought, action = self._parse_output(response_text)

            if thought:
                print(f"思考: {thought}")

            if not action:
                print("警告: 未能解析出有效的Action，流程终止。")
                break

            # 执行Action
            if action.startswith('Finish'):
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
                print(f"🎉 最终答案: {final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                """
                此处预留稳健性
                """
                continue

            print(f"🎬 行动: {tool_name}[{tool_input}]")

            tool_function = self.tool_executor.getTool(tool_name)
            if not tool_function:
                observation = f"错误:未找到名为 '{tool_name}' 的工具。"
            else:
                observation = tool_function(tool_input)  # 调用真实工具

            print(f"👀 观察: {observation}")

            # 将本轮的Action和Observation添加到历史记录中
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

            # 循环结束
        print("已达到最大步数，流程终止。")
        return None


    def _parse_output(self, text: str):
        """
        根据prompt的设计解析LLM返回的结果--Action和Thought
        """
        thought_match = re.search(r"Though: (.*)", text)
        action_match = re.search(r"Action: (.*)", text)

        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None

        return thought, action

    def _parse_action(self, action_text: str):
        """
        解析行动指令，提取工具名称以及输入
        """
        match = re.match(r"(\w+)\[(.*)\]", action_text)
        if match:
            return match.group(1), match.group(2)
        return None, None


if __name__ == '__main__':
    # 实例化LLM和工具执行器
    llm_client = HelloAgentsLLM()
    tool_executor = ToolExecutor()

    # 注册所需要的tool
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    tool_executor.registerTool("Search", search_description, search)

    # 实例化agent
    react_agent = ReActAgent(llm_client, tool_executor)
    react_agent.run("2025年9月30日前后阿里巴巴集团发生了什么利好的事情？")