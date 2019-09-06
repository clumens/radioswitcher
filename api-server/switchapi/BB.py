import Adafruit_BBIO.GPIO as GPIO

class BB(object):
    def __init__(self, xverters=None):
        self._activeGpioPin = None
        self._initialized = False
        self._previouslyActive = None

        # These are the pins on the BeagleBone which are hooked up to a pin on
        # the relay board.  It is assumed they are connected in the same order.
        # That is, P8_7 -> In1, P8_8 -> In2, ..., P9_16 -> In8.
        self._gpioPinsUsed = [ "P8_7", "P8_8", "P8_9", "P8_10",
                               "P9_13", "P9_14", "P9_15", "P9_16" ]

        self._pins = {}

        if xverters == None:
            for p in self._gpioPinsUsed:
                self._pins[p] = None
        else:
            if len(xverters) != 8:
                raise ValueError("Exactly eight pin definitions must be given")

            for ndx, name in enumerate(self._gpioPinsUsed):
                self._pins[name] = xverters[ndx]

    @property
    def activeBand(self):
        if not self._initialized:
            raise RuntimeError("Hardware is not initialized")

        if not self._activeGpioPin:
            return None
        else:
            return self._pins[self._activeGpioPin].band

    def activateBand(self, band):
        if not self._initialized:
            raise RuntimeError("Hardware is not initialized")

        pin = self._pinForBand(band)
        if not pin:
            raise ValueError("Unsupported band: " + band)

        self._activatePin(pin)

    @property
    def bands(self):
        objs = filter(lambda obj: obj is not None, self._pins.values())
        return sorted([obj.band for obj in list(objs)])

    def deactivateBand(self, band):
        if not self._initialized:
            raise RuntimeError("Hardware is not initialized")

        pin = self._pinForBand(band)
        if not pin:
            raise ValueError("Unsupported band: " + band)

        self._deactivatePin(pin)

    @property
    def defaultBand(self):
        for name, obj in self._pins.items():
            if obj and obj.isDefault:
                return name

        return self._pins.keys()[0].band

    def initHW(self):
        self.__relaysInit()
        self._initialized = True

    def _activatePin(self, name):
        if not self._initialized:
            raise RuntimeError("Hardware is not initialized")

        if name not in self._gpioPinsUsed:
            raise ValueError("Pin " + name + " is not supported")

        self.__activatePin(name)

    # Like _activatePin, but without any checking
    def __activatePin(self, name):
        # We only allow one active pin at a time, so if one was previously active
        # it must first be deactivated.
        if self._activeGpioPin:
            self.__deactivatePin(self._activeGpioPin)

        GPIO.output(name, GPIO.LOW)
        self._activeGpioPin = name

    def _deactivatePin(self, name):
        if not self._initialized:
            raise RuntimeError("Hardware is not initialized")

        self.__deactivatePin(name)

    # Like _deactivatePin, but without any checking
    def __deactivatePin(self, name):
        GPIO.output(name, GPIO.HIGH)
        self._activeGpioPin = None

    def _pinForBand(self, band):
        for pin, obj in self._pins.items():
            if obj and obj.band == band:
                return pin

        return None

    def __relaysInit(self):
        default = None

        if self._initialized:
            return

        for name, obj in self._pins.items():
            # Initialize everything to HIGH (off) by default.
            GPIO.setup(name, GPIO.OUT)
            self.__deactivatePin(name)

            # If this pin is marked as the default, grab that and save it
            # for after we get done with everything else.  If nothing is
            # marked as default, all pins will be left HIGH (off).
            if obj and obj.isDefault:
                default = name

        # If there was a default pin, set it to LOW (on) now.
        if default:
            self.__activatePin(default)
