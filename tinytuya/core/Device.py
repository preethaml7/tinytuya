# TinyTuya Module
# -*- coding: utf-8 -*-

import logging

from .XenonDevice import XenonDevice
from . import command_types as CT


log = logging.getLogger(__name__)

class Device(XenonDevice):
    #def __init__(self, *args, **kwargs):
    #    super(Device, self).__init__(*args, **kwargs)

    def set_status(self, on, switch=1, nowait=False):
        """
        Set status of the device to 'on' or 'off'.

        Args:
            on(bool):  True for 'on', False for 'off'.
            switch(int): The switch to set
            nowait(bool): True to send without waiting for response.
        """
        # open device, send request, then close connection
        if isinstance(switch, int):
            switch = str(switch)  # index and payload is a string
        payload = self.generate_payload(CT.CONTROL, {switch: on})

        data = self._send_receive(payload, getresponse=(not nowait))
        log.debug("set_status received data=%r", data)

        return data

    def product(self):
        """
        Request AP_CONFIG Product Info from device. [BETA]

        """
        # open device, send request, then close connection
        payload = self.generate_payload(CT.AP_CONFIG)
        data = self._send_receive(payload, 0)
        log.debug("product received data=%r", data)
        return data

    def heartbeat(self, nowait=True):
        """
        Send a keep-alive HEART_BEAT command to keep the TCP connection open.

        Devices only send an empty-payload response, so no need to wait for it.

        Args:
            nowait(bool): True to send without waiting for response.
        """
        # open device, send request, then close connection
        payload = self.generate_payload(CT.HEART_BEAT)
        data = self._send_receive(payload, 0, getresponse=(not nowait))
        log.debug("heartbeat received data=%r", data)
        return data

    def updatedps(self, index=None, nowait=False):
        """
        Request device to update index.

        Args:
            index(array): list of dps to update (ex. [4, 5, 6, 18, 19, 20])
            nowait(bool): True to send without waiting for response.
        """
        if index is None:
            index = [1]

        log.debug("updatedps() entry (dev_type is %s)", self.dev_type)
        # open device, send request, then close connection
        payload = self.generate_payload(CT.UPDATEDPS, index)
        data = self._send_receive(payload, 0, getresponse=(not nowait))
        log.debug("updatedps received data=%r", data)
        return data

    def set_value(self, index, value, nowait=False):
        """
        Set int value of any index.

        Args:
            index(int): index to set
            value(int): new value for the index
            nowait(bool): True to send without waiting for response.
        """
        # open device, send request, then close connection
        if isinstance(index, int):
            index = str(index)  # index and payload is a string

        payload = self.generate_payload(CT.CONTROL, {index: value})

        data = self._send_receive(payload, getresponse=(not nowait))

        return data

    def set_multiple_values(self, data, nowait=False):
        """
        Set multiple indexes at the same time

        Args:
            data(dict): array of index/value pairs to set
            nowait(bool): True to send without waiting for response.
        """
        out = {}
        for i in data:
            out[str(i)] = data[i]
        payload = self.generate_payload(CT.CONTROL, out)
        return self._send_receive(payload, getresponse=(not nowait))

    def turn_on(self, switch=1, nowait=False):
        """Turn the device on"""
        return self.set_status(True, switch, nowait)

    def turn_off(self, switch=1, nowait=False):
        """Turn the device off"""
        return self.set_status(False, switch, nowait)

    def set_timer(self, num_secs, dps_id=0, nowait=False):
        """
        Set a timer.

        Args:
            num_secs(int): Number of seconds
            dps_id(int): DPS Index for Timer
            nowait(bool): True to send without waiting for response.
        """

        # Query status, pick last device id as that is probably the timer
        if dps_id == 0:
            status = self.status()
            if "dps" in status:
                devices = status["dps"]
                devices_numbers = list(devices.keys())
                devices_numbers.sort()
                dps_id = devices_numbers[-1]
            else:
                log.debug("set_timer received error=%r", status)
                return status

        payload = self.generate_payload(CT.CONTROL, {dps_id: num_secs})

        data = self._send_receive(payload, getresponse=(not nowait))
        log.debug("set_timer received data=%r", data)
        return data