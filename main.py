import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

# ==========================================
# 🎨 COLOR PALETTE & STYLING
# ==========================================
COLORS = {
    "bg": "#1e1e2e",           # Dark Navy Background
    "panel": "#252535",        # Slightly lighter panel
    "text": "#e0e0e0",         # Soft White
    "accent": "#bb86fc",       # Soft Purple (for graph lines)
    "btn_primary": "#6200ea",  # Deep Purple (Compute)
    "btn_success": "#00c853",  # Green (Save)
    "btn_secondary": "#37474f",# Grey (Example)
    "input_bg": "#303040",     # Input field background
    "input_fg": "#ffffff"      # Input text color
}

FONTS = {
    "header": ("Segoe UI", 14, "bold"),
    "label": ("Segoe UI", 10),
    "input": ("Consolas", 11),
    "btn": ("Segoe UI", 10, "bold")
}

# ==========================================
# 📚 EXAMPLE SCENARIOS
# ==========================================
# This list holds different cooling/warming scenarios
# Clicking the button cycles through these.
EXAMPLES = [
    {
        "name": "☕ Hot Coffee in Room",
        "T0": 90.0,   # Starts hot
        "T_env": 25.0, # Room temp
        "k": 0.07,    # Moderate cooling
        "t_max": 60.0,
        "points": 100
    },
    {
        "name": "🧊 Iced Tea Warming Up",
        "T0": 4.0,     # Starts cold (Fridge)
        "T_env": 30.0, # Hot day
        "k": 0.05,     # Warms up
        "t_max": 120.0,
        "points": 100
    },
    {
        "name": "🕵️ Forensic: Body Cooling",
        "T0": 37.0,    # Body temp
        "T_env": 15.0, # Cold basement
        "k": 0.03,     # Slow cooling (insulated)
        "t_max": 180.0,
        "points": 200
    },
    {
        "name": "🔥 Metal Quenching",
        "T0": 800.0,   # Red hot metal
        "T_env": 20.0, # Water bath
        "k": 0.2,      # Very fast cooling
        "t_max": 30.0,
        "points": 200
    }
]

# Track which example is currently shown
current_example_index = 0

# ==========================================
# 🧮 LOGIC FUNCTIONS
# ==========================================
def validate_float(value, name):
    try:
        return float(value)
    except:
        raise ValueError(f"{name} must be a number. Got: {value}")

def compute_and_plot():
    try:
        # Get values
        T0 = validate_float(entry_T0.get(), "T0")
        T_env = validate_float(entry_Tenv.get(), "T_env")
        k = validate_float(entry_k.get(), "k")
        t_max = validate_float(entry_tmax.get(), "t_max")
        npts = int(validate_float(entry_npts.get(), "Points"))

        if npts < 2: raise ValueError("Points must be > 1")
        if t_max <= 0: raise ValueError("Max time must be positive")

    except Exception as e:
        status_label.config(text=f"❌ Error: {str(e)}", fg="#ff5252")
        return

    # Math
    t = np.linspace(0, t_max, npts)
    T = T_env + (T0 - T_env) * np.exp(-k * t)

    # --- Plotting (Modernized) ---
    fig.clear()
    fig.patch.set_facecolor(COLORS["bg"]) # Match app background
    
    ax = fig.add_subplot(111)
    ax.set_facecolor(COLORS["bg"])
    
    # Plot Line
    ax.plot(t, T, color=COLORS["accent"], linewidth=2.5, alpha=0.9)
    ax.fill_between(t, T, T_env, color=COLORS["accent"], alpha=0.1) # Cool glow effect under line

    # Styling Axis
    ax.set_title("Newton's Law of Cooling", color="white", fontsize=12, pad=10)
    ax.set_xlabel("Time (t)", color="#aaaaaa")
    ax.set_ylabel("Temperature (T)", color="#aaaaaa")
    ax.tick_params(colors="#aaaaaa")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
    
    ax.grid(True, color="#444444", linestyle="--", alpha=0.3)
    
    canvas.draw()

    # Update UI Text
    formula_text.set(f"T(t) = {T_env} + ({T0 - T_env:.2f})e^(-{k}t)")
    status_label.config(text="✔ Calculation complete.", fg="#69f0ae")

    # Store Data
    app_state["t"] = t
    app_state["T"] = T

def save_csv():
    if "t" not in app_state:
        status_label.config(text="⚠ Run calculation first!", fg="#ffd740")
        return

    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not path: return

    try:
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["t", "T(t)"])
            for ti, Ti in zip(app_state["t"], app_state["T"]):
                w.writerow([ti, Ti])
        status_label.config(text=f"✔ Saved to {path.split('/')[-1]}", fg="#69f0ae")
    except Exception as e:
        status_label.config(text=f"❌ Save Error: {e}", fg="#ff5252")

