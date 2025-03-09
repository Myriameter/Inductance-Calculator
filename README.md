How It Works.
The calculator applies the resonant frequency formula to determine inductance:

Connect a known capacitor in parallel with your unknown inductor.
Apply a square wave to excite the LC circuit.
Measure the resonant frequency oscillations on your oscilloscope.
Enter the capacitor value, number of cycles, and total time of measurement.
The calculator computes the inductance based on the formula: L = 1/(4π²f²C).

Requirements:

Python 3.x
Tkinter (included in standard Python installation)
https://www.python.org/downloads/

# Run the calculator
python inductor_calc.py
Or use inductor_calc.exe 

Usage

Enter your known capacitor value and select the appropriate units.
Input any known parasitic inductance of your measurement setup (or leave as zero).
Enter the number of cycles measured on your oscilloscope.
Enter the total time of these cycles and select the appropriate time units.
Click "Calculate Inductance" to get your result.
