import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from deadlock_detector import DeadlockDetector
from graph_visualizer import visualize_graph

class DeadlockDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detection Simulator")
        self.root.geometry("800x600")
        self.style = tb.Style(theme="darkly")
        
        self.detector = DeadlockDetector()
        self.processes = []
        self.resources = []
        
        self.create_gui()
        self.update_history()
    
    def create_gui(self):
        """Create the main GUI layout with the modern design"""
        main_frame = tb.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = tb.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        tb.Label(
            title_frame, 
            text="Resource Allocation Graph Analysis", 
            font=("Helvetica", 18, "bold"),
            bootstyle="inverse-light"
        ).pack(pady=(0, 5))
        
        tb.Label(
            title_frame, 
            text="Add process-resource dependencies to detect potential deadlocks",
            bootstyle="inverse-secondary"
        ).pack()
       
        panel_frame = tb.Frame(main_frame)
        panel_frame.pack(fill=tk.BOTH, expand=True)
        
        left_panel = tb.Frame(panel_frame, bootstyle="light")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 7.5))
        
        input_frame = tb.LabelFrame(left_panel, text="Resource Allocation", padding=10, bootstyle="info")
        input_frame.pack(fill=tk.X, pady=10, padx=5)
        
        process_frame = tb.Frame(input_frame)
        process_frame.pack(fill=tk.X, pady=5)
        
        tb.Label(process_frame, text="Process:", width=12, anchor=tk.W).pack(side=tk.LEFT, padx=5)
        
        self.process_var = tk.StringVar()
        self.process_combo = ttk.Combobox(process_frame, textvariable=self.process_var)
        self.process_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.process_combo['values'] = ['P1', 'P2', 'P3', 'P4', 'P5']
        
        tb.Button(
            process_frame, 
            text="Add New", 
            command=self.add_new_process,
            bootstyle="light-outline",
            width=8
        ).pack(side=tk.RIGHT, padx=5)
        
        resource_frame = tb.Frame(input_frame)
        resource_frame.pack(fill=tk.X, pady=5)
        
        tb.Label(resource_frame, text="Resource:", width=12, anchor=tk.W).pack(side=tk.LEFT, padx=5)
        
        self.resource_var = tk.StringVar()
        self.resource_combo = ttk.Combobox(resource_frame, textvariable=self.resource_var)
        self.resource_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.resource_combo['values'] = ['R1', 'R2', 'R3', 'R4', 'R5']
        
        tb.Button(
            resource_frame, 
            text="Add New", 
            command=self.add_new_resource,
            bootstyle="light-outline",
            width=8
        ).pack(side=tk.RIGHT, padx=5)
        
        button_frame = tb.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        tb.Button(
            button_frame, 
            text="Request Resource", 
            command=self.add_dependency,
            bootstyle="info",
            width=16
        ).pack(side=tk.LEFT, padx=5)
        
        tb.Button(
            button_frame, 
            text="Allocate Resource",
            command=self.allocate_resource,
            bootstyle="success",
            width=16
        ).pack(side=tk.LEFT, padx=5)
        
        tb.Button(
            button_frame, 
            text="Release Resource",
            command=self.release_resource,
            bootstyle="warning",
            width=16
        ).pack(side=tk.LEFT, padx=5)
        
        detect_frame = tb.Frame(left_panel)
        detect_frame.pack(fill=tk.X, pady=10, padx=5)
        
        tb.Button(
            detect_frame, 
            text="Detect Deadlock",
            command=self.check_deadlock,
            bootstyle="danger",
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        tb.Button(
            detect_frame, 
            text="Visualize Graph",
            command=lambda: visualize_graph(self.detector.graph),
            bootstyle="primary",
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar(value="System Status: Ready")
        self.status_label = tb.Label(
            left_panel, 
            textvariable=self.status_var,
            font=("Helvetica", 12),
            bootstyle="secondary"
        )
        self.status_label.pack(fill=tk.X, pady=10, padx=5)
        
        right_panel = tb.Frame(panel_frame, bootstyle="light")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(7.5, 0))
        
        history_frame = tb.LabelFrame(right_panel, text="Resource Allocation History", padding=10, bootstyle="secondary")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)
        
        scroll_frame = tb.Frame(history_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = tb.Scrollbar(scroll_frame, orient="vertical", bootstyle="round")
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(
            scroll_frame, 
            height=20, 
            bg="#2E3440", 
            fg="#D8DEE9",
            font=("Consolas", 10),
            wrap=tk.WORD,
            yscrollcommand=scroll_y.set
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.history_text.yview)
        
        control_frame = tb.Frame(right_panel)
        control_frame.pack(fill=tk.X, pady=5, padx=5)
        
        tb.Button(
            control_frame, 
            text="Clear All",
            command=self.clear_all,
            bootstyle="secondary-outline"
        ).pack(side=tk.RIGHT, padx=5)
    
    def add_new_process(self):
        next_num = len(self.processes) + 1
        new_process = f"P{next_num}"
        if new_process not in self.processes:
            self.processes.append(new_process)
            self.process_combo['values'] = self.processes
            self.process_var.set(new_process)
            self.log_action(f"Added new process: {new_process}")
    
    def add_new_resource(self):
        next_num = len(self.resources) + 1
        new_resource = f"R{next_num}"
        if new_resource not in self.resources:
            self.resources.append(new_resource)
            self.resource_combo['values'] = self.resources
            self.resource_var.set(new_resource)
            self.log_action(f"Added new resource: {new_resource}")
    
    def add_dependency(self):
        process = self.process_var.get().strip()
        resource = self.resource_var.get().strip()
        if not process or not resource:
            self.show_error("Please select both Process and Resource")
            return
        process = f"P{process}" if not process.startswith("P") else process
        resource = f"R{resource}" if not resource.startswith("R") else resource
        self.detector.add_dependency(process, resource)
        self.update_status(f"Process {process} requested {resource}", "info")
        self.update_history()
        self.check_for_deadlock_silent()
    
    def allocate_resource(self):
        process = self.process_var.get().strip()
        resource = self.resource_var.get().strip()
        if not process or not resource:
            self.show_error("Please select both Process and Resource")
            return
        process = f"P{process}" if not process.startswith("P") else process
        resource = f"R{resource}" if not resource.startswith("R") else resource
        try:
            if self.detector.graph.has_edge(process, resource):
                self.detector.graph.remove_edge(process, resource)
            self.detector.graph.add_edge(resource, process)
            self.update_status(f"Resource {resource} allocated to {process}", "success")
            self.update_history()
            self.check_for_deadlock_silent()
        except AttributeError:
            self.show_error("Error: Unable to allocate resource.")
    
    def release_resource(self):
        process = self.process_var.get().strip()
        resource = self.resource_var.get().strip()
        if not process or not resource:
            self.show_error("Please select both Process and Resource")
            return
        process = f"P{process}" if not process.startswith("P") else process
        resource = f"R{resource}" if not resource.startswith("R") else resource
        self.detector.release_resource(process, resource)
        self.update_status(f"Released {resource} from {process}", "warning")
        self.update_history()
    
    def check_deadlock(self):
        is_deadlocked, deadlocked_nodes = self.detector.detect_deadlock()
        if is_deadlocked:
            deadlocked_list = ", ".join(sorted(deadlocked_nodes))
            self.update_status(f"DEADLOCK DETECTED! Involving: {deadlocked_list}", "danger")
            messagebox.showwarning("Deadlock Detected", 
                                  f"A deadlock has been detected involving nodes:\n{deadlocked_list}")
        else:
            self.update_status("No deadlock detected in the system", "success")
        visualize_graph(self.detector.graph)  # Removed deadlocked_nodes as it’s handled in visualize_graph
        self.update_history()
    
    def check_for_deadlock_silent(self):
        is_deadlocked, deadlocked_nodes = self.detector.detect_deadlock()
        if is_deadlocked:
            deadlocked_list = ", ".join(sorted(deadlocked_nodes))
            self.update_status(f"DEADLOCK DETECTED! Involving: {deadlocked_list}", "danger")
    
    def clear_all(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to clear all data?"):
            self.detector = DeadlockDetector()
            self.update_status("System reset successfully", "secondary")
            self.update_history()
    
    def update_status(self, message, status_type):
        self.status_var.set(f"System Status: {message}")
        self.status_label.configure(bootstyle=status_type)
    
    def update_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        nodes = list(self.detector.graph.nodes())
        edges = list(self.detector.graph.edges())
        self.history_text.insert(tk.END, "==== CURRENT SYSTEM STATE ====\n\n")
        if not nodes:
            self.history_text.insert(tk.END, "No processes or resources added yet.\n")
        else:
            processes = sorted([n for n in nodes if n.startswith("P")])
            self.history_text.insert(tk.END, f"Processes ({len(processes)}):\n")
            self.history_text.insert(tk.END, ", ".join(processes) + "\n\n")
            resources = sorted([n for n in nodes if n.startswith("R")])
            self.history_text.insert(tk.END, f"Resources ({len(resources)}):\n")
            self.history_text.insert(tk.END, ", ".join(resources) + "\n\n")
            if edges:
                self.history_text.insert(tk.END, "Relationships:\n")
                requests = [(s, t) for s, t in edges if s.startswith("P") and t.startswith("R")]
                if requests:
                    self.history_text.insert(tk.END, "Requests (Process → Resource):\n")
                    for s, t in sorted(requests):
                        self.history_text.insert(tk.END, f"  • {s} → {t}\n")
                allocations = [(s, t) for s, t in edges if s.startswith("R") and t.startswith("P")]
                if allocations:
                    self.history_text.insert(tk.END, "\nAllocations (Resource → Process):\n")
                    for s, t in sorted(allocations):
                        self.history_text.insert(tk.END, f"  • {s} → {t}\n")
            else:
                self.history_text.insert(tk.END, "No relationships defined yet.\n")
        self.history_text.config(state=tk.DISABLED)
    
    def log_action(self, message):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"• {message}\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = DeadlockDetectionApp(root)
    root.mainloop()
