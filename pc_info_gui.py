import customtkinter as ctk
import psutil
import platform

# Set appearance mode and red color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def format_bytes(bytes_value):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def format_frequency(freq):
    """Format CPU frequency"""
    try:
        if freq is None:
            return "N/A"
        
        # Handle scpufreq object (has current, min, max attributes)
        if hasattr(freq, 'current'):
            return f"{freq.current:.2f} MHz"
        
        # Handle dict format
        if isinstance(freq, dict):
            return f"{freq.get('current', freq.get('min', 0)):.2f} MHz"
        
        # Handle numeric value
        if isinstance(freq, (int, float)):
            return f"{freq:.2f} MHz"
        
        # Try to convert to float if it's a string-like object
        try:
            return f"{float(freq):.2f} MHz"
        except:
            return str(freq)
    except Exception:
        return "N/A"

def update_system_info():
    """Update all system information"""
    try:
        # CPU Information
        cpu_physical = psutil.cpu_count(logical=False)
        cpu_total = psutil.cpu_count(logical=True)
        
        try:
            cpu_freq = psutil.cpu_freq()
            cpu_freq_value.configure(text=format_frequency(cpu_freq))
        except Exception:
            cpu_freq_value.configure(text="N/A")
        
        cpu_percent = psutil.cpu_percent(interval=1)
        
        cpu_cores_value.configure(text=f"{cpu_physical}")
        cpu_total_cores_value.configure(text=f"{cpu_total}")
        cpu_percent_value.configure(text=f"{cpu_percent}%")
        
        # Memory Information
        memory = psutil.virtual_memory()
        memory_total_value.configure(text=format_bytes(memory.total))
        memory_available_value.configure(text=format_bytes(memory.available))
        memory_used_value.configure(text=format_bytes(memory.used))
        memory_percent_value.configure(text=f"{memory.percent}%")
        
        # Disk Information
        try:
            # Try root partition first, fallback to C: on Windows
            if platform.system() == "Windows":
                disk = psutil.disk_usage('C:')
            else:
                disk = psutil.disk_usage('/')
        except:
            disk = psutil.disk_usage('/')
        
        disk_total_value.configure(text=format_bytes(disk.total))
        disk_used_value.configure(text=format_bytes(disk.used))
        disk_free_value.configure(text=format_bytes(disk.free))
        disk_percent_value.configure(text=f"{disk.percent}%")
        
        # System Information
        system_value.configure(text=platform.system())
        processor_value.configure(text=platform.processor())
        platform_value.configure(text=platform.platform())
        
    except Exception as e:
        # Silently handle errors - individual sections have their own error handling
        pass

# Create the main window
root = ctk.CTk()
root.geometry("800x700")
root.title("System Information - [Developed By cat0x01]")
root.resizable(True, True)

# Create main container
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Title label with red accent
title_label = ctk.CTkLabel(
    main_frame,
    text="System Information",
    font=ctk.CTkFont(size=28, weight="bold"),
    text_color="#F44336"
)
title_label.pack(pady=(10, 5))

subtitle_label = ctk.CTkLabel(
    main_frame,
    text="Developed By cat0x01",
    font=ctk.CTkFont(size=14),
    text_color="#EF5350"
)
subtitle_label.pack(pady=(0, 10))

# Refresh button
refresh_button = ctk.CTkButton(
    main_frame,
    text="🔄 Refresh",
    command=update_system_info,
    font=ctk.CTkFont(size=14, weight="bold"),
    width=150,
    height=35,
    corner_radius=8,
    fg_color="#F44336",
    hover_color="#D32F2F"
)
refresh_button.pack(pady=(0, 15))

# Create scrollable frame for content
scrollable_frame = ctk.CTkScrollableFrame(main_frame, label_text="")
scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)

# CPU Information Section
cpu_frame = ctk.CTkFrame(scrollable_frame)
cpu_frame.pack(fill="x", padx=20, pady=10)

cpu_label = ctk.CTkLabel(
    cpu_frame,
    text="💻 CPU Information",
    font=ctk.CTkFont(size=18, weight="bold"),
    text_color="#F44336"
)
cpu_label.pack(pady=(15, 10))

cpu_info_frame = ctk.CTkFrame(cpu_frame)
cpu_info_frame.pack(fill="x", padx=15, pady=5)

cpu_cores_label = ctk.CTkLabel(cpu_info_frame, text="Physical Cores:", font=ctk.CTkFont(size=12))
cpu_cores_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
cpu_cores_value = ctk.CTkLabel(cpu_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
cpu_cores_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)

cpu_total_cores_label = ctk.CTkLabel(cpu_info_frame, text="Total Cores:", font=ctk.CTkFont(size=12))
cpu_total_cores_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
cpu_total_cores_value = ctk.CTkLabel(cpu_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
cpu_total_cores_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)

