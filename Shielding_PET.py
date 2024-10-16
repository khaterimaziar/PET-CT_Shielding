import tkinter as tk
from tkinter import messagebox, simpledialog, Menu
import math

# Constants
A0 = 333  # Administered activity (MBq)
T = 1  # Occupancy factor
T1_2 = 109.8 / 60  # Radionuclide half-life in hours (109.8 minutes)
dr = 0.092  # Dose rate immediately after administration (µSv m²/MBq h)
P_controlled = 100  # Weekly dose limit for controlled areas (µSv)
P_uncontrolled = 20  # Weekly dose limit for uncontrolled areas (µSv)

# Transmission factors for Lead and Concrete
transmission_factors = {
    "Lead": {
        0: 1.0000, 1: 0.8912, 2: 0.7873, 3: 0.6905, 4: 0.6021,
        5: 0.5227, 6: 0.4522, 7: 0.3903, 8: 0.3362, 9: 0.2892,
        10: 0.2485, 12: 0.1831, 14: 0.1347, 16: 0.0990, 18: 0.0728,
        20: 0.0535, 25: 0.0247, 30: 0.0114, 40: 0.0024, 50: 0.0005, 60: 0.000115
    },
    "Concrete": {
        0: 1.0000, 1: 0.9583, 2: 0.9088, 3: 0.8519, 4: 0.7889,
        5: 0.7218, 6: 0.6528, 7: 0.5842, 8: 0.5180, 9: 0.4558,
        10: 0.3987, 12: 0.3008, 14: 0.2243, 16: 0.1662, 18: 0.1227,
        20: 0.0904, 25: 0.0419, 30: 0.0194, 40: 0.0042, 50: 0.0009, 60: 0.000264
    }
}

# Function to calculate the dose reduction factor over uptake time
def RtU(T1_2, tU):
    return 1.443 * (T1_2 / tU) * (1 - math.exp(-0.693 * tU / T1_2))

# Function to calculate the dose reduction factor over imaging time
def RtI(T1_2, tI):
    return 1.443 * (T1_2 / tI) * (1 - math.exp(-0.693 * tI / T1_2))

# Function to calculate Fu for the scan room
def Fu(tU):
    return math.exp(-0.693 * (tU * 60) / 110)

# Function to calculate transmission factor for the uptake room
def B_uptake_room(P, d, T, Nw, A0, tU, RtU):
    return 10.9 * P * (d ** 2) / (T * Nw * A0 * tU * RtU)

# Function to calculate transmission factor for the Scan room
def B_scan_room(P, d, T, Nw, A0, tI, Fu, RtI):
    return 12.8 * P * (d ** 2) / (T * Nw * A0 * 0.85 * tI * Fu * RtI)

# Function to find thickness based on transmission factor (B)
def find_thickness(B, material):
    factors = transmission_factors[material]
    for thickness, factor in factors.items():
        if factor <= B:
            return thickness  # Return the first thickness where factor is less than or equal to B
    return None

