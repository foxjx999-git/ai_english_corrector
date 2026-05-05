from corrector import correct_english,evaluate_review_answer
from storage import save_record,clear_records,export_records
from analyzer import (
    analyze_error_types, 
    get_error_type_label, 
    get_recent_records, 
    get_latest_record,
    get_random_record,
    get_random_record_by_error_type,
    generate_learning_report)


def show_stats():
    stats = analyze_error_types()

    print("\n你的常见错误统计：")

    if not stats:
        print("暂无练习记录。")
    else:
        for error_type, count in stats:
            label = get_error_type_label(error_type)
            print(f"{error_type} ({label}): {count} 次")


def show_report():
    report = generate_learning_report()

    if not report:
        print("\n暂无练习记录，先输入几句英文进行练习吧。")
        return

    print("\n学习报告：")

    print(f"\n总练习次数：{report['total_records']}")

    """
    print("\n最常见错误：")
    for index, item in enumerate(report["stats"], start=1):
        error_type = item[0]
        count = item[1]
        label = get_error_type_label(error_type)
        print(f"{index}. {error_type} ({label}): {count} 次")
    """

    print("\n最常见错误 Top 3：")

    top_stats = report["stats"][:3]

    for index, item in enumerate(top_stats, start=1):
        error_type = item[0]
        count = item[1]
        label = get_error_type_label(error_type)
        print(f"{index}. {error_type} ({label}): {count} 次")

    latest_record = report["latest_record"]

    print("\n最近一次练习：")
    print(f"原句: {latest_record.get('original', '')}")
    print(f"修改: {latest_record.get('corrected', '')}")

    top_error = report["top_error"]

    print("\n学习建议：")

    if top_error == "capitalization":
        print("你最近最常出现的是大小写错误。建议重点注意句首大写，以及人称代词 I 永远大写。")
    elif top_error == "subject_verb_agreement":
        print("你最近主谓一致错误比较多。建议重点复习 he/she/it 后面的一般现在时动词加 -s/-es。")
    elif top_error == "punctuation":
        print("你最近标点问题比较多。建议每次写完英文句子后，检查句末是否有 . ? !。")
    elif top_error == "word_choice":
        print("你最近用词错误比较多。建议多积累自然表达，比如 really like、agree with、be interested in 等固定搭配。")
    elif top_error == "grammar":
        print("你最近语法错误比较多。建议先复习最常见句型：主语 + 动词 + 宾语，以及 be 动词和实义动词不要乱搭。")
    else:
        print("继续保持练习。建议你多用 review 模式复习之前的错句。")

    if top_error:
        top_error_label = get_error_type_label(top_error)

        print("\n推荐下一步：")
        print(f"输入 review {top_error} 复习{top_error_label}。")




def show_history():
    records = get_recent_records()

    print("\n最近练习记录：")

    if not records:
        print("暂无练习记录。")
    else:
        for index, record in enumerate(records, start=1):
            error_types = record.get("error_type", [])

            if isinstance(error_types, str):
                error_types = [error_types]

            print(f"\n{index}. 时间: {record.get('time', '未知时间')}")
            print(f"   原句: {record.get('original', '')}")
            print(f"   修改: {record.get('corrected', '')}")
            print(f"   错误类型: {', '.join(error_types)}")


def clear_history():
    confirm = input("\n确定要清空所有练习记录吗？输入 yes 确认：")

    if confirm.strip().lower() == "yes":
        clear_records()
        print("\n所有练习记录已清空。")
    else:
        print("\n已取消清空操作。")




