import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

DATA_PATH = "/Users/akashsingh/Downloads/banking_transactions.csv"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def plot_histograms(df: pd.DataFrame, numeric_cols: list):
    n_cols = 2
    n_rows = int(np.ceil(len(numeric_cols) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(10, 4 * n_rows))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        axes[i].hist(df[col].dropna(), bins=30, color="#1f77b4", edgecolor="black")
        axes[i].set_title(col)
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Frequency")
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    fig.tight_layout()
    return fig


def plot_correlation(df: pd.DataFrame, numeric_cols: list):
    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.matshow(corr, cmap="coolwarm")
    fig.colorbar(cax)
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha="left")
    ax.set_yticklabels(numeric_cols)
    ax.set_title("Correlation Matrix", pad=20)
    return fig


def main():
    st.title("Banking Transactions EDA")
    st.markdown(f"**Data path:** `{DATA_PATH}`")

    df = load_data(DATA_PATH)

    st.header("Dataset Preview")
    st.dataframe(df.head(20))

    st.header("Basic Information")
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")

    st.subheader("Column Types")
    st.write(df.dtypes)

    st.subheader("Summary Statistics")
    st.write(df.describe(include="all"))

    st.subheader("Missing Values")
    missing = df.isna().sum()
    st.write(missing[missing > 0] if missing.any() else "No missing values found.")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        st.header("Numeric Distribution")
        st.pyplot(plot_histograms(df, numeric_cols))

        st.header("Correlation Analysis")
        st.pyplot(plot_correlation(df, numeric_cols))
    else:
        st.info("No numeric columns available for histogram or correlation plots.")

    st.header("Sample Value Counts")
    for col in df.select_dtypes(include=[object, "category"]).columns[:3]:
        st.subheader(col)
        st.write(df[col].value_counts().head(10))


if __name__ == "__main__":
    main()
