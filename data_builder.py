import requests
import json
import os
import sys
import pandas as pd
from typing import Optional

# ==========================================
# 1. API 配置（从环境变量读取，运行前请先设置）
# ==========================================
# 设置方式（终端中执行）:
#   export POLICY_API_KEY="sk-xxx"
#   export POLICY_API_URL="https://open.bigmodel.cn/api/paas/v4/chat/completions"
#   export POLICY_MODEL_NAME="glm-4"
# 或者直接在下面修改默认值:

API_KEY = os.environ.get("POLICY_API_KEY", "sk-在此处填入你的真实API_KEY")
API_URL = os.environ.get("POLICY_API_URL", "替换成你选择的大模型接口地址")
MODEL_NAME = os.environ.get("POLICY_MODEL_NAME", "替换成模型名称，比如 glm-4 或 qwen-plus")

# ==========================================
# 2. 示例政策文本（可从政府网站复制原文替换）
# ==========================================
raw_policy_text = """
关于印发《本市青年见习计划实施办法》的通知。为促进青年就业，决定实施青年见习计划。
适用对象：年龄在 16至25周岁 的本市户籍失业青年，或本市普通高等学校毕业学年的在校学生。
补贴标准：见习期间，按本市当年城镇职工月最低工资标准的 80% 给予生活费补贴（当前约 2000元/月）。
注意：申请人不得有正式工作，需处于待业状态或为在校学生。无收入限制要求。
"""

# ==========================================
# 3. Prompt 模板（让 AI 变成基层治理专家）
# ==========================================
system_prompt = """
你是一个专业的公共政策分析师和数据提取工程师。
请阅读用户提供的政策原文，提取核心要素，并严格按照以下 JSON 格式输出，不要输出任何额外的解释文本或 Markdown 标记。

必须输出的 JSON 字段如下：
{
    "id": "随机生成一个以P开头的编号，如P015",
    "name": "政策的简短名称",
    "category": "从[就业创业, 民生保障, 养老服务, 住房补贴]中选一个",
    "description": "用一句话概括政策内容",
    "condition_age_min": 最小年龄数字(不限填0),
    "condition_age_max": 最大年龄数字(不限填120),
    "condition_status": "从[学生/应届生, 在职, 待业/灵活就业, 退休]中选择适用身份，如果有多个请用分号隔开，如'学生/应届生;待业/灵活就业'",
    "condition_income_max": 最高月收入限制数字(不限填999999),
    "condition_hukou": "填写'是'或'否'，表示该政策是否要求本市户籍",
    "amount": "提取具体的补贴金额或福利内容，如'2000元/月'"
}
"""

# ==========================================
# 4. 核心提取函数（带重试机制）
# ==========================================
def extract_policy_data(text: str, max_retries: int = 3) -> Optional[dict]:
    """调用大模型提取政策结构化数据，失败时自动重试。"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    for attempt in range(1, max_retries + 1):
        print(f"🚀 正在请求大模型提取数据... (第 {attempt}/{max_retries} 次)")

        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json={
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"请提取以下政策文本:\n{text}"}
                    ],
                    "temperature": 0.1
                },
                timeout=60
            )

            if response.status_code == 200:
                result_text = response.json()['choices'][0]['message']['content']
                result_text = result_text.replace("```json", "").replace("```", "").strip()

                try:
                    data = json.loads(result_text)
                    # 验证必填字段
                    required_fields = [
                        "id", "name", "category", "description",
                        "condition_age_min", "condition_age_max",
                        "condition_status", "condition_income_max",
                        "condition_hukou", "amount"
                    ]
                    missing = [f for f in required_fields if f not in data]
                    if missing:
                        print(f"⚠️ 返回数据缺少字段: {missing}，尝试重试...")
                        continue

                    print("✅ 提取成功！\n", json.dumps(data, indent=4, ensure_ascii=False))
                    return data

                except json.JSONDecodeError:
                    print(f"❌ 解析 JSON 失败，大模型返回格式不标准: {result_text}")
                    if attempt < max_retries:
                        print("🔄 正在重试...")
                    continue
            else:
                print(f"❌ API 请求失败，状态码：{response.status_code}")
                print(response.text[:500])
                if attempt < max_retries:
                    print("🔄 正在重试...")

        except requests.exceptions.Timeout:
            print(f"❌ 请求超时（60秒）")
        except requests.exceptions.ConnectionError:
            print(f"❌ 网络连接失败，请检查 API_URL 是否正确")
            break  # 网络错误不重试
        except Exception as e:
            print(f"❌ 未知错误: {e}")

    return None


# ==========================================
# 5. CSV 保存函数
# ==========================================
def save_to_csv(data_list: list, filepath: str = "policies.csv") -> None:
    """保存政策数据到 CSV 文件，自动处理新文件创建和追加。"""
    if not data_list:
        print("⚠️ 没有数据可保存")
        return

    df = pd.DataFrame(data_list)
    file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0

    # 确保列顺序一致
    column_order = [
        "id", "name", "category", "description",
        "condition_age_min", "condition_age_max", "condition_status",
        "condition_income_max", "condition_hukou", "amount"
    ]
    df = df[[c for c in column_order if c in df.columns]]

    df.to_csv(
        filepath,
        mode='a',
        index=False,
        header=not file_exists,
        encoding='utf-8'
    )
    print(f"🎉 已保存 {len(df)} 条记录到 {filepath}")


# ==========================================
# 6. 主入口
# ==========================================
def main():
    # 检查 API 配置
    if "在此处填入" in API_KEY or "替换成" in API_URL or "替换成" in MODEL_NAME:
        print("=" * 50)
        print("⚠️  请先配置 API 参数！")
        print("")
        print("方式一（推荐）：设置环境变量")
        print("  export POLICY_API_KEY=\"sk-xxx\"")
        print("  export POLICY_API_URL=\"https://...\"")
        print("  export POLICY_MODEL_NAME=\"glm-4\"")
        print("")
        print("方式二：直接修改本文件顶部的 API_KEY / API_URL / MODEL_NAME")
        print("=" * 50)
        sys.exit(1)

    extracted_data = extract_policy_data(raw_policy_text)

    if extracted_data:
        save_to_csv([extracted_data])
    else:
        print("❌ 数据提取失败，请检查 API 配置和网络连接")
        sys.exit(1)


if __name__ == "__main__":
    main()
