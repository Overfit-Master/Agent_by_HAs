import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict


# 加载.env (gitignore)中的环境变量
load_dotenv()


class HelloAgentsLLM:
    """
    以Hello Agents教程定制的LLM客户端
    调用兼容OpenAI接口的服务，默认流式响应
    """

    def __init__(self, model: str = None, apikey: str = None, baseurl: str = None, timeout: int = None):
        """
        初始化客户端，优先使用传入参数，未提供则从环境变量中进行加载
        """

        self.model = model or os.getenv("LLM_MODEL_ID")
        apikey = apikey or os.getenv("LLM_API_KEY")
        baseurl = baseurl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))      # getenv可以设置默认值(str)然后通过int进行转换

        if not all([self.model, apikey, baseurl]):
            raise ValueError("模型ID、API密钥和服务地址加载出现空缺")

        self.client = OpenAI(api_key=apikey, base_url=baseurl, timeout=timeout)


    def think(self, messages: List[Dict[str, str]], temperature: float = 0):
        """
        temperature越低越具备确定性
        """

        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True
            )

            # 处理流式响应
            print("🆗 大语言模型响应成功")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)      # 输出后使用flush刷新缓存
                collected_content.append(content)
            print()     # 流式输出后换行
            return "".join(collected_content)       # 拼接完整的流式输出为完整内容

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误：{e}")
            return None


# 代码测试
if __name__ == '__main__':
    try:
        llmClient = HelloAgentsLLM()

        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "推荐新手入门的rag项目及相关数据集"}
        ]

        print("--- 调用LLM ---")
        responseText = llmClient.think(exampleMessages)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)

    except ValueError as e:
        print(e)