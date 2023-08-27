from machine import Pin, PWM

class Servo:
    def __init__(self, pin, freq, minangle, maxangle, desc):
        self.__min_u10_duty = 26 - 0 # offset for correction
        self.__max_u10_duty = 123- 0  # offset for correction
        self.desc = desc
        self.__servo_pwm_freq = freq
        self.min_angle = 0
        self.max_angle = 180
        self.current_angle = 0.001
        self.__initialise(pin)
    
    def return_state(self,each):
        return {
            "name": each,
            "desc": self.desc,
            "freq": self.__servo_pwm_freq,
            "min_angle": self.min_angle,
            "max_angle": self.max_angle,
            "current_angle": self.current_angle
            }


    def update_settings(self, servo_pwm_freq, min_u10_duty, max_u10_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u10_duty = min_u10_duty
        self.__max_u10_duty = max_u10_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)


    def move(self, data):
        if "angle" in data:
            angle = int(data["angle"])
            if angle >= self.min_angle and angle <= self.max_angle:
                angle = round(angle, 2)
                if angle == self.current_angle:
                    return
                self.current_angle = angle
                duty_u10 = self.__angle_to_u10_duty(angle)
                self.__motor.duty(duty_u10)

    def __angle_to_u10_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u10_duty


    def __initialise(self, pin):
        self.current_angle = 0.001
        self.__angle_conversion_factor = (self.__max_u10_duty - self.__min_u10_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)

class Plugin():
    def __init__(self, config):
        if "SERVOS" in config:
            config = config["SERVOS"]
        self.servos = {}
        for each in config.keys():
            self.servos[config[each]["name"]] = Servo(config[each]["pin"], config[each]["freq"], config[each]["minangle"], config[each]["maxangle"], config[each]["desc"])
    
    def get_states(self):
        mydict = {}
        for each in self.servos:
            mydict.update({each:self.servos[each].return_state(each)})
        return mydict

    def return_functions(self):
        mydict = {}
        for each in self.servos:
            mydict.update({each:[self.servos[each].move, [ ["Int", "angle", "move angle between min/max_angle"] ] ]})
        return mydict

    