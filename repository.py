import os

class ScanRepository:
    """Manage storage of raw scan data under a base directory."""

    def __init__(self, base_path='data/raw_data'):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def host_dir(self, ip):
        """Ensure and return directory for a given host IP."""
        path = os.path.join(self.base_path, ip)
        os.makedirs(path, exist_ok=True)
        return path

    def file_path(self, ip, filename):
        """Return the full path for a file belonging to a host."""
        return os.path.join(self.host_dir(ip), filename)

    def ensure_file(self, path):
        """Ensure that a file exists by creating it with 'NULL' if absent."""
        if not os.path.isfile(path):
            with open(path, 'w') as f:
                f.write("NULL")
        return path
