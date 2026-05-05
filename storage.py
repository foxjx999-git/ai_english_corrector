import json
from datetime import datetime
from pathlib import Path


DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "history.jsonl"


def save_record(result):
    DATA_DIR.mkdir(exist_ok=True)

    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original": result["original"],
        "corrected": result["corrected"],
        "explanation": result["explanation"],
        "natural_expression": result["natural_expression"],
        "error_type": result["error_type"],
        "suggestion": result["suggestion"]
    }

    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")

def load_records():
    if not HISTORY_FILE.exists():
        return []

    records = []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                record = json.loads(line)
                records.append(record)

    return records

def clear_records():
    if HISTORY_FILE.exists():
        HISTORY_FILE.write_text("", encoding="utf-8")


def export_records():
    records = load_records()

    if not records:
        return False

    DATA_DIR.mkdir(exist_ok=True)

    export_file = DATA_DIR / "report.txt"

    with open(export_file, "w", encoding="utf-8") as file:
        file.write("AI English Corrector 学习记录\n\n")
        file.write(f"总练习次数：{len(records)}\n\n")

        for index, record in enumerate(records, start=1):
            error_types = record.get("error_type", [])

            if isinstance(error_types, str):
                error_types = [error_types]

            file.write(f"{index}. 时间：{record.get('time', '未知时间')}\n")
            file.write(f"原句：{record.get('original', '')}\n")
            file.write(f"修改：{record.get('corrected', '')}\n")
            file.write(f"错误类型：{', '.join(error_types)}\n")
            file.write(f"建议：{record.get('suggestion', '')}\n")
            file.write("\n")

    return True