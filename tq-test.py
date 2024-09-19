import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import csv
from datetime import datetime

# Create the I2C bus / ADC object
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)

# Create analog inputs for all four channels
channels = [
    AnalogIn(ads, ADS.P0),
    AnalogIn(ads, ADS.P1),
    AnalogIn(ads, ADS.P2),
    AnalogIn(ads, ADS.P3)
]

# Set up the load cell parameters for each sensor
CALIBRATION_FACTORS = [1000, 1000, 1000, 1000]  # Calibrate these values
ZERO_OFFSETS = [0, 0, 0, 0]  # Determine these values

# CSV file name
CSV_FILE = "load_cell_data.csv"

def read_load_cells():
    forces = []
    for i, chan in enumerate(channels):
        adc_value = chan.value
        force_kg = (adc_value - ZERO_OFFSETS[i]) / CALIBRATION_FACTORS[i]
        forces.append(force_kg)
    return forces

def write_to_csv(timestamp, forces):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp] + forces)

def main():
    print("Multi-Sensor Load Cell Measurement Script")
    print(f"Taking readings every 15 minutes and writing to {CSV_FILE}")
    print("Press Ctrl-C to exit")
    
    # Create CSV file with headers if it doesn't exist
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Force1 (kg)", "Force2 (kg)", "Force3 (kg)", "Force4 (kg)"])
    
    try:
        while True:
            forces = read_load_cells()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"Timestamp: {timestamp}")
            for i, force in enumerate(forces, 1):
                print(f"Sensor {i}: {force:.2f} kg")
            
            write_to_csv(timestamp, [f"{force:.2f}" for force in forces])
            
            # Wait for 15 minutes
            time.sleep(15 * 60)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
