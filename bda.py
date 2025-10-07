import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# Visualization Functions
# ----------------------------

def show_basic_stats(df):
    try:
        required_cols = ["Age", "Avg_Daily_Screen_Time"]
        for col in required_cols:
            if col not in df.columns:
                messagebox.showerror("Error", f"Missing column: {col}")
                return

        stats = (
            f"Total Records: {len(df)}\n"
            f"Average Age: {df['Age'].mean():.2f}\n"
            f"Average Daily Screen Time: {df['Avg_Daily_Screen_Time'].mean():.2f} hrs\n"
        )
        messagebox.showinfo("Basic Statistics", stats)
    except Exception as e:
        messagebox.showerror("Error", f"Cannot calculate stats:\n{e}")


def plot_device_distribution(df):
    try:
        if "Primary_Device" not in df.columns:
            messagebox.showerror("Error", "Missing column: Primary_Device")
            return

        device_counts = df["Primary_Device"].value_counts()
        device_counts.plot(
            kind="pie",
            autopct="%1.1f%%",
            startangle=140,
            ylabel="",
            labels=device_counts.index,
            title="Primary Device Usage"
        )
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot plot device distribution:\n{e}")


def plot_gender_distribution(df):
    try:
        if "Gender" not in df.columns:
            messagebox.showerror("Error", "Missing column: Gender")
            return

        df["Gender"].value_counts().plot(
            kind="bar",
            color=["#66b3ff", "#ff9999"],
            title="Gender Distribution"
        )
        plt.xlabel("Gender")
        plt.ylabel("Count")
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot plot gender distribution:\n{e}")


def plot_screen_time_by_age(df):
    try:
        required_cols = ["Age", "Avg_Daily_Screen_Time"]
        for col in required_cols:
            if col not in df.columns:
                messagebox.showerror("Error", f"Missing column: {col}")
                return

        df.groupby("Age")["Avg_Daily_Screen_Time"].mean().plot(
            kind="line",
            marker="o",
            color="skyblue",
            title="Average Screen Time by Age"
        )
        plt.xlabel("Age")
        plt.ylabel("Avg Daily Screen Time (hrs)")
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot plot screen time by age:\n{e}")


def correlation_analysis(df):
    try:
        df_numeric = df.select_dtypes(include="number")
        if df_numeric.empty:
            messagebox.showerror("Error", "No numeric columns for correlation analysis.")
            return

        plt.figure(figsize=(8,6))
        sns.heatmap(df_numeric.corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot generate correlation heatmap:\n{e}")

# ----------------------------
# Tkinter GUI
# ----------------------------

class ScreentimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Indian Kids Screentime 2025")
        self.root.geometry("600x400")

        self.df = None

        buttons = [
            ("📂 Load Screentime CSV", self.load_csv),
            ("📊 Show Basic Stats", self.show_stats),
            ("📱 Device Usage Chart", self.device_chart),
            ("🚻 Gender Distribution Chart", self.gender_chart),
            ("📈 Screen Time by Age", self.age_chart),
            ("🔍 Correlation Analysis", self.show_corr)
        ]

        for text, cmd in buttons:
            tk.Button(root, text=text, command=cmd, width=35).pack(pady=8)

    # ----------------------------
    # Button Actions
    # ----------------------------
    def load_csv(self):
        try:
            url = "https://raw.githubusercontent.com/kjahanvi/indian-kids-screentime-2025/main/indian_kids_screentime_2025.csv"
            self.df = pd.read_csv(url)
            messagebox.showinfo("Success", f"Dataset loaded from GitHub!\n{len(self.df)} records.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load dataset:\n{e}")

    def show_stats(self):
        if self.df is not None:
            show_basic_stats(self.df)
        else:
            messagebox.showwarning("Warning", "Load a CSV file first!")

    def device_chart(self):
        if self.df is not None:
            plot_device_distribution(self.df)
        else:
            messagebox.showwarning("Warning", "Load a CSV file first!")

    def gender_chart(self):
        if self.df is not None:
            plot_gender_distribution(self.df)
        else:
            messagebox.showwarning("Warning", "Load a CSV file first!")

    def age_chart(self):
        if self.df is not None:
            plot_screen_time_by_age(self.df)
        else:
            messagebox.showwarning("Warning", "Load a CSV file first!")

    def show_corr(self):
        if self.df is not None:
            correlation_analysis(self.df)
        else:
            messagebox.showwarning("Warning", "Load a CSV file first!")

# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ScreentimeApp(root)
    root.mainloop()