# Function to calculate transmission factors and thicknesses
def calculate_transmission_factors():
    try:
        Nw = int(nw_entry.get())
        d = float(d_entry.get())
        tU = float(tu_entry.get())
        tI = float(ti_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all inputs.")
        return

    # Calculate the dose reduction factor RtU & RtI
    rtU = RtU(T1_2, tU)
    rti = RtI(T1_2, tI)

    # Calculate Fu
    fu = Fu(tU)

    # Calculate the transmission factor B for uncontrolled and controlled areas
    B_U_uncontrolled = B_uptake_room(P_uncontrolled, d, T, Nw, A0, tU, rtU)
    B_U_controlled = B_uptake_room(P_controlled, d, T, Nw, A0, tU, rtU)
    B_S_uncontrolled = B_scan_room(P_uncontrolled, d, T, Nw, A0, tI, fu, rti)
    B_S_controlled = B_scan_room(P_controlled, d, T, Nw, A0, tI, fu, rti)

    # Calculate thicknesses for each room
    results = {
        "Uptake Room Uncontrolled": {
            "Lead": find_thickness(B_U_uncontrolled, "Lead"),
            "Concrete": find_thickness(B_U_uncontrolled, "Concrete")
        },
        "Uptake Room Controlled": {
            "Lead": find_thickness(B_U_controlled, "Lead"),
            "Concrete": find_thickness(B_U_controlled, "Concrete")
        },
        "Scan Room Uncontrolled": {
            "Lead": find_thickness(B_S_uncontrolled, "Lead"),
            "Concrete": find_thickness(B_S_uncontrolled, "Concrete")
        },
        "Scan Room Controlled": {
            "Lead": find_thickness(B_S_controlled, "Lead"),
            "Concrete": find_thickness(B_S_controlled, "Concrete")
        }
    }

    # Display the results
    result_message = ""
    for room, thicknesses in results.items():
        result_message += f"{room}:\n"
        lead_thickness = thicknesses.get("Lead", "Not found")
        concrete_thickness = thicknesses.get("Concrete", "Not found")
        result_message += f"  Lead Thickness: {lead_thickness} mm\n"
        result_message += f"  Concrete Thickness: {concrete_thickness} cm\n\n"

    result_font = ('Helvetica', 14)  # Larger font for results
    result_message = ""  # Your existing result message construction
    messagebox.showinfo("Results", result_message)

# Function to show and edit parameters
def show_parameters():
    # Create a new window for editing parameters
    def edit_parameters():
        entered_password = simpledialog.askstring("Password", "Enter password:", show='*')
        if entered_password == "admin123":
            # Add fields for editing parameters
            edit_window = tk.Toplevel(root)
            edit_window.title("Edit Parameters")
            edit_window.geometry("300x300")

            tk.Label(edit_window, text="Administered activity (MBq):").pack(pady=5)
            A0_var = tk.StringVar(value=str(A0))
            tk.Entry(edit_window, textvariable=A0_var).pack(pady=5)

            tk.Label(edit_window, text="Occupancy factor (T):").pack(pady=5)
            T_var = tk.StringVar(value=str(T))
            tk.Entry(edit_window, textvariable=T_var).pack(pady=5)

            tk.Label(edit_window, text="Half-life (min):").pack(pady=5)
            T1_2_var = tk.StringVar(value=str(T1_2 * 60))
            tk.Entry(edit_window, textvariable=T1_2_var).pack(pady=5)

            tk.Label(edit_window, text="Dose rate (µSv/m²/h):").pack(pady=5)
            dr_var = tk.StringVar(value=str(dr))
            tk.Entry(edit_window, textvariable=dr_var).pack(pady=5)

            tk.Button(edit_window, text="Save", command=lambda: save_parameters(A0_var, T_var, T1_2_var, dr_var)).pack(pady=10)
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def save_parameters(A0_var, T_var, T1_2_var, dr_var):
        global A0, T, T1_2, dr
        A0 = float(A0_var.get())
        T = float(T_var.get())
        T1_2 = float(T1_2_var.get()) / 60  # Convert minutes back to hours
        dr = float(dr_var.get())
        messagebox.showinfo("Success", "Parameters updated successfully.")

    edit_parameters_button = tk.Button(root, text="Edit Parameters", command=edit_parameters)
    edit_parameters_button.pack(pady=20)

# Set up the GUI
root = tk.Tk()
root.title("Radiation Shielding Calculator")
root.geometry("600x500")  # Increased window size
root.configure(bg="#f0f0f0")

# Font style for better resolution
font_style = ('Helvetica', 14)

# Menu
menu = Menu(root)
root.config(menu=menu)
edit_menu = Menu(menu)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Edit Parameters", command=show_parameters)

# Input fields with increased font size
tk.Label(root, text="Number of patients per week:", bg="#f0f0f0", font=font_style).pack(pady=10)
nw_entry = tk.Entry(root, font=font_style)
nw_entry.pack(pady=5)

tk.Label(root, text="Distance from source to barrier (m):", bg="#f0f0f0", font=font_style).pack(pady=10)
d_entry = tk.Entry(root, font=font_style)
d_entry.pack(pady=5)

tk.Label(root, text="Uptake time (hours):", bg="#f0f0f0", font=font_style).pack(pady=10)
tu_entry = tk.Entry(root, font=font_style)
tu_entry.pack(pady=5)

tk.Label(root, text="Scan time (hours):", bg="#f0f0f0", font=font_style).pack(pady=10)
ti_entry = tk.Entry(root, font=font_style)
ti_entry.pack(pady=5)

# Calculate button with increased font size
calculate_button = tk.Button(root, text="Calculate", command=calculate_transmission_factors, font=font_style)
calculate_button.pack(pady=20)

root.mainloop()
