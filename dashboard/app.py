import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="LLM-Bench",
    page_icon="🤖",
    layout="wide"
)
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)



RESULTS_PATH = "data/results/benchmark_results_reevaluated.csv"


@st.cache_data
def load_results():
    return pd.read_csv(RESULTS_PATH)


def main():

    st.title("🤖 LLM-Bench")
    st.caption(
        "Multi-Model LLM Evaluation & Benchmarking Framework"
    )

    df = load_results()

    # --------------------------------------------------
    # Sidebar
    # --------------------------------------------------

    st.sidebar.header("Filters")

    models = st.sidebar.multiselect(
        "Select Models",
        options=df["model"].unique(),
        default=df["model"].unique()
    )

    filtered_df = df[
        df["model"].isin(models)
    ]
    
    # --------------------------------------------------
    # Search Field
    # --------------------------------------------------
        
    search = st.text_input("Search questions or answers")
    
    if search:
        filtered_df = filtered_df[
            filtered_df["question_id"].astype(str).str.contains(
                search, case=False, na=False
            )
            | filtered_df["final_answer"].astype(str).str.contains(
                search, case=False, na=False
            )
        ]

    # --------------------------------------------------
    # Overview Metrics
    # --------------------------------------------------

    st.subheader("Benchmark Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Models",
            filtered_df["model"].nunique()
        )

    with col2:
        st.metric(
            "Evaluations",
            len(filtered_df)
        )

    with col3:
        avg_score = filtered_df[
            "evaluation_score"
        ].mean()

        st.metric(
            "Average Score",
            f"{avg_score * 100:.1f}%" if pd.notna(avg_score) else "No Data"
        )

    with col4:
        avg_latency = filtered_df[
            "latency"
        ].mean()

        st.metric(
            "Avg Latency",
            f"{avg_latency:.2f}s" if pd.notna(avg_latency) else "No Data"
        )

    st.divider()

    # --------------------------------------------------
    # Model Leaderboard
    # --------------------------------------------------

    st.subheader("🏆 Model Leaderboard")

    leaderboard = (
        filtered_df
        .groupby("model")
        .agg(
            Score=("evaluation_score", "mean"),
            Latency=("latency", "mean"),
            Output_Tokens=("output_tokens", "mean")
        )
        .reset_index()
    )

    leaderboard["Score"] *= 100

    leaderboard = leaderboard.rename(
        columns={
            "Score": "Score (%)",
            "Latency": "Avg Latency (s)",
            "Output_Tokens": "Avg Output Tokens"
        }
    )

    leaderboard["Score (%)"] = leaderboard["Score (%)"].round(1)
    leaderboard["Avg Latency (s)"] = leaderboard["Avg Latency (s)"].round(2)
    leaderboard["Avg Output Tokens"] = (
    leaderboard["Avg Output Tokens"].round(1)
    )

    st.dataframe(
        leaderboard,
        width="stretch",
        hide_index=True
    )

    # --------------------------------------------------
    # Charts
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Score Comparison")

        score_chart = (
            filtered_df
            .groupby("model")["evaluation_score"]
            .mean()
            .mul(100)
        )

        st.bar_chart(score_chart)

    with col2:

        st.subheader("Latency Comparison")

        latency_chart = (
            filtered_df
            .groupby("model")["latency"]
            .mean()
        )

        st.bar_chart(latency_chart)

    # --------------------------------------------------
    # Token Usage
    # --------------------------------------------------

    st.subheader("📊 Token Usage")

    token_chart = (
        filtered_df
        .groupby("model")["output_tokens"]
        .mean()
    )

    st.bar_chart(token_chart)

    # --------------------------------------------------
    # Detailed Results
    # --------------------------------------------------

    st.subheader("🔍 Detailed Results")

    display_columns = [
        "question_id",
        "model",
        "final_answer",
        "evaluation_score",
        "evaluation_status",
        "latency",
        "input_tokens",
        "output_tokens"
    ]

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True
    )
    
    # --------------------------------------------------
    # Evaluation filters
    # --------------------------------------------------
    
    categories = st.sidebar.multiselect(
    "Select Categories",
    options=sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
    )

    difficulties = st.sidebar.multiselect(
        "Select Difficulty",
        options=sorted(df["difficulty"].dropna().unique()),
        default=sorted(df["difficulty"].dropna().unique())
    )

    filtered_df = df[
        df["model"].isin(models)
        & df["category"].isin(categories)
        & df["difficulty"].isin(difficulties)
    ]


if __name__ == "__main__":
    main()