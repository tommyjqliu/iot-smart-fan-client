from asyncio import create_task, sleep
from rpi_ws281x import PixelStrip, Color

LED_GPIO = 18
LED_COUNT = 16  # LED灯的个数
LED_PIN = 18  # DI端接GPIO18
# 以下可以不用改
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

class Led:
    def __init__(self, led_gpio = LED_GPIO):
        self.strip = PixelStrip(LED_COUNT, led_gpio, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        create_task(self.colorWipe(Color(0,0,255)))
    
    def wheel(self, pos):
        """生成横跨0-255个位置的彩虹颜色."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    async def colorWipe(self, color, wait_ms=2000):
        """一次擦除显示像素的颜色."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        await sleep(wait_ms / 1000.0)

    async def theaterChase(self, color, wait_ms=50, iterations=10):
        """电影影院灯光风格的追逐动画."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    async def rainbow(self, wait_ms=20, iterations=1):
        """绘制彩虹，褪色的所有像素一次."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            sleep(wait_ms / 1000.0)

    async def rainbowCycle(self, wait_ms=10, iterations=5):
        """画出均匀分布在所有像素上的彩虹."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            sleep(wait_ms / 1000.0)

    async def theaterChaseRainbow(self, wait_ms=50):
        """旋转的彩色灯光."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)
    
    def on_close(self):
        create_task(self.colorWipe(Color(0,0,0)))