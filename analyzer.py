from collections import Counter
from storage import load_records
import random

ERROR_TYPE_LABELS = {
    "capitalization": "大小写错误",
    "grammar": "语法错误",
    "word_choice": "用词错误",
    "subject_verb_agreement": "主谓一致错误",
    "punctuation": "标点错误",
    "chinese_english": "中式英语",
    "other": "其他错误"
}

def get_error_type_label(error_type):
    return ERROR_TYPE_LABELS.get(error_type, "未知错误")

def analyze_error_types():
    records = load_records()

    counter = Counter()

    for record in records:
        error_types = record.get("error_type", [])

        if isinstance(error_types, str):
            error_types = [error_types]

        counter.update(error_types)

    return counter.most_common()

def get_recent_records(limit=5):
    records = load_records()

    recent_records = records[-limit:]

    recent_records.reverse()

    return recent_records

def get_latest_record():
    records = load_records()

    if not records:
        return None
    return records[-1]

def get_random_record():
    records = load_records()
    if not records:
        return None
    return random.choice(records)

def get_random_record_by_error_type(target_error_type):
    records = load_records()

    match_records = []

    for record in records:
        error_types = record.get("error_type",[])

        if isinstance(error_types,str):
            error_types = [error_types]

        if target_error_type in error_types:
            match_records.append(record)
    if not match_records:
        return None
    return random.choice(match_records)

def generate_learning_report():
    records =load_records()
    if not records:
        return None
    
    stats = analyze_error_types()

    latest_record = records[-1]

    top_error = stats[0][0] if stats else None
    top_error_count = stats[0][1] if stats else 0

    return {
        "total_records": len(records),
        "stats": stats,
        "latest_record": latest_record,
        "top_error": top_error,
        "top_error_count": top_error_count
    }