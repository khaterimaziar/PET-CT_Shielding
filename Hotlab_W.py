import tkinter as tk
from tkinter import messagebox

# Function to calculate transmission factor (B)
def calculate_transmission_factor(P, d, T, A_source, shielding_factor):
    B = (P * d ** 2) / (T * A_source * shielding_factor * dose_rate_constant)
    return B

# Function to find the required thickness for a material (Lead/Concrete)
def find_thickness(B, material):
    factors = transmission_factors[material]
    for thickness, factor in factors.items():
        if factor <= B:
            return thickness  # Returns the first thickness where the factor is less than or equal to B
    return None

# Function to run calculations when the button is clicked
def calculate():
    try:
        distance = float(entry_distance.get())
        
        # Calculate transmission factors for controlled and uncontrolled areas
        B_controlled = calculate_transmission_factor(P_controlled, distance, T, A_source, vial_shielding_factor)
        B_uncontrolled = calculate_transmission_factor(P_uncontrolled, distance, T, A_source, vial_shielding_factor)
        
        # Calculate required thickness for both Lead and Concrete
        lead_thickness_controlled = find_thickness(B_controlled, "Lead")
        concrete_thickness_controlled = find_thickness(B_controlled, "Concrete")
        
        lead_thickness_uncontrolled = find_thickness(B_uncontrolled, "Lead")
        concrete_thickness_uncontrolled = find_thickness(B_uncontrolled, "Concrete")
        
        # Display results
        result_text = f"Controlled Area:\n"
        result_text += f"  Lead Thickness: {lead_thickness_controlled} mm\n"
        result_text += f"  Concrete Thickness: {concrete_thickness_controlled} cm\n\n"
        
        result_text += f"Uncontrolled Area \n"
        result_text += f"  Lead Thickness: {lead_thickness_uncontrolled} mm\n"
        result_text += f"  Concrete Thickness: {concrete_thickness_uncontrolled} cm"
        
        label_result.config(text=result_text)
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for distance.")

# Initialize the GUI application
root = tk.Tk()
root.title("Radiation Shielding Calculator_PET/CT_HOTLAB")

# Create and place widgets
label_distance = tk.Label(root, text="Enter Distance (m):")
label_distance.grid(row=0, column=0, padx=10, pady=10)

entry_distance = tk.Entry(root)
entry_distance.grid(row=0, column=1, padx=10, pady=10)

button_calculate = tk.Button(root, text="Calculate", command=calculate)
button_calculate.grid(row=1, columnspan=2, pady=10)

label_result = tk.Label(root, text="", justify="left")
label_result.grid(row=2, columnspan=2, padx=10, pady=10)

# Constants
A_source = 37000  # Initial radioactive source activity in MBq
P_controlled = 15  # Daily dose limit for controlled areas (µSv)
P_uncontrolled = 3  # Daily dose limit for uncontrolled areas (µSv)
T = 1  # Occupancy factor
dose_rate_constant = 0.092  # µSv m²/MBq h, dose rate constant for FDG
vial_shielding_factor = 0.0024  # 99.76% shielding by the 40mm vial

# Transmission factors for Lead and Concrete
transmission_factors = {
    "Lead": {
        0: 1.0000, 1: 0.8912, 2: 0.7873, 3: 0.6905, 4: 0.6021,
        5: 0.5227, 6: 0.4522, 7: 0.3903, 8: 0.3362, 9: 0.2892,
        10: 0.2485, 12: 0.1831, 14: 0.1347, 16: 0.0990, 18: 0.0728,
        20: 0.0535, 25: 0.0247, 30: 0.0114, 40: 0.0024, 50: 0.0005
    },
    "Concrete": {
        0: 1.0000, 1: 0.9583, 2: 0.9088, 3: 0.8519, 4: 0.7889,
        5: 0.7218, 6: 0.6528, 7: 0.5842, 8: 0.5180, 9: 0.4558,
        10: 0.3987, 12: 0.3008, 14: 0.2243, 16: 0.1662, 18: 0.1227,
        20: 0.0904, 25: 0.0419, 30: 0.0194, 40: 0.0042, 50: 0.0009
    }
}

# Start the GUI event loop
root.mainloop()