def load_next_example():
    """Cycles through the predefined EXAMPLES list"""
    global current_example_index
    
    # Get current scenario
    scenario = EXAMPLES[current_example_index]
    
    # Update UI inputs
    set_entry(entry_T0, str(scenario["T0"]))
    set_entry(entry_Tenv, str(scenario["T_env"]))
    set_entry(entry_k, str(scenario["k"]))
    set_entry(entry_tmax, str(scenario["t_max"]))
    set_entry(entry_npts, str(scenario["points"]))
    
    # Notify user which topic is loaded
    status_label.config(text=f"ℹ Loaded Topic: {scenario['name']}", fg="#80d8ff")
    
    # Automatically plot it for smoothness
    compute_and_plot()
    
    # Move to next index (loop back to 0 if at end)
    current_example_index = (current_example_index + 1) % len(EXAMPLES)

def set_entry(entry, val):
    entry.delete(0, tk.END)
    entry.insert(0, val)

# ==========================================
# 🖥️ UI CONSTRUCTION
# ==========================================
root = tk.Tk()
root.title("Thermal Decay Simulator")
root.geometry("1100x700")
root.configure(bg=COLORS["bg"])

app_state = {}
formula_text = tk.StringVar(value="Formula will appear here")

# --- Layout Frames ---
# Left Panel (Controls)
left_frame = tk.Frame(root, bg=COLORS["panel"], width=300, padx=20, pady=20)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False) # Force width to stay 300px

# Right Panel (Graph)
right_frame = tk.Frame(root, bg=COLORS["bg"])
right_frame.pack(side="right", fill="both", expand=True)

# --- Left Panel Content ---

# Title
tk.Label(left_frame, text="PARAMETERS", bg=COLORS["panel"], fg=COLORS["accent"], 
         font=FONTS["header"]).pack(anchor="w", pady=(0, 20))

# Helper to make inputs
def create_input(parent, label):
    lbl = tk.Label(parent, text=label, bg=COLORS["panel"], fg=COLORS["text"], font=FONTS["label"])
    lbl.pack(anchor="w", pady=(5, 0))
    ent = tk.Entry(parent, bg=COLORS["input_bg"], fg=COLORS["input_fg"], 
                   insertbackground="white", relief="flat", font=FONTS["input"])
    ent.pack(fill="x", pady=(2, 10), ipady=4) # ipady adds internal height
    return ent

entry_T0 = create_input(left_frame, "Initial Temp (T0)")
entry_Tenv = create_input(left_frame, "Ambient Temp (Tenv)")
entry_k = create_input(left_frame, "Cooling Constant (k)")
entry_tmax = create_input(left_frame, "Max Time")
entry_npts = create_input(left_frame, "Resolution (Points)")

# Formula Display
tk.Label(left_frame, text="Model:", bg=COLORS["panel"], fg="#888", font=("Segoe UI", 9)).pack(anchor="w", pady=(15,0))
tk.Label(left_frame, textvariable=formula_text, bg=COLORS["panel"], fg=COLORS["text"], 
         font=("Consolas", 9), wraplength=260, justify="left").pack(anchor="w", pady=(0, 20))

# Buttons
def create_btn(parent, text, cmd, bg_color):
    btn = tk.Button(parent, text=text, command=cmd, bg=bg_color, fg="white", 
                    font=FONTS["btn"], relief="flat", activebackground=COLORS["text"], activeforeground="black", cursor="hand2")
    btn.pack(fill="x", pady=6, ipady=5)
    return btn

create_btn(left_frame, "🚀 COMPUTE GRAPH", compute_and_plot, COLORS["btn_primary"])
create_btn(left_frame, "💾 SAVE TO CSV", save_csv, COLORS["btn_success"])
# Updated Button Text
create_btn(left_frame, "↺ NEXT SCENARIO", load_next_example, COLORS["btn_secondary"])

# --- Right Panel Content ---
# Graph Area
fig = plt.Figure(figsize=(5, 5), dpi=100, facecolor=COLORS["bg"])
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

# Status Bar (Bottom)
status_frame = tk.Frame(right_frame, bg=COLORS["panel"], height=30)
status_frame.pack(fill="x", side="bottom")
status_label = tk.Label(status_frame, text="Ready", bg=COLORS["panel"], fg="#888", font=("Segoe UI", 9))
status_label.pack(side="left", padx=10, pady=5)

# Initialize with the first example
load_next_example()

root.mainloop()
