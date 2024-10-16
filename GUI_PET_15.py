import tkinter as tk
from tkinter import messagebox
import math

# Constants
A0 = 333  # Administered activity (MBq)
T = 1  # Occupancy factor
T1_2 = 109.8 / 60  # Radionuclide half-life in hours (109.8 minutes)
dr = 0.092  # Dose rate immediately after administration (µSv m²/MBq h)
P_controlled = 100  # Weekly dose limit for controlled areas (µSv)
P_uncontrolled = 20  # Weekly dose limit for uncontrolled areas (µSv)

# Original Functions without modification
def RtU(T1_2, tU):
    return 1.443 * (T1_2 / tU) * (1 - math.exp(-0.693 * tU / T1_2))

def RtI(T1_2, tI):
    return 1.443 * (T1_2 / tI) * (1 - math.exp(-0.693 * tI / T1_2))

def DtU(dr, A0, tU, RtU, d):
    return dr * A0 * tU * (RtU / d**2)

def B_uptake_room(P, d, T, Nw, A0, tU, RtU):
    return 10.9 * P * (d ** 2) / (T * Nw * A0 * tU * RtU)

def Fu(tU):
    return math.exp(-0.693 * (tU*60) / 110)

def B_scan_room(P, d, T, Nw, A0, tI, Fu, RtI):
    return 12.8 * P * (d ** 2) / (T * Nw * A0 * 0.85 * tI * Fu * RtI)

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

def find_thickness(B, material):
    factors = transmission_factors[material]
    for thickness, factor in factors.items():
        if factor <= B:
            return thickness
    return None

# Function to calculate transmission factors and thickness
def calculate_transmission_factors(Nw, d, tU, tI):
    rtU = RtU(T1_2, tU)
    rti = RtI(T1_2, tI)
    fu = Fu(tU)

    B_U_uncontrolled = B_uptake_room(P_uncontrolled, d, T, Nw, A0, tU, rtU)
    B_U_controlled = B_uptake_room(P_controlled, d, T, Nw, A0, tU, rtU)
    B_S_uncontrolled = B_scan_room(P_uncontrolled, d, T, Nw, A0, tI, fu, rti)
    B_S_controlled = B_scan_room(P_controlled, d, T, Nw, A0, tI, fu, rti)

    return {
        "Uptake Room Uncontrolled": B_U_uncontrolled,
        "Uptake Room Controlled": B_U_controlled,
        "Scan Room Uncontrolled": B_S_uncontrolled,
        "Scan Room Controlled": B_S_controlled
    }

# GUI Setup
def create_gui():
    # Create the main window
    window = tk.Tk()
    window.title("Transmission Factor and Thickness Calculator")

    # Labels and Entry boxes
    tk.Label(window, text="Number of Patients per Week:").grid(row=0, column=0)
    Nw_entry = tk.Entry(window)
    Nw_entry.grid(row=0, column=1)

    tk.Label(window, text="Distance from Source to Barrier (m):").grid(row=1, column=0)
    d_entry = tk.Entry(window)
    d_entry.grid(row=1, column=1)

    tk.Label(window, text="Uptake Time (hours):").grid(row=2, column=0)
    tU_entry = tk.Entry(window)
    tU_entry.grid(row=2, column=1)

    tk.Label(window, text="Scan Time (hours):").grid(row=3, column=0)
    tI_entry = tk.Entry(window)
    tI_entry.grid(row=3, column=1)

    # Function to handle the calculation when the button is clicked
    def on_calculate():
        try:
            Nw = int(Nw_entry.get())
            d = float(d_entry.get())
            tU = float(tU_entry.get())
            tI = float(tI_entry.get())

            # Perform calculations
            B_results = calculate_transmission_factors(Nw, d, tU, tI)

            # Find thickness for each material
            results = {}
            for room, B in B_results.items():
                thickness_lead = find_thickness(B, "Lead")
                thickness_concrete = find_thickness(B, "Concrete")
                results[room] = {
                    "Lead Thickness": thickness_lead,
                    "Concrete Thickness": thickness_concrete
                }

            # Display the results
            result_text = ""
            for room, thicknesses in results.items():
                result_text += f"{room}:\n"
                result_text += f"  Lead Thickness: {thicknesses['Lead Thickness']} mm\n"
                result_text += f"  Concrete Thickness: {thicknesses['Concrete Thickness']} cm\n\n"

            messagebox.showinfo("Results", result_text)
        
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    # Calculate button
    calculate_button = tk.Button(window, text="Calculate", command=on_calculate)
    calculate_button.grid(row=4, columnspan=2)

    # Run the GUI event loop
    window.mainloop()

# Run the GUI
create_gui()
