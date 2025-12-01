# Thermal Decay Simulator

A Python Tkinter application that visualizes *Newton’s Law of Cooling* with interactive parameters, real-time graph plotting, CSV export support, and predefined real-world scenarios.

---

## Overview

The *Thermal Decay Simulator* demonstrates how an object cools or warms based on Newton’s Law of Cooling.

The temperature at any time t is given by:

    T(t) = T_env + (T0 – T_env) * e^(-k * t)

Where:
- T(t) = Temperature at time t  
- T0 = Initial temperature  
- T_env = Ambient temperature  
- k = Cooling constant (positive value)  
- e = Euler’s number (2.718…)

The app allows users to:
- Enter their own values  
- Load predefined scenarios  
- Plot the temperature curve  
- Export data to CSV  

---

##  Features

###  Interactive Inputs
- Initial Temperature (T0)
- Ambient Temperature (T_env)
- Cooling Constant (k)
- Maximum Time (t_max)
- Resolution / Number of Points

###  Real-Time Graph
- Clean temperature vs. time plot
- Dark-themed UI
- Shaded area under curve

###  Built-in Scenarios
-  Hot coffee cooling  
- Iced tea warming  
-  Forensic body cooling  
-  Metal quenching  

