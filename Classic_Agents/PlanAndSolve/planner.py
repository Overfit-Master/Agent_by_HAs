import ast
from Classic_Agents.general_llm import HelloAgentsLLM
from planner_prompt import PLANNER_PROMPT_TEMPLATE


class Planner:
    def __init__(self, llm_client: HelloAgentsLLM, prompt=PLANNER_PROMPT_TEMPLATE):
        self.llm_client = llm_client
        self.prompt_template = prompt

    def plan(self, question: str):
        prompt = self.prompt_template.format(question=question)
        messages = [{"role": "user", "content": prompt}]

        print("--- 正在生成计划 ---")
        response_text = self.llm_client.think(messages)
        print(f"✅ 计划已生成:\n{response_text}")

        # 进行计划解析
        try:
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            # 字符串转为列表
            plan_list = ast.literal_eval(plan_str)

            return plan_list if isinstance(plan_list, list) else []

        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            print(f"原始响应: {response_text}")
            return []

        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []


if __name__ == '__main__':
    llm_client = HelloAgentsLLM()
    planner = Planner(llm_client)
    result = planner.plan("我的爷爷是谁？")

    print(f"\n\n\n{result}")