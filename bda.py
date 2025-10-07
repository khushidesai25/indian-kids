import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Visualization Functions
# ----------------------------

def show_basic_stats(df):
    try:
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
        df["Primary_Device"].value_counts().plot(
            kind="pie",
            autopct="%1.1f%%",
            startangle=140,
            title="Primary Device Usage",
            ylabel=""
        )
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot plot device distribution:\n{e}")


def plot_gender_distribution(df):
    try:
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
        plt.matshow(df_numeric.corr(), cmap="coolwarm")
        plt.colorbar()
        plt.title("Correlation Heatmap", pad=20)
        plt.xticks(range(len(df_numeric.columns)), df_numeric.columns, rotation=45, ha="left")
        plt.yticks(range(len(df_numeric.columns)), df_numeric.columns)
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
        self.root.geometry("500x350")

        self.df = None

        tk.Button(root, text="📂 Load Screentime CSV", command=self.load_csv, width=30).pack(pady=10)
        tk.Button(root, text="📊 Show Basic Stats", command=self.show_stats, width=30).pack(pady=5)
        tk.Button(root, text="📱 Device Usage Chart", command=self.device_chart, width=30).pack(pady=5)
        tk.Button(root, text="🚻 Gender Distribution Chart", command=self.gender_chart, width=30).pack(pady=5)
        tk.Button(root, text="📈 Screen Time by Age", command=self.age_chart, width=30).pack(pady=5)
        tk.Button(root, text="🔍 Correlation Analysis", command=self.show_corr, width=30).pack(pady=5)

    # ----------------------------
    # Button Actions
    # ----------------------------
    def load_csv(self):
        try:
            # Load dataset directly from GitHub
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

