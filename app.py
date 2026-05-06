import streamlit as st
import pandas as pd
import altair as alt

from corrector import correct_english, evaluate_review_answer
from storage import save_record, export_records, clear_records
from analyzer import (analyze_error_types, 
                      get_error_type_label, 
                      get_recent_records, 
                      generate_learning_report,
                      get_random_record,
                      get_random_record_by_error_type
                      )




st.set_page_config(
    page_title="AI English Corrector",
    page_icon="📘",
    layout="centered"
)

page = st.sidebar.radio(
    "请选择功能：",
    ["Correct", "Stats", "History", "Report", "Review", "Manage"]
)

if page == "Correct":
    st.title("📘 AI English Corrector")
    st.write("面向中文学习者的 AI 英语纠错助手")

    sentence = st.text_area(
        "请输入一句英文：",
        height=120,
        placeholder="例如：i very like this movie"
    )

    if st.button("开始纠错"):

        if not sentence.strip():
            st.warning("请先输入一句英文。")
        else:
            with st.spinner("AI 正在纠错中..."):
                result = correct_english(sentence.strip())

            st.markdown("### ✅ 纠错结果")

            st.write(f"**原句：** {result['original']}")

            if result["success"]:
                st.success(f"**修改后：** {result['corrected']}")

                st.info(f"**更自然表达：** {result['natural_expression']}")

                error_types = ", ".join(result["error_type"])
                st.write(f"**错误类型：** `{error_types}`")

                with st.expander("📘 查看错误解释"):
                    st.write(result["explanation"])

                with st.expander("🎯 查看学习建议"):
                    st.write(result["suggestion"])

                save_record(result)
                st.toast("本次练习记录已保存。", icon="✅")

            else:
                st.error("程序出错了：")
                st.write(result["error"])

