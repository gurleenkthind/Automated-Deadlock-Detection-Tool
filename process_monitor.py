import psutil

def get_system_processes():
    """Fetch running system processes."""
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        processes.append((proc.info['pid'], proc.info['name']))
    return processes
