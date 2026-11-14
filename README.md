# 学生成绩统计系统

> 当前版本：v0.1

一个命令行工具：从 JSON 文件读取学生成绩，统计平均分、最高最低分和
及格人数，支持按学号查询，并可将结果导出为文本报告。

## 功能

- 从 `data/students.json` 加载学生数据
- 自动校验每条记录：学号、姓名不能为空，成绩须为 0~100 的数字
- 非法记录自动跳过并给出警告，不影响其余数据加载
- 文件缺失、数据为空或 JSON 格式错误时给出明确提示，程序不会崩溃
- 仅支持 UTF-8 编码的数据文件（其他编码会抛 `UnicodeDecodeError`，见「已知限制」）
- 统计平均分、最高分、最低分、及格人数（及格线 60）
- 按学号查询某个学生的成绩（查不到时提示“未查询到该学生，请重新输入”）
- 通过菜单导出统计结果到 `output/report.txt`

## 运行方式

环境：Python **3.10 及以上**。代码使用了 `match` 语句，3.9 及以下会直接报错
`SyntaxError: invalid syntax` —— 是文件根本解析不了，不是运行出错。
可用 `python --version` 确认版本；Windows 若要精确指定版本，用 `py -3.14 -V`
这种写法（`py -0` 可列出本机所有已安装的 Python 版本）。

运行程序**不需要任何第三方库**，只用 Python 标准库。

`requirements.txt` 中列出的是**开发依赖**（`pytest`，用于将来编写自动化测试），
当前仓库暂无测试用例，运行程序无需安装。

```bash
git clone https://github.com/John-Z26/student-statistics.git
cd student-statistics

# 可选但推荐：建独立环境（固定 Python 版本）
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1     # PowerShell；Git Bash 用 source .venv/Scripts/activate

python src/run.py

```

> 注意：必须在项目根目录运行，程序使用相对路径读取 `data/students.json`。
> 导出报告时会自动创建 `output/` 目录，无需手动新建。

## 数据格式

`data/students.json` 是一个数组，每个元素包含学号、姓名、成绩：

```json
[
   {
      "id": "2026001",
      "name": "Alice",
      "score": 92
   },
   {
      "id": "2026002",
      "name": "Bob",
      "score": 76
   }
]
```

字段说明：

- `id`：学生学号，唯一标识一条记录
- `name`：学生姓名，不能为空
- `score`：学生成绩，0~100 的数字，可以是小数

校验规则：

- `id`、`name` 缺失或为空白（包括只有空格）的记录会被跳过，并输出警告
- `score` 不是数字、或不在 0~100 之间的记录会被跳过，并输出警告
- 学号重复时，后一条记录覆盖前一条
- `id`、`name` 会自动去除首尾空格；`id` 写成数字也能被接受（会转为字符串），
  但数字 `0` 除外，会被视为缺少学号而跳过

以下数据可用于验证上述规则，预期只有第 4 条正常加载：

```json
[
  {"id": "", "name": "A", "score": 92},
  {"id": "2", "name": "B", "score": "abc"},
  {"id": "3", "name": "C", "score": 120},
  {"id": "4", "name": "D", "score": 66}
]
```

## 输出示例

程序运行后：

```text
学生信息加载完成，共 2 条有效记录
欢迎使用教务系统~

1.查询考试平均分
2.查询考试最高分和最低分
3.查询及格人数
4.查询指定学生成绩
5.查询所有学生成绩
6.输出并打印统计结果
7.退出系统

请输入您的操作(1-7):
```

选 6 时屏幕会先显示统计结果，随后生成文件 `output/report.txt`：

```text
学生成绩统计报告
====================
学生总人数:2
及格人数:2
平均分:84.00
最高分:Alice 92
最低分:Bob 76
```

## 如何测试

本节为手工验收步骤，按顺序执行可覆盖全部功能与异常分支：

1. 把「数据格式」中的验证数据替换进 `data/students.json`
2. 在项目根目录运行 `python src/run.py`
3. 预期看到 3 条警告（缺少学号 / 成绩不是数字 / 成绩超出范围），
   并显示「学生信息加载完成，共 1 条有效记录」
4. 依次选择菜单 1–5，检查平均分、最高最低分、及格人数、
   按学号查询、全部学生名单是否正确。
   其中菜单 4 会额外要求输入学号，
   输入 `4`（验证数据里唯一有效的学号），
   预期显示「学号：4,姓名：D,成绩：66」
5. 输入 `7` 退出程序，执行 `git checkout -- data/students.json` 还原示例数据
   （若是下载 ZIP 获取的，改回第 1 步前备份的内容）
6. 重新运行 `python src/run.py` 并选择菜单 6，
   检查 `output/report.txt` 是否自动生成、内容是否与「输出示例」一致

## 项目结构

```text
student-statistics/
├── src/
│   ├── run.py           # 程序入口，创建 StudentSystem 并调用 run()
│   └── models.py        # Students 类（单条记录）/ StudentSystem 类（业务逻辑）
├── data/
│   └── students.json    # 学生数据（输入文件，手动维护）
├── output/              # 运行后自动创建
│   └── report.txt       # 统计报告（生成物，可随时删除）
├── requirements.txt     # 依赖清单（运行程序无需第三方库）
├── .gitignore
└── README.md
```

## 已知限制

- 数据字段固定为 `id` / `name` / `score`，多余字段会被忽略
- 数据文件必须为 UTF-8 编码，其他编码会报 `UnicodeDecodeError`
- 程序使用相对路径读取数据，必须在项目根目录（`student-statistics` 文件夹）运行
- 仅支持读取和统计，暂不支持修改、删除学生数据

