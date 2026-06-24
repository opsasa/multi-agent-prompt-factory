import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

user_goal = (
    os.getenv("USER_GOAL")
    or os.getenv("TOPIC")
    or "我想做一个 Windows 故障诊断 AI，用户输入问题后，AI 输出安全的排查步骤，要求像真人，不要太人机。"
)

model = os.getenv("MODEL", "deepseek/deepseek-v4-pro")

llm_args = {
    "model": model,
    "temperature": float(os.getenv("TEMPERATURE", "0.8")),
}

api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL") or os.getenv("OPENAI_BASE_URL")

if api_key:
    llm_args["api_key"] = api_key

if base_url:
    llm_args["base_url"] = base_url

llm = LLM(**llm_args)


# Agent 1：需求分析员
requirement_analyst = Agent(
    role="需求分析员",
    goal="分析用户真正想让 AI 完成什么任务，拆出使用场景、目标用户、输出要求和风险点。",
    backstory=(
        "你擅长把模糊需求拆清楚。"
        "你不会急着写 Prompt，而是先判断用户到底想要什么、怕什么、需要什么输出。"
    ),
    llm=llm,
    verbose=True,
)


# Agent 2：Prompt 架构师
prompt_architect = Agent(
    role="Prompt 架构师",
    goal="根据需求分析结果，设计一版结构清晰、可直接复制使用的 Prompt 初稿。",
    backstory=(
        "你是一名 Prompt 工程师，擅长设计角色、任务、输入、输出格式、限制条件和风格要求。"
        "你写的 Prompt 要具体，不要空泛。"
    ),
    llm=llm,
    verbose=True,
)


# Agent 3：反例测试员
prompt_critic = Agent(
    role="Prompt 反例测试员",
    goal="专门挑出 Prompt 初稿里的问题，包括太泛、人机味太重、输出不稳定、缺少限制条件等。",
    backstory=(
        "你很挑剔，专门检查 Prompt 在真实使用时会不会翻车。"
        "你会指出哪里容易导致 AI 胡说、写废话、格式混乱或输出危险内容。"
    ),
    llm=llm,
    verbose=True,
)


# Agent 4：最终优化员
prompt_optimizer = Agent(
    role="Prompt 最终优化员",
    goal="根据前面的分析、初稿和批评意见，输出最终可复制的高质量 Prompt。",
    backstory=(
        "你负责把 Prompt 打磨到能直接使用。"
        "你的输出要自然、清楚、少废话，避免 AI 套话和过度格式化。"
    ),
    llm=llm,
    verbose=True,
)


# Task 1：分析需求
analyze_requirement_task = Task(
    description=(
        "用户想要生成一个 Prompt，原始需求如下：\n\n"
        "{user_goal}\n\n"
        "请先不要写最终 Prompt。你只需要分析需求。\n\n"
        "请输出：\n"
        "1. 用户真正想完成的任务\n"
        "2. 这个 Prompt 的目标用户\n"
        "3. AI 应该扮演什么角色\n"
        "4. 最终输出应该包含什么\n"
        "5. 有哪些容易翻车的点\n"
        "6. 这个 Prompt 应该避免什么语气或行为"
    ),
    expected_output=(
        "一份需求分析报告，要求清楚、具体、不要写成正式论文。"
    ),
    agent=requirement_analyst,
)


# Task 2：写 Prompt 初稿
draft_prompt_task = Task(
    description=(
        "根据前面的需求分析，写一版 Prompt 初稿。\n\n"
        "要求：\n"
        "1. 必须可直接复制使用\n"
        "2. 必须包含角色设定\n"
        "3. 必须包含任务目标\n"
        "4. 必须包含输入变量\n"
        "5. 必须包含输出格式\n"
        "6. 必须包含限制条件\n"
        "7. 如果涉及风险内容，要加入安全边界\n"
        "8. 不要写空泛套话"
    ),
    expected_output=(
        "一份 Prompt 初稿，格式清晰，可以直接给大模型使用。"
    ),
    agent=prompt_architect,
)


# Task 3：挑毛病
critic_prompt_task = Task(
    description=(
        "请严格审查前面的 Prompt 初稿。\n\n"
        "重点检查：\n"
        "1. 是否太泛\n"
        "2. 是否容易输出人机味\n"
        "3. 是否缺少关键限制\n"
        "4. 是否输出格式不够稳定\n"
        "5. 是否有安全风险\n"
        "6. 是否有废话、套话、过度礼貌\n"
        "7. 是否适合真实用户使用\n\n"
        "不要重写最终 Prompt，只负责指出问题和修改建议。"
    ),
    expected_output=(
        "一份 Prompt 审核报告，包含问题列表和具体修改建议。"
    ),
    agent=prompt_critic,
)


# Task 4：输出最终 Prompt
final_prompt_task = Task(
    description=(
        "根据需求分析、Prompt 初稿和审核意见，输出最终版本。\n\n"
        "最终输出必须包含：\n"
        "1. 最终 Prompt\n"
        "2. 使用方法\n"
        "3. 适合场景\n"
        "4. 不适合场景\n"
        "5. 可修改参数\n\n"
        "写作要求：\n"
        "1. 不要像官方客服\n"
        "2. 不要说“祝你成功”“希望对你有帮助”等套话\n"
        "3. 不要堆 emoji\n"
        "4. 不要废话太多\n"
        "5. 最终 Prompt 必须放在 Markdown 代码块里\n"
        "6. 最终 Prompt 要具体、自然、可复制"
    ),
    expected_output=(
        "一份最终可用的 Prompt 方案，其中最终 Prompt 必须能直接复制使用。"
    ),
    agent=prompt_optimizer,
)


crew = Crew(
    agents=[
        requirement_analyst,
        prompt_architect,
        prompt_critic,
        prompt_optimizer,
    ],
    tasks=[
        analyze_requirement_task,
        draft_prompt_task,
        critic_prompt_task,
        final_prompt_task,
    ],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff(inputs={"user_goal": user_goal})

os.makedirs("output", exist_ok=True)

with open("output/final_prompt.md", "w", encoding="utf-8") as f:
    f.write(str(result))

with open("output/result.md", "w", encoding="utf-8") as f:
    f.write(str(result))

print("\n====== 多 Agent Prompt 已保存到 output/final_prompt.md ======\n")
print(result)