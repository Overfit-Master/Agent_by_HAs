from Classic_Agents.general_llm import HelloAgentsLLM
from executor_prompt import EXECUTOR_PROMPT_TEMPLATE


class Executor:
    def __init__(self, llm_client: HelloAgentsLLM, prompt=EXECUTOR_PROMPT_TEMPLATE):
        self.llm_client = llm_client
        self.prompt_template = prompt

    def execute(self, question: str, plan: list[str]):
        """
        按计划逐步执行
        """

        # 存储历史步骤和结果
        history = ""

        print("\n--- 正在执行计划---")

        for i, step in enumerate(plan):
            print(f"\n-> 正在执行步骤 {i+1}/{len(plan)}: {step}")

            prompt = self.prompt_template.format(
                question = question,
                plan = plan,
                history = history if history else "无",
                current_step = step
            )

            messages = [{"role": "user", "content": prompt}]

            response_text = self.llm_client.think(messages)

            history += f"步骤 {i+1} 已完成\n结果: {response_text}\n\n"
            print(f"✅ 步骤 {i+1} 已完成，结果: {response_text}")

        final_answer = response_text
        return final_answer