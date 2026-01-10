import tkinter as tk
from tkinter import ttk

class InductorCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Myriameter.uk Inductor Calculator")
        # Dynamic sizing based on content
        self.root.minsize(500, 600)
        self.root.resizable(True, True)
        
        # Configure fonts
        self.header_font = ('Helvetica', 16, 'bold')
        self.label_font = ('Helvetica', 10)
        self.result_font = ('Helvetica', 12, 'bold')
        
        # Unit variables
        self.capacitor_unit = tk.StringVar(value="nF")
        self.parasitic_unit = tk.StringVar(value="pH")  # Default to pH
        self.time_unit = tk.StringVar(value="µS")
        self.result_unit = tk.StringVar(value="µH")
        
        # Define conversion factors
        self.cap_factors = {"pF": 1e-12, "nF": 1e-9, "µF": 1e-6}
        self.time_factors = {"nS": 1e-9, "µS": 1e-6, "mS": 1e-3}
        
        # Result storage
        self.calculated_inductance_picohenries = 0
        self.calculated_q_factor = 0
        self.calculated_esr_ohms = 0
        self.resonant_frequency_hz = 0  # For ESR calculation
        
        # New variables for Q measurement
        self.enable_q_measurement = tk.BooleanVar(value=False)
        
        # Create the UI
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20, padx=20, fill='x')
        
        ttk.Label(header_frame, text="Myriameter.uk Inductor Calculator", font=self.header_font).pack()
        # Add slightly more padding between the title and the subtitle
        ttk.Label(header_frame, text="", font=('Helvetica', 3)).pack()  # Small empty label for spacing
        ttk.Label(header_frame, text="Calculate inductance by measuring resonant frequency", 
                 font=self.label_font).pack(pady=0)
        ttk.Label(header_frame, text="(LC) with an oscilloscope and square wave generator", 
                 font=self.label_font).pack(pady=5)
        
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Input Parameters")
        input_frame.pack(padx=20, pady=10, fill='x')
        
        # Capacitor Input
        ttk.Label(input_frame, text="Known capacitor value:", font=self.label_font).pack(anchor='w', padx=15, pady=(15,0))
        cap_frame = ttk.Frame(input_frame)
        cap_frame.pack(fill='x', padx=15, pady=(0,10))
        
        self.capacitor_entry = ttk.Entry(cap_frame, width=10)
        self.capacitor_entry.pack(side=tk.LEFT)
        self.capacitor_entry.insert(0, "10")  # Default to 10nF
        
        cap_unit_frame = ttk.Frame(cap_frame)
        cap_unit_frame.pack(side=tk.LEFT, padx=(5,0))
        
        for unit in ["pF", "nF", "µF"]:
            ttk.Radiobutton(cap_unit_frame, text=unit, value=unit, variable=self.capacitor_unit).pack(side=tk.LEFT, padx=2)
        
        # Parasitic Input
        ttk.Label(input_frame, text="Parasitic inductance of module: (Zero if unknown)", 
                 font=self.label_font).pack(anchor='w', padx=15)
        para_frame = ttk.Frame(input_frame)
        para_frame.pack(fill='x', padx=15, pady=(0,10))
        
        self.parasitic_entry = ttk.Entry(para_frame, width=10)
        self.parasitic_entry.pack(side=tk.LEFT)
        self.parasitic_entry.insert(0, "0")
        
        para_unit_frame = ttk.Frame(para_frame)
        para_unit_frame.pack(side=tk.LEFT, padx=(5,0))
        
        for unit in ["pH", "nH", "µH"]:
            ttk.Radiobutton(para_unit_frame, text=unit, value=unit, variable=self.parasitic_unit).pack(side=tk.LEFT, padx=2)
        
        # Cycles Input
        ttk.Label(input_frame, text="Number of cycles measured on oscilloscope:", 
                 font=self.label_font).pack(anchor='w', padx=15)
        cycles_frame = ttk.Frame(input_frame)
        cycles_frame.pack(fill='x', padx=15, pady=(0,10))
        
        self.cycles_entry = ttk.Entry(cycles_frame, width=10)
        self.cycles_entry.pack(side=tk.LEFT)
        self.cycles_entry.insert(0, "10")  # Default to 10 cycles
        
        # Time Input
        ttk.Label(input_frame, text="Total waveform time:", font=self.label_font).pack(anchor='w', padx=15)
        time_frame = ttk.Frame(input_frame)
        time_frame.pack(fill='x', padx=15, pady=(0,10))
        
        self.time_entry = ttk.Entry(time_frame, width=10)
        self.time_entry.pack(side=tk.LEFT)
        self.time_entry.insert(0, "100")  # Default to 100 µS
        
        time_unit_frame = ttk.Frame(time_frame)
        time_unit_frame.pack(side=tk.LEFT, padx=(5,0))
        
        for unit in ["nS", "µS", "mS"]:
            ttk.Radiobutton(time_unit_frame, text=unit, value=unit, variable=self.time_unit).pack(side=tk.LEFT, padx=2)
        
        # Q Measurement Toggle
        q_toggle_frame = ttk.Frame(input_frame)
        q_toggle_frame.pack(fill='x', padx=15, pady=(5,0))
        
        q_checkbox = ttk.Checkbutton(
            q_toggle_frame, 
            text="Enable Q factor and ESR measurements", 
            variable=self.enable_q_measurement,
            command=self.toggle_q_measurement
        )
        q_checkbox.pack(anchor='w')
        
        # Q Measurement Method Frame (hidden by default)
        self.q_method_frame = ttk.LabelFrame(input_frame, text="Q Measurement")
        
        ttk.Label(self.q_method_frame, 
                 text="Measures Q using amplitude decay between oscillations", 
                 font=self.label_font).pack(anchor='w', padx=10, pady=(5,5))
        
        # Ringdown Method Inputs - directly in the q_method_frame
        ttk.Label(self.q_method_frame, text="Initial amplitude (V₁):", 
                 font=self.label_font).pack(anchor='w', padx=15)
        v1_frame = ttk.Frame(self.q_method_frame)
        v1_frame.pack(fill='x', padx=15, pady=(0,5))
        
        self.v1_entry = ttk.Entry(v1_frame, width=10)
        self.v1_entry.pack(side=tk.LEFT)
        ttk.Label(v1_frame, text="V", font=self.label_font).pack(side=tk.LEFT, padx=(5,0))
        
        # Final amplitude label will be set dynamically when cycles change
        self.final_amplitude_label = ttk.Label(self.q_method_frame, 
                                             text="", 
                                             font=self.label_font)
        self.final_amplitude_label.pack(anchor='w', padx=15)
        
        v2_frame = ttk.Frame(self.q_method_frame)
        v2_frame.pack(fill='x', padx=15, pady=(0,10))
        
        self.v2_entry = ttk.Entry(v2_frame, width=10)
        self.v2_entry.pack(side=tk.LEFT)
        ttk.Label(v2_frame, text="V", font=self.label_font).pack(side=tk.LEFT, padx=(5,0))
        
        # Calculate Button (moved from input_frame to below)
        calc_button_frame = ttk.Frame(self.root)
        calc_button_frame.pack(pady=(0,15), fill='x')
        
        self.calc_button = ttk.Button(calc_button_frame, text="Calculate", command=self.calculate)
        self.calc_button.pack(pady=(0,0))
        
        # Result Frame (removed "Results" label)
        self.result_frame = ttk.Frame(self.root)
        self.result_frame.pack(padx=20, pady=10, fill='x')
        
        # Result Display - centered alignment
        result_display_frame = ttk.Frame(self.result_frame)
        result_display_frame.pack(pady=15, padx=15, fill='x')
        
        # Create a container frame for centering
        result_center_frame = ttk.Frame(result_display_frame)
        result_center_frame.pack(anchor='center')
        
        self.result_label = ttk.Label(result_center_frame, text="Calculated inductance will appear here", 
                                     font=self.result_font, justify=tk.CENTER)
        self.result_label.pack()
        
        # Q factor result (initially hidden)
        self.q_result_label = ttk.Label(result_center_frame, text="", 
                                      font=self.result_font, justify=tk.CENTER)
        
        # ESR result (initially hidden)
        self.esr_result_label = ttk.Label(result_center_frame, text="", 
                                       font=self.result_font, justify=tk.CENTER)
        
        # Result unit selection
        result_unit_frame = ttk.Frame(self.result_frame)
        result_unit_frame.pack(pady=(0,15), padx=15)
        
        # Center the "Display result in:" text and radio buttons
        unit_container = ttk.Frame(result_unit_frame)
        unit_container.pack(anchor='center')
        
        ttk.Label(unit_container, text="Display result in: ", font=self.label_font).pack(side=tk.LEFT)
        
        # Store references to radio buttons
        self.result_radio_buttons = []
        for unit in ["pH", "nH", "µH", "mH", "H"]:
            rb = ttk.Radiobutton(
                unit_container, 
                text=unit, 
                value=unit, 
                variable=self.result_unit,
                command=self.update_result_display
            )
            rb.pack(side=tk.LEFT, padx=5)
            self.result_radio_buttons.append((unit, rb))
        
        # Status Frame
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(padx=20, pady=5, fill='x')
        
        self.status_label = ttk.Label(self.status_frame, text="Ready to calculate", 
                                     font=('Helvetica', 9, 'italic'))
        self.status_label.pack(side=tk.LEFT)
        
        # Version label at bottom right
        version_label = ttk.Label(self.status_frame, text="V1.31  2025",
                                 font=('Helvetica', 9))
        version_label.pack(side=tk.RIGHT)
        
        # Set focus to first entry
        self.capacitor_entry.focus()
        
        # Bind Enter key to calculate
        self.root.bind('<Return>', lambda event: self.calculate())
        
        # Bind tab order
        self.capacitor_entry.bind('<Return>', lambda e: self.parasitic_entry.focus())
        self.parasitic_entry.bind('<Return>', lambda e: self.cycles_entry.focus())
        self.cycles_entry.bind('<Return>', lambda e: self.time_entry.focus())
        self.time_entry.bind('<Return>', lambda e: self.calculate())
        
        # Bind cycles entry to update the final amplitude label
        self.cycles_entry.bind('<KeyRelease>', lambda e: self.update_final_amplitude_label())
    
    def toggle_q_measurement(self):
        """Show or hide Q measurement controls based on checkbox state"""
        if self.enable_q_measurement.get():
            # Show Q measurement frame
            self.q_method_frame.pack(padx=15, pady=(0, 5), fill='x')
            # Show Q result label and ESR label
            self.q_result_label.pack()
            self.esr_result_label.pack()
            # Update final amplitude label based on current cycles value
            self.update_final_amplitude_label()
            # Update window size to ensure all components are visible
            self.root.update_idletasks()  # Process pending geometry changes
            self.root.geometry("")  # Reset geometry to let window resize to content
        else:
            # Hide Q-related frame
            self.q_method_frame.pack_forget()
            # Hide Q result and ESR labels
            self.q_result_label.pack_forget()
            self.esr_result_label.pack_forget()
            # Update window size
            self.root.update_idletasks()
            self.root.geometry("")
    
    def update_final_amplitude_label(self):
        """Update the final amplitude label text based on cycles"""
        try:
            cycles = int(float(self.cycles_entry.get()))
            cycle_text = "cycle" if cycles == 1 else "cycles"
            self.final_amplitude_label.config(
                text=f"Final amplitude (V₂) after {cycles} measured {cycle_text}:"
            )
        except (ValueError, AttributeError):
            # In case cycles entry is empty or invalid
            self.final_amplitude_label.config(
                text="Final amplitude (V₂) after measured cycles:"
            )
    

        
    def validate_input(self, value, allow_negative=False):
        try:
            float_value = float(value)
            if not allow_negative and float_value <= 0:
                return False, "Values must be greater than zero"
            return True, float_value
        except ValueError:
            return False, "Please enter valid numbers"
    
    def calculate(self):
        # Validate inputs
        entries = [
            (self.capacitor_entry, "Capacitor", False),
            (self.cycles_entry, "Cycles", False),
            (self.time_entry, "Time", False),
            (self.parasitic_entry, "Parasitic inductance", True)  # Allow negative values
        ]
        
        for entry, name, allow_negative in entries:
            valid, result = self.validate_input(entry.get(), allow_negative)
            if not valid:
                self.status_label.config(text=f"Error: {name} - {result}", foreground='red')
                return
                
        # Get values
        capacitor_value = float(self.capacitor_entry.get())
        cycles = float(self.cycles_entry.get())
        time_value = float(self.time_entry.get())
        parasitic = float(self.parasitic_entry.get())
        
        # Apply conversions for capacitor and time
        capacitor_in_farads = capacitor_value * self.cap_factors[self.capacitor_unit.get()]
        time_in_seconds = time_value * self.time_factors[self.time_unit.get()]
        
        # Calculate frequency (Hz)
        frequency = (cycles / time_in_seconds)
        self.resonant_frequency_hz = frequency  # Store for ESR calculation
        
        # Calculate inductance using the resonant frequency formula
        # L = 1/(4π²f²C)
        pi = 3.14159265359
        
        # The standard formula gives result in henries when using SI units
        L_henries = 1 / (4 * pow(pi, 2) * pow(frequency, 2) * capacitor_in_farads)
        
        # Convert from henries to picohenries for easier handling of small values
        L_picohenries = L_henries * 1e12
        
        # Convert parasitic inductance to picohenries and subtract
        parasitic_unit = self.parasitic_unit.get()
        parasitic_in_picohenries = 0
        
        if parasitic_unit == "pH":
            parasitic_in_picohenries = parasitic
        elif parasitic_unit == "nH":
            parasitic_in_picohenries = parasitic * 1000  # 1 nH = 1000 pH
        elif parasitic_unit == "µH":
            parasitic_in_picohenries = parasitic * 1000000  # 1 µH = 1,000,000 pH
        
        L_picohenries -= parasitic_in_picohenries
        
        # Store result in picohenries
        self.calculated_inductance_picohenries = L_picohenries
        
        # Calculate Q factor if enabled
        if self.enable_q_measurement.get():
            q_valid = self.calculate_q_factor()
            if not q_valid:
                return  # Error message already set by calculate_q_factor
            
            # Calculate ESR
            L_henries = L_picohenries * 1e-12  # Convert back to henries for calculation
            self.calculated_esr_ohms = (2 * pi * frequency * L_henries) / self.calculated_q_factor
        
        # Update radio button states
        self.update_radio_button_states()
        
        # Update display
        self.update_result_display()
        
        self.status_label.config(text="Calculation completed successfully", foreground='green')
        
        # Reset focus
        self.capacitor_entry.focus()
        self.capacitor_entry.select_range(0, tk.END)
    
    def calculate_q_factor(self):
        """Calculate the Q factor using the ringdown method"""
        # Validate inputs
        ringdown_entries = [
            (self.v1_entry, "Initial amplitude (V₁)", False),
            (self.v2_entry, "Final amplitude (V₂)", False)
        ]
        
        for entry, name, allow_negative in ringdown_entries:
            valid, result = self.validate_input(entry.get(), allow_negative)
            if not valid:
                self.status_label.config(text=f"Error: {name} - {result}", foreground='red')
                return False
        
        # Get values
        v1 = float(self.v1_entry.get())
        v2 = float(self.v2_entry.get())
        n = float(self.cycles_entry.get())  # Use the same cycles value as for inductance calculation
        
        # Validate that v1 > v2
        if v1 <= v2:
            self.status_label.config(text="Error: Initial amplitude must be greater than final amplitude", foreground='red')
            return False
        
        # Calculate Q factor using ringdown method: Q = π·n / ln(V₁/V₂)
        import math
        delta = math.log(v1 / v2)
        self.calculated_q_factor = math.pi * n / delta
        
        return True
    
    def update_radio_button_states(self):
        # Units in order from smallest to largest
        units = ["pH", "nH", "µH", "mH", "H"]
        
        # Convert picohenries to each unit to find suitable display units
        suitable_units = []
        
        # pH is the base unit - no conversion needed
        ph_value = self.calculated_inductance_picohenries
        if abs(round(ph_value)) >= 1:  # Would display as at least 1
            suitable_units.append(("pH", ph_value))
        
        # nH = pH / 1000
        nh_value = ph_value / 1000
        if abs(round(nh_value)) >= 1:  # Would display as at least 1
            suitable_units.append(("nH", nh_value))
        
        # µH = nH / 1000 = pH / 1000000
        uh_value = ph_value / 1000000
        if abs(round(uh_value, 2)) >= 0.01:  # Would display as at least 0.01
            suitable_units.append(("µH", uh_value))
        
        # mH = µH / 1000 = pH / 1000000000
        mh_value = ph_value / 1000000000
        if abs(round(mh_value, 2)) >= 0.01:  # Would display as at least 0.01
            suitable_units.append(("mH", mh_value))
        
        # H = mH / 1000 = pH / 1000000000000
        h_value = ph_value / 1000000000000
        if abs(round(h_value, 2)) >= 0.01:  # Would display as at least 0.01
            suitable_units.append(("H", h_value))
        
        # If no suitable units found, enable only pH as fallback
        if not suitable_units:
            for unit, rb in self.result_radio_buttons:
                if unit == "pH":
                    rb.configure(state="normal")
                    self.result_unit.set("pH")
                else:
                    rb.configure(state="disabled")
            return
        
        # Find the best unit (where 1 <= |value| < 1000)
        best_unit = None
        for unit, value in suitable_units:
            if 1 <= abs(value) < 1000:
                best_unit = unit
                break
        
        # If no best unit found, find the most appropriate unit for extreme values
        if not best_unit:
            # For extremely large values (>1000 in the largest unit)
            if len(suitable_units) > 0 and abs(suitable_units[-1][1]) >= 1000:
                # Use the largest suitable unit (which will be at the end of the list)
                best_unit = suitable_units[-1][0]
            # For normal values just outside range, use the smallest suitable unit
            else:
                best_unit = suitable_units[0][0]
        
        # Enable only suitable units and set the best unit
        enabled_units = [unit for unit, _ in suitable_units]
        
        # Enable/disable appropriate units
        for unit, rb in self.result_radio_buttons:
            if unit in enabled_units:
                rb.configure(state="normal")
                # Auto-select the best unit
                if unit == best_unit:
                    self.result_unit.set(unit)
            else:
                rb.configure(state="disabled")
    
    def update_result_display(self):
        selected_unit = self.result_unit.get()
        
        # Convert from picohenries (pH) to the selected unit
        if selected_unit == "pH":
            converted_value = self.calculated_inductance_picohenries
        elif selected_unit == "nH":
            converted_value = self.calculated_inductance_picohenries / 1000
        elif selected_unit == "µH":
            converted_value = self.calculated_inductance_picohenries / 1000000
        elif selected_unit == "mH":
            converted_value = self.calculated_inductance_picohenries / 1000000000
        elif selected_unit == "H":
            converted_value = self.calculated_inductance_picohenries / 1000000000000
            
        # Format display based on unit type
        if selected_unit in ["pH", "nH"]:
            # Display as integer (0 decimal places)
            # Use abs() to handle potential negative values correctly
            display_value = int(round(abs(converted_value)))
            # Add negative sign back if value was negative
            if converted_value < 0:
                display_value = -display_value
                
            self.result_label.config(
                text=f"Calculated Inductance: {display_value} {selected_unit}",
                font=self.result_font
            )
        else:
            # Display with 2 decimal places for other units
            self.result_label.config(
                text=f"Calculated Inductance: {converted_value:.2f} {selected_unit}",
                font=self.result_font
            )
        
        # Update Q factor display if enabled
        if self.enable_q_measurement.get():
            self.q_result_label.config(
                text=f"Quality Factor (Q): {self.calculated_q_factor:.2f}",
                font=self.result_font
            )
            
            # Update ESR display
            # Format ESR based on value range for readability
            if self.calculated_esr_ohms >= 1:
                # Display in ohms with 2 decimal places
                self.esr_result_label.config(
                    text=f"ESR: {self.calculated_esr_ohms:.2f} Ω",
                    font=self.result_font
                )
            elif self.calculated_esr_ohms >= 0.001:
                # Display in milliohms
                esr_mohms = self.calculated_esr_ohms * 1000
                self.esr_result_label.config(
                    text=f"ESR: {esr_mohms:.2f} mΩ",
                    font=self.result_font
                )
            else:
                # Display in microohms
                esr_uohms = self.calculated_esr_ohms * 1000000
                self.esr_result_label.config(
                    text=f"ESR: {esr_uohms:.2f} µΩ",
                    font=self.result_font
                )

if __name__ == "__main__":
    root = tk.Tk()
    app = InductorCalculator(root)
    root.mainloop()