def show_review():
    record =get_random_record()

    if not record:
        print("\n暂无练习记录，先输入一句英文进行纠错吧。")
        return
    
    print("\n随机复习一条错句：")
    print(f"\n原句：{record.get('original', '')}")


    user_answer = input("\n请你先尝试修改这句话：").strip()

    review_result = evaluate_review_answer(
        record.get("original", ""),
        user_answer,
        record.get("corrected", ""),
        record.get("explanation", "")

    )

    if review_result["success"]:
        print("\nAI 评价:")
        print(review_result["feedback"])

        print("\n评分:")
        print(f"{review_result['score']}/100")

        print("\n是否完全正确:")
        print("是" if review_result["is_correct"] else "否")

        print("\n仍需注意:")
        missing_points = review_result["missing_points"]

        if missing_points:
            for point in missing_points:
                print(f"- {point}")
        else:
            print("没有明显问题。")

        print("\n更好的答案:")
        print(review_result["better_answer"])

    else:
        print("\nAI 评价失败：")
        print(review_result["error"])

def show_review_by_error_type(error_type):
    record = get_random_record_by_error_type(error_type)

    if not record:
        print(f"\n暂无 {error_type} 类型的练习记录。")
        return

    print(f"\n随机复习一条 {error_type} 错误：")
    print(f"\n原句: {record.get('original', '')}")

    user_answer = input("\n请你先尝试修改这句话：").strip()

    review_result = evaluate_review_answer(
        record.get("original", ""),
        user_answer,
        record.get("corrected", ""),
        record.get("explanation", "")
    )

    print("\n你的修改:")
    print(user_answer)

    print("\n参考答案:")
    print(record.get("corrected", ""))

    if review_result["success"]:
        print("\nAI 评价:")
        print(review_result["feedback"])

        print("\n评分:")
        print(f"{review_result['score']}/100")

        print("\n是否完全正确:")
        print("是" if review_result["is_correct"] else "否")

        print("\n仍需注意:")
        missing_points = review_result["missing_points"]

        if missing_points:
            for point in missing_points:
                print(f"- {point}")
        else:
            print("没有明显问题。")

        print("\n更好的答案:")
        print(review_result["better_answer"])

    else:
        print("\nAI 评价失败：")
        print(review_result["error"])

def show_correction_result(result):
    print("\nOriginal:")
    print(result["original"])

    if result["success"]:
        print("\nCorrected:")
        print(result["corrected"])

        print("\nExplanation:")
        print(result["explanation"])

        print("\nMore Natural:")
        print(result["natural_expression"])

        print("\nError Type:")
        print(", ".join(result["error_type"]))

        print("\nSuggestion:")
        print(result["suggestion"])
    else:
        print("\n程序出错了：")
        print(result["error"])

def export_history():
    success = export_records()

    if success:
        print("\n学习记录已导出到 data/report.txt")
    else:
        print("\n暂无练习记录，无法导出。")


def show_help():
    print("\n可用命令：")
    print("stats                 查看错误统计")
    print("history               查看最近练习记录")
    print("review                随机复习一条错句")
    print("review grammar         按错误类型复习语法错误")
    print("review punctuation     按错误类型复习标点错误")
    print("review subject_verb_agreement  按错误类型复习主谓一致错误")
    print("report                查看学习报告")
    print("export                导出学习记录")
    print("clear                 清空练习记录")
    print("q                     退出程序")


def handle_sentence(sentence):
    result = correct_english(sentence)

    show_correction_result(result)

    if result["success"]:
        save_record(result)
        print("\n本次练习记录已保存。")


def main():
    while True:
        sentence = input("\n请输入一句英文，输入 stats 查看统计，输入 history 查看历史，输入 review 复习，输入 report 查看学习报告，输入 export 导出记录，输入 clear 清空记录，输，入 help 查看命令输入 q 退出：")

        command = sentence.strip().lower()

        if command == "q":
            print("程序已退出。")
            break

        if command == "stats":
            show_stats()
            continue

        if command == "history":
            show_history()
            continue

        if command.startswith("review"):
            parts = command.split()

            if len(parts) == 1:
                show_review()
            elif len(parts) == 2:
                error_type = parts[1]
                show_review_by_error_type(error_type)
            else:
                print("\n命令格式不正确。可以输入：review 或 review grammar")

            continue

        if command == "report":
            show_report()
            continue
        
        if command == "clear":
            clear_history()
            continue

        if command == "export":
            export_history()
            continue

        if command == "help":
            show_help()
            continue


        handle_sentence(sentence)


main()