elif page == "Stats":
    st.title("📊 错误统计")
    st.write("查看你最近最常见的英文错误类型。")

    stats = analyze_error_types()

    if not stats:
        st.info("暂无练习记录。请先完成几次英文纠错。")
    else:
        data = []
        for error_type, count in stats:
            label = get_error_type_label(error_type)
            data.append({
                "错误类型": error_type,
                "中文说明": label,
                "次数": count
            })

        df = pd.DataFrame(data)

        st.metric("错误类型数量", len(df))

        st.subheader("错误类型明细")
        st.dataframe(df, use_container_width=True)

        st.subheader("错误次数图表")
        '''
        chart_data = df.set_index("中文说明")["次数"]
        st.bar_chart(chart_data)
        '''

        chart = (
            alt.Chart(df)
            .mark_bar(size=30)
            .encode(
                x=alt.X("中文说明:N", title="错误类型", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("次数:Q", title="次数"),
                tooltip=["错误类型", "中文说明", "次数"]
            )
        )

        st.altair_chart(chart, use_container_width=True)


elif page == "History":
    st.title("📜 最近练习记录")
    st.write("查看最近保存的英语练习记录。")

    limit = st.selectbox(
        "显示最近几条记录：",
        [5, 10, 20],
        index=0
    )

    records = get_recent_records(limit=limit)

    #records = get_recent_records()

    if not records:
        st.info("暂无练习记录。请先完成几次英文纠错。")
    else:
        for index, record in enumerate(records, start=1):
            error_types = record.get("error_type", [])

            if isinstance(error_types, str):
                error_types = [error_types]

            with st.container(border=True):
                st.markdown(f"### 记录 {index}")
                st.caption(record.get("time", "未知时间"))

                st.write(f"**原句：** {record.get('original', '')}")
                st.success(f"**修改后：** {record.get('corrected', '')}")

                st.write(f"**错误类型：** `{', '.join(error_types)}`")

                with st.expander("📘 查看错误解释"):
                    st.write(record.get("explanation", ""))

                with st.expander("🎯 查看学习建议"):
                    st.write(record.get("suggestion", ""))


elif page == "Report":
    st.title("📈 学习报告")
    st.write("根据你的练习记录，生成阶段性学习分析。")

    report = generate_learning_report()

    if not report:
        st.info("暂无练习记录，先输入几句英文进行练习吧。")
    else:
        top_error = report["top_error"]
        top_error_label = get_error_type_label(top_error) if top_error else "暂无"

        col1, col2 = st.columns(2)

        with col1:
            st.metric("总练习次数", report["total_records"])

        with col2:
            st.metric("最常见错误", top_error_label)

        st.subheader("最常见错误 Top 3")

        top_stats = report["stats"][:3]

        for index, item in enumerate(top_stats, start=1):
            error_type = item[0]
            count = item[1]
            label = get_error_type_label(error_type)

            with st.container(border=True):
                st.write(f"**{index}. {error_type}（{label}）**")
                st.progress(min(count / report["total_records"], 1.0))
                st.caption(f"出现 {count} 次")

        latest_record = report["latest_record"]

        st.subheader("最近一次练习")

        with st.container(border=True):
            st.write(f"**原句：** {latest_record.get('original', '')}")
            st.success(f"**修改后：** {latest_record.get('corrected', '')}")

            error_types = latest_record.get("error_type", [])

            if isinstance(error_types, str):
                error_types = [error_types]

            st.write(f"**错误类型：** `{', '.join(error_types)}`")

        st.subheader("学习建议")

        if top_error == "capitalization":
            suggestion = "你最近最常出现的是大小写错误。建议重点注意句首大写，以及人称代词 I 永远大写。"
        elif top_error == "subject_verb_agreement":
            suggestion = "你最近主谓一致错误比较多。建议重点复习 he/she/it 后面的一般现在时动词加 -s/-es。"
        elif top_error == "punctuation":
            suggestion = "你最近标点问题比较多。建议每次写完英文句子后，检查句末是否有 . ? !。"
        elif top_error == "word_choice":
            suggestion = "你最近用词错误比较多。建议多积累自然表达，比如 really like、agree with、be interested in 等固定搭配。"
        elif top_error == "grammar":
            suggestion = "你最近语法错误比较多。建议先复习最常见句型：主语 + 动词 + 宾语，以及 be 动词和实义动词不要乱搭。"
        else:
            suggestion = "继续保持练习。建议你多用 review 模式复习之前的错句。"

        st.info(suggestion)

        if top_error:
            st.success(f"推荐下一步：复习 {top_error}（{top_error_label}）类型错误。")


elif page == "Review":
    st.title("🧠 错句复习")
    st.write("从历史记录中抽取错句，先自己修改，再让 AI 评价你的答案。")

    review_options = {
        "全部错误": None,
        "大小写错误": "capitalization",
        "语法错误": "grammar",
        "用词错误": "word_choice",
        "主谓一致错误": "subject_verb_agreement",
        "标点错误": "punctuation",
        "中式英语": "chinese_english",
        "其他错误": "other"
    }

    selected_label = st.selectbox(
        "选择复习类型：",
        list(review_options.keys())
    )

    selected_error_type = review_options[selected_label]

    if "review_record" not in st.session_state:
        st.session_state.review_record = None

    if st.button("抽取错句"):
        if selected_error_type:
            record = get_random_record_by_error_type(selected_error_type)
        else:
            record = get_random_record()

        st.session_state.review_record = record
        st.session_state.review_result = None

    record = st.session_state.review_record

    if not record:
        st.info("请先点击“抽取错句”。如果没有记录，请先完成几次英文纠错。")
    else:
        with st.container(border=True):
            st.subheader("本次复习句子")
            st.write(f"**原句：** {record.get('original', '')}")

            error_types = record.get("error_type", [])
            if isinstance(error_types, str):
                error_types = [error_types]

            st.write(f"**错误类型：** `{', '.join(error_types)}`")

        user_answer = st.text_area(
            "请你先尝试修改这句话：",
            height=100,
            placeholder="在这里输入你的修改版本"
        )

        if st.button("提交答案"):
            if not user_answer.strip():
                st.warning("请先输入你的修改答案。")
            else:
                with st.spinner("AI 正在评价你的答案..."):
                    review_result = evaluate_review_answer(
                        record.get("original", ""),
                        user_answer.strip(),
                        record.get("corrected", ""),
                        record.get("explanation", "")
                    )

                st.session_state.review_result = review_result
                st.session_state.user_answer = user_answer.strip()

        review_result = st.session_state.get("review_result")

        if review_result:
            st.subheader("AI 评价结果")

            st.write(f"**你的修改：** {st.session_state.get('user_answer', '')}")
            st.write(f"**参考答案：** {record.get('corrected', '')}")

            if review_result["success"]:

                #st.metric("评分", f"{review_result['score']}/100")
                score = review_result["score"]

                if score >= 95:
                    st.success(f"评分：{score}/100")
                elif score >= 80:
                    st.warning(f"评分：{score}/100")
                else:
                    st.error(f"评分：{score}/100")


                if review_result["is_correct"]:
                    st.success("是否完全正确：是")
                else:
                    st.warning("是否完全正确：否")

                st.info(review_result["feedback"])

                missing_points = review_result["missing_points"]

                with st.expander("仍需注意", expanded=True):
                    if missing_points:
                        for point in missing_points:
                            st.write(f"- {point}")
                    else:
                        st.write("没有明显问题。")

                st.success(f"更好的答案：{review_result['better_answer']}")
            else:
                st.error("AI 评价失败：")
                st.write(review_result["error"])

elif page == "Manage":
    st.title("⚙️ 数据管理")
    st.write("导出或清空本地学习记录。")

    st.subheader("导出学习记录")

    st.write("将当前历史记录导出到 `data/report.txt`。")

    if st.button("导出记录"):
        success = export_records()

        if success:
            st.success("学习记录已导出到 data/report.txt")
        else:
            st.info("暂无练习记录，无法导出。")

    st.divider()

    st.subheader("清空历史记录")

    st.warning("清空后，所有练习历史、统计和报告都会被清除。")

    confirm_clear = st.checkbox("我确认要清空所有练习记录")

    if st.button("清空记录"):
        if confirm_clear:
            clear_records()

            st.session_state.review_record = None
            st.session_state.review_result = None
            st.session_state.user_answer = ""

            st.success("所有练习记录已清空。")
        else:
            st.warning("请先勾选确认框。")