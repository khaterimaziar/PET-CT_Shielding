import tkinter as tk
from tkinter import messagebox
import math

def calculate_shielding(thickness, num_patients, activity, material):
    """
    Calculate the required shielding thickness for PET/CT rooms.

    :param thickness: HVL thickness for the material (in mm or cm)
    :param num_patients: Number of patients present
    :param activity: Administered activity (in MBq)
    :param material: Type of material (Lead or Concrete)
    :return: Required thickness (in mm)
    """
    if material == 'Lead':
        hvl = thickness / 1000  # convert mm to meters
    else:  # Concrete
        hvl = thickness / 100  # convert cm to meters

    # Calculate exposure rate at 1 meter
    exposure_rate = 0.143 * activity  # in μSv/h
    total_exposure_rate = exposure_rate * num_patients  # total exposure rate for all patients

    # Calculate required thickness to reduce exposure to acceptable levels
    required_thickness = -math.log(0.1) / (hvl * 1.0)  # For reducing to 10% of original exposure

    return required_thickness * 1000 if material == 'Lead' else required_thickness * 100

def on_calculate():
    try:
        thickness = float(entry_thickness.get())
        num_patients = int(entry_patients.get())
        activity = float(entry_activity.get())
        material = material_var.get()

        result = calculate_shielding(thickness, num_patients, activity, material)
        result_label.config(text=f"Required Thickness: {result:.2f} mm")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# Create the main window
root = tk.Tk()
root.title("Shielding Calculator")

# Create input fields
tk.Label(root, text="HVL Thickness (mm for lead, cm for concrete):").grid(row=0, column=0, padx=10, pady=10)
entry_thickness = tk.Entry(root)
entry_thickness.grid(row=0, column=1)

tk.Label(root, text="Number of Patients:").grid(row=1, column=0, padx=10, pady=10)
entry_patients = tk.Entry(root)
entry_patients.grid(row=1, column=1)

tk.Label(root, text="Administered Activity (MBq):").grid(row=2, column=0, padx=10, pady=10)
entry_activity = tk.Entry(root)
entry_activity.grid(row=2, column=1)

# Radio buttons for material selection
material_var = tk.StringVar(value='Lead')
tk.Label(root, text="Material:").grid(row=3, column=0, padx=10, pady=10)
tk.Radiobutton(root, text="Lead", variable=material_var, value='Lead').grid(row=3, column=1, sticky='w')
tk.Radiobutton(root, text="Concrete", variable=material_var, value='Concrete').grid(row=3, column=1, sticky='e')

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=on_calculate)
calculate_button.grid(row=4, column=0, columnspan=2, pady=20)

# Label to display the result
result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2)

# Run the application
root.mainloop()
