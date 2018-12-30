from .can import CANSocket
from .config import get_config_value, create_default_configfile
from .timer import Timer


class ChassisController:
    def __init__(self, create_config=True):
        if create_config:
            create_default_configfile()

        self.can1, self.can2, self.can3 = self.connect_can_buses()

        self.heartbeat_freq = int(get_config_value("HEARTBEAT", "heartbeat-frequency"))
        self.heartbeat_timer = Timer(1/self.heartbeat_freq, self.heartbeat_loop)
        self.inverter_heartbeat_frequency = int(get_config_value("HEARTBEAT", "inverter-frequency"))
        self.inverter_send_heartbeat = False
        self.amu_heartbeat_frequency = int(get_config_value("HEARTBEAT", "amu-frequency"))
        self.amu_send_heartbeat = False
        self.pdm_heartbeat_frequency = int(get_config_value("HEARTBEAT", "pdm-frequency"))
        self.pdm_send_heartbeat = False
        self.shutdown_heartbeat_frequency = int(get_config_value("HEARTBEAT", "shutdown-frequency"))
        self.shutdown_send_heartbeat = False
        self.wheel_heartbeat_frequency = int(get_config_value("HEARTBEAT", "wheel-frequency"))
        self.wheel_send_heartbeat = False
        self.heartbeat_counter = 0

    def heartbeat_loop(self):
        self.heartbeat_counter += 1

        if self.heartbeat_counter >= (self.heartbeat_freq / self.inverter_heartbeat_frequency):
            self.inverter_send_heartbeat = True
        if self.heartbeat_counter >= (self.heartbeat_freq / self.amu_heartbeat_frequency):
            self.amu_send_heartbeat = True
        if self.heartbeat_counter >= (self.heartbeat_freq / self.pdm_heartbeat_frequency):
            self.pdm_send_heartbeat = True
        if self.heartbeat_counter >= (self.heartbeat_freq / self.shutdown_heartbeat_frequency):
            self.shutdown_send_heartbeat = True
        if self.heartbeat_counter >= (self.heartbeat_freq / self.wheel_heartbeat_frequency):
            self.wheel_send_heartbeat = True
        if self.heartbeat_counter >= self.heartbeat_freq:
            self.heartbeat_counter = 0

    def start(self):
        self.heartbeat_timer.start()
        while True:
            if self.inverter_send_heartbeat:
                # TODO Send info on CAN
                self.inverter_send_heartbeat = False

            if self.amu_send_heartbeat:
                # TODO Send info on CAN
                self.amu_send_heartbeat = False

            if self.pdm_send_heartbeat:
                # TODO Send info on CAN
                self.pdm_send_heartbeat = False

            if self.shutdown_send_heartbeat:
                # TODO Send info on CAN
                self.shutdown_send_heartbeat = False

            if self.wheel_send_heartbeat:
                # TODO Send info on CAN
                self.wheel_send_heartbeat = False

    @classmethod
    def connect_can_buses(cls):
        can1_interface = get_config_value("CAN", "can1-interface")
        can1 = CANSocket(can1_interface)
        can2_interface = get_config_value("CAN", "can2-interface")
        can2 = CANSocket(can2_interface)
        can3_interface = get_config_value("CAN", "can3-interface")
        can3 = CANSocket(can3_interface)
        return can1, can2, can3

