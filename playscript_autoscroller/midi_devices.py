
import os

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
        if os.name == 'nt':
            return self.name
        return f"{self.num} :: {self.name}"

    def register_in_port(self, port):
        self._in_ports.append(port)


class InPort:
    def __init__(self, mido_name):
        self._mido_name = mido_name

        split_point = mido_name.rfind(' ')
        if os.name == 'nt':
            if mido_name.find('(') > -1:
                self._device_name = mido_name[mido_name.find('(')+1:mido_name.find(')')]
            else:
                self._device_name = mido_name[:split_point]
            self._name = 'Input'

            self._device_num = None
            self._num = int(mido_name[split_point+1:]) + 1
        else:
            # {device name}:{port name} {dev#}:{port#}
            # Both device and port names may have colons in.
            colon_split = mido_name.count(':', 0, split_point) // 2 + 1
            device = mido_name[:split_point].split(':')
            self._device_name = ':'.join(device[0:colon_split])
            self._name = ':'.join(device[colon_split:])
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
        if os.name == 'nt':
            return f"{self.name} {self._num}"
        return f"{self.port_id} :: {self.name}"


class MidiDevices:

    def __init__(self):
        self._devices = {}
        self._ports = {}

    def devices(self):
        return self._devices.values()

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
