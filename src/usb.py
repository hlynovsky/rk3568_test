import os
import time
import logging
import subprocess


class Usb:
    TEST_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    TEST_FILE = 'test_file'
    READ_FILE = 'test_read_file'

    def __init__(self, usb_paths, log_file='logs/test.log'):
        self.usb_paths = usb_paths
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(self.log_file)]
        )
        
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        logging.getLogger().addHandler(console)


    def run_command(self, command):
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Command execution failed: {e}")
            raise

    def create_test_file(self):
        logging.debug("Creating a test file...")
        with open(self.TEST_FILE, 'wb') as f:
            f.write(os.urandom(self.TEST_FILE_SIZE))

    def check_free_space(self, mount_point):
        statvfs = os.statvfs(mount_point)
        free_space = statvfs.f_bavail * statvfs.f_frsize
        if free_space < self.TEST_FILE_SIZE:
            logging.error(f"Not enough free space on {mount_point}")
            return False
        return True

    def mount_all(self):
        for path in self.usb_paths:
            dev_path = path.replace('/media/', '/dev/')
            if not os.path.exists(path):
                self.run_command(f'sudo mkdir -p {path}')
            try:
                self.run_command(f'sudo mount {dev_path} {path}')
                logging.debug(f"Mounted {dev_path} to {path}")
            except Exception:
                logging.error(f"Failed to mount {dev_path} to {path}")

    def unmount_all(self):
        for path in self.usb_paths:
            try:
                self.run_command(f'sudo umount {path}')
                logging.debug(f"Unmounted {path}")
            except Exception:
                logging.warning(f"Failed to unmount {path}")
            if os.path.exists(path):
                self.run_command(f'sudo rmdir {path}')

    def test_write_speed(self, mount_point):
        dest_path = os.path.join(mount_point, self.TEST_FILE)
        try:
            logging.debug("Testing write speed...")
            start_time = time.time()
            self.run_command(f'cp {self.TEST_FILE} {dest_path}')
            end_time = time.time()
            write_speed = self.TEST_FILE_SIZE / (end_time - start_time) / (1024 * 1024)
            logging.debug(f"Write speed: {write_speed:.2f} MB/s")
            return write_speed
        except Exception as e:
            logging.error(f"Write error: {e}")
            return None

    def test_read_speed(self, mount_point):
        source_path = os.path.join(mount_point, self.TEST_FILE)
        try:
            if not os.path.exists(source_path):
                logging.error("File for read test not found!")
                return None
            logging.debug("Testing read speed...")
            start_time = time.time()
            self.run_command(f'cp {source_path} {self.READ_FILE}')
            end_time = time.time()
            read_speed = self.TEST_FILE_SIZE / (end_time - start_time) / (1024 * 1024)
            logging.debug(f"Read speed: {read_speed:.2f} MB/s")
            return read_speed
        except Exception as e:
            logging.error(f"Read error: {e}")
            return None

    def clean_temp_files(self):
        for file in [self.TEST_FILE, self.READ_FILE]:
            if os.path.exists(file):
                os.remove(file)
                logging.debug(f"Temporary file removed: {file}")

    def run_tests(self):
        try:
            self.create_test_file()
            self.mount_all()
            for mount_point in self.usb_paths:
                logging.debug(f"\nStarting test for {mount_point}")
                if not self.check_free_space(mount_point):
                    continue
                write_speed = self.test_write_speed(mount_point)
                read_speed = self.test_read_speed(mount_point)
                if write_speed and read_speed:
                    logging.info(f"USB {mount_point} Write speed = {write_speed:.2f} MB/s OK | Read speed = {read_speed:.2f} MB/s OK")
                dest_path = os.path.join(mount_point, self.TEST_FILE)
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                    logging.debug(f"File removed from {mount_point}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.clean_temp_files()
            self.unmount_all()