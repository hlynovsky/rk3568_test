import time
import os
import logging

class GPIO():
    def __init__(self):
        pass
    
    def gpio_operations(self, pin):
        try:
            pin_path = f"/sys/class/gpio/gpio{pin}"
            
            # Export pin
            try:
                with open("/sys/class/gpio/export", "w") as f:
                    f.write(str(pin))
            except OSError:
                # Pin might already be exported
                pass
                
            # Set pin as input
            try:
                with open(pin_path + "/direction", "w") as f:
                    f.write("in")
            except Exception as e:
                logging.error(f"Failed to set direction for GPIO{pin}: {str(e)}")
                return 1
                
            # Read initial state
            try:
                with open(pin_path + "/value", "r") as f:
                    value = f.read().strip()
                logging.info(f"GPIO{pin} initial value: {value}")
            except Exception as e:
                logging.error(f"Failed to read initial value for GPIO{pin}: {str(e)}")
                return 1
                
            # Set pin as output and write 0
            try:
                with open(pin_path + "/direction", "w") as f:
                    f.write("out")
                with open(pin_path + "/value", "w") as f:
                    f.write("0")
            except Exception as e:
                logging.error(f"Failed to set output and write 0 for GPIO{pin}: {str(e)}")
                return 1
                
            # Read value after writing 0
            try:
                with open(pin_path + "/value", "r") as f:
                    value = f.read().strip()
                logging.info(f"GPIO{pin} after writing 0: {value}")
            except Exception as e:
                logging.error(f"Failed to read value after writing 0 for GPIO{pin}: {str(e)}")
                return 1
                
            # Write 1
            try:
                with open(pin_path + "/value", "w") as f:
                    f.write("1")
            except Exception as e:
                logging.error(f"Failed to write 1 for GPIO{pin}: {str(e)}")
                return 1
                
            # Read value after writing 1
            try:
                with open(pin_path + "/value", "r") as f:
                    value = f.read().strip()
                print(f"GPIO{pin} after writing 1: {value}")
            except Exception as e:
                logging.error(f"Failed to read value after writing 1 for GPIO{pin}: {str(e)}")
                return 1
                
            # Unexport pin
            try:
                with open("/sys/class/gpio/unexport", "w") as f:
                    f.write(str(pin))
            except Exception as e:
                logging.error(f"Failed to unexport GPIO{pin}: {str(e)}")
                return 1
                
            return 0 
            
        except Exception as e:
            logging.error(f"General error for GPIO{pin}: {str(e)}")
            return 1
        
    def run(self):
        for pin in range(20, 63):
            if pin != 23:  # Исключаем 23-й пин
                self.gpio_operations(pin)
                time.sleep(0.25) 
        return 0