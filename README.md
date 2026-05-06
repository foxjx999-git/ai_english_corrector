# AI English Corrector

AI English Corrector 是一个面向中文学习者的 AI 英语纠错学习助手。

它不仅可以纠正英文句子，还可以解释错误原因、标记错误类型、保存练习记录，并支持复习和学习报告。

## 功能

- 输入英文句子，AI 自动纠错
- 使用简体中文解释错误原因
- 给出更自然的英文表达
- 自动标记错误类型
- 保存练习历史
- 查看常见错误统计
- 查看最近练习记录
- 随机复习错句
- 按错误类型复习
- AI 评价用户复习答案
- 生成学习报告
- 导出学习记录
- 清空历史记录
- 提供 Streamlit Web 页面

## 命令说明
- `help`：查看所有可用命令
- `stats`：查看常见错误统计
- `history`：查看最近练习记录
- `review`：随机复习一条错句
- `review grammar`：按语法错误复习
- `review punctuation`：按标点错误复习
- `review subject_verb_agreement`：按主谓一致错误复习
- `report`：生成学习报告
- `export`：导出学习记录到 `data/report.txt`
- `clear`：清空历史记录
- `q`：退出程序

## 项目结构

```text
ai_english_corrector/
├── app.py
├── main.py
├── corrector.py
├── prompts.py
├── openai_client.py
├── storage.py
├── analyzer.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    ├── history.jsonl
    └── report.txt
```
说明：

- `.env` 文件用于保存本地 API Key，不应该上传到 GitHub。
- `data/` 文件夹用于保存本地练习记录，运行程序后自动生成。

## 文件说明
- `app.py`：Streamlit Web 版入口，负责网页界面展示
- `main.py`：程序入口，负责命令行交互和命令分发
- `corrector.py`：负责英文纠错和 review 答案评价
- `prompts.py`：管理发送给 AI 的 prompt
- `openai_client.py`：封装 OpenAI API 调用
- `storage.py`：负责保存、读取、清空和导出练习记录
- `analyzer.py`：负责错误统计、历史分析和学习报告数据生成
- `requirements.txt`：记录项目依赖
- `.gitignore`：配置不上传到 GitHub 的文件
- `data/history.jsonl`：保存每次练习记录
- `data/report.txt`：导出的学习记录

## 安装与运行

### 1. 先创建并激活虚拟环境。

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```


### 2. 安装依赖

```bash
pip install -r requirements.txt
```


### 3. 配置 API Key

在项目根目录创建 `.env` 文件：
```env
OPENAI_API_KEY=your_api_key_here
```
注意：不要把 `.env` 上传到 GitHub。

### 4. 运行项目

命令行版：

```bash
python main.py
```
Streamlit Web 版：

```bash
streamlit run app.py
```

运行后可以直接输入英文句子，或者输入命令，例如：
```text
help
stats
history
review
report
export
q
```

## Web 版功能

````markdown
Streamlit Web 版支持以下页面：

- `Correct`：输入英文句子，AI 自动纠错并保存记录
- `Stats`：查看错误统计表格和柱状图
- `History`：查看最近练习记录
- `Report`：查看学习报告和推荐复习方向
- `Review`：随机或按错误类型复习错句，并由 AI 评价答案
- `Manage`：导出或清空本地学习记录
```

## 示例

输入：

```text
i very like this movie
```

输出示例：

```text
Original:
i very like this movie

Corrected:
I really like this movie.

Explanation:
原句中 “i” 需要大写为 “I”。另外，“very” 不能直接修饰动词 “like”。

More Natural:
I like this movie very much.

Error Type:
capitalization, word_choice, grammar

Suggestion:
注意人称代词 I 永远大写，并积累 really like / like ... very much 这类自然表达。
```

## Review 复习模式示例

输入：
```text
review grammar
```

程序会随机抽取一条语法错误记录，让用户先尝试修改，然后由 AI 评价修改结果。

示例：

```text
原句:
i am agree with you

请你先尝试修改这句话:
I agree with you

AI 评价:
你的句子语法正确，但句末建议加句号，使书面表达更规范。

评分:
90/100

是否完全正确:
否

更好的答案:
I agree with you.
```

## 学习报告示例

输入：

```text
report
```

输出示例：

```text
学习报告：

总练习次数：3

最常见错误 Top 3：
1. capitalization (大小写错误): 3 次
2. grammar (语法错误): 2 次
3. punctuation (标点错误): 2 次

学习建议：
你最近最常出现的是大小写错误。建议重点注意句首大写，以及人称代词 I 永远大写。

推荐下一步：
输入 review capitalization 复习大小写错误。
```

## 当前版本

V2.8 Streamlit Web 版基础功能完成。

## 后续计划

- 增加 Web 版 Review 页面更多交互优化
- 使用 SQLite 保存练习数据
- 支持更完整的学习报告
- 增加用户学习进度追踪
- 增加项目截图
- 部署到线上