
import mido


class MidiDevice:
    def __init__(self, name):
        self._name = name
        self._in_ports = []

    @property
    def in_ports(self):
        return self._in_ports

    @property
    def name(self):
        return self._name

    @property
    def num(self):
        if self._in_ports:
            return self._in_ports[0].device_num
        return None

    @property
    def ui_name(self):
        return f"{self.num} :: {self.name}"

    def register_in_port(self, port):
        self._in_ports.append(port)


class InPort:
    def __init__(self, mido_name):
        self._mido_name = mido_name

        split_point = mido_name.rfind(' ')
        self._device_name, self._name = mido_name[:split_point].split(':')
        self._device_num, self._num = mido_name[split_point+1:].split(':')

    @property
    def device_name(self):
        return self._device_name

    @property
    def device_num(self):
        return self._device_num

    @property
    def mido_name(self):
        return self._mido_name

    @property
    def name(self):
        return self._name

    @property
    def num(self):
        return self._num

    @property
    def port_id(self):
        return f"{self._device_num}:{self._num}"

    @property
    def ui_name(self):
        return f"{self.port_id} :: {self.name}"


class MidiDevices:

    def __init__(self):
        self._devices = {}
        self._ports = {}

    def devices(self):
        for num in self._devices:
            yield self._devices[num]

    def refresh(self):
        processed = []
        for full_name in mido.get_input_names():
            port = InPort(full_name)
            if port.port_id in processed:
                continue
            processed.append(port.port_id)

            if port.device_num not in self._devices:
                self._devices[port.device_num] = MidiDevice(port.device_name)
            self._devices[port.device_num].register_in_port(port)
            self._ports[port.port_id] = port