cpu_freq_label = ctk.CTkLabel(cpu_info_frame, text="CPU Frequency:", font=ctk.CTkFont(size=12))
cpu_freq_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
cpu_freq_value = ctk.CTkLabel(cpu_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
cpu_freq_value.grid(row=2, column=1, sticky="w", padx=10, pady=5)

cpu_percent_label = ctk.CTkLabel(cpu_info_frame, text="CPU Usage:", font=ctk.CTkFont(size=12))
cpu_percent_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
cpu_percent_value = ctk.CTkLabel(cpu_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
cpu_percent_value.grid(row=3, column=1, sticky="w", padx=10, pady=5)

# Memory Information Section
memory_frame = ctk.CTkFrame(scrollable_frame)
memory_frame.pack(fill="x", padx=20, pady=10)

memory_label = ctk.CTkLabel(
    memory_frame,
    text="🧠 Memory Information",
    font=ctk.CTkFont(size=18, weight="bold"),
    text_color="#F44336"
)
memory_label.pack(pady=(15, 10))

memory_info_frame = ctk.CTkFrame(memory_frame)
memory_info_frame.pack(fill="x", padx=15, pady=5)

memory_total_label = ctk.CTkLabel(memory_info_frame, text="Total Memory:", font=ctk.CTkFont(size=12))
memory_total_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
memory_total_value = ctk.CTkLabel(memory_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
memory_total_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)

memory_available_label = ctk.CTkLabel(memory_info_frame, text="Available:", font=ctk.CTkFont(size=12))
memory_available_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
memory_available_value = ctk.CTkLabel(memory_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
memory_available_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)

memory_used_label = ctk.CTkLabel(memory_info_frame, text="Used:", font=ctk.CTkFont(size=12))
memory_used_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
memory_used_value = ctk.CTkLabel(memory_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
memory_used_value.grid(row=2, column=1, sticky="w", padx=10, pady=5)

memory_percent_label = ctk.CTkLabel(memory_info_frame, text="Usage:", font=ctk.CTkFont(size=12))
memory_percent_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
memory_percent_value = ctk.CTkLabel(memory_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
memory_percent_value.grid(row=3, column=1, sticky="w", padx=10, pady=5)

# Disk Information Section
disk_frame = ctk.CTkFrame(scrollable_frame)
disk_frame.pack(fill="x", padx=20, pady=10)

disk_label = ctk.CTkLabel(
    disk_frame,
    text="💾 Disk Information",
    font=ctk.CTkFont(size=18, weight="bold"),
    text_color="#F44336"
)
disk_label.pack(pady=(15, 10))

disk_info_frame = ctk.CTkFrame(disk_frame)
disk_info_frame.pack(fill="x", padx=15, pady=5)

disk_total_label = ctk.CTkLabel(disk_info_frame, text="Total Space:", font=ctk.CTkFont(size=12))
disk_total_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
disk_total_value = ctk.CTkLabel(disk_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
disk_total_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)

disk_used_label = ctk.CTkLabel(disk_info_frame, text="Used Space:", font=ctk.CTkFont(size=12))
disk_used_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
disk_used_value = ctk.CTkLabel(disk_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
disk_used_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)

disk_free_label = ctk.CTkLabel(disk_info_frame, text="Free Space:", font=ctk.CTkFont(size=12))
disk_free_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
disk_free_value = ctk.CTkLabel(disk_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
disk_free_value.grid(row=2, column=1, sticky="w", padx=10, pady=5)

disk_percent_label = ctk.CTkLabel(disk_info_frame, text="Usage:", font=ctk.CTkFont(size=12))
disk_percent_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
disk_percent_value = ctk.CTkLabel(disk_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
disk_percent_value.grid(row=3, column=1, sticky="w", padx=10, pady=5)

# System Information Section
system_frame = ctk.CTkFrame(scrollable_frame)
system_frame.pack(fill="x", padx=20, pady=10)

system_label = ctk.CTkLabel(
    system_frame,
    text="🖥️ System Information",
    font=ctk.CTkFont(size=18, weight="bold"),
    text_color="#F44336"
)
system_label.pack(pady=(15, 10))

system_info_frame = ctk.CTkFrame(system_frame)
system_info_frame.pack(fill="x", padx=15, pady=5)

system_label_widget = ctk.CTkLabel(system_info_frame, text="Operating System:", font=ctk.CTkFont(size=12))
system_label_widget.grid(row=0, column=0, sticky="w", padx=10, pady=5)
system_value = ctk.CTkLabel(system_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
system_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)

processor_label = ctk.CTkLabel(system_info_frame, text="Processor:", font=ctk.CTkFont(size=12))
processor_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
processor_value = ctk.CTkLabel(system_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
processor_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)

platform_label = ctk.CTkLabel(system_info_frame, text="Platform:", font=ctk.CTkFont(size=12))
platform_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
platform_value = ctk.CTkLabel(system_info_frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFCDD2")
platform_value.grid(row=2, column=1, sticky="w", padx=10, pady=5)

# Initial update
update_system_info()

root.mainloop()
