import board
import busio as io
import adafruit_mlx90614

class Temperature:
    def __init__(self):
        # Initialize the I2C bus
        self.i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
        # Create a sensor instance
        self.mlx = adafruit_mlx90614.MLX90614(self.i2c)

    @property
    def ambient_temperature(self):
        # Return the ambient temperature formatted to two decimal places
        return "{:.2f}".format(self.mlx.ambient_temperature)

    @property
    def target_temperature(self):
        # Return the target/object temperature formatted to two decimal places
        return "{:.2f}".format(self.mlx.object_temperature)

    def on_close(self):
        pass