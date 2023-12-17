#!/usr/bin/env python
# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for adb."""

from io import BytesIO
import struct
import unittest
from mock import mock


from adb import common
from adb import adb_commands
from adb import adb_protocol
from adb.usb_exceptions import TcpTimeoutException, DeviceNotFoundError
import common_stub


BANNER = b'blazetest'
LOCAL_ID = 1
REMOTE_ID = 2


class BaseAdbTest(unittest.TestCase):

  @classmethod
  def _ExpectWrite(cls, usb, command, arg0, arg1, data):
    usb.ExpectWrite(cls._MakeHeader(command, arg0, arg1, data))
    usb.ExpectWrite(data)
    if command == b'WRTE':
      cls._ExpectRead(usb, b'OKAY', 0, 0)

  @classmethod
  def _ExpectRead(cls, usb, command, arg0, arg1, data=b''):
    usb.ExpectRead(cls._MakeHeader(command, arg0, arg1, data))
    if data:
      usb.ExpectRead(data)
    if command == b'WRTE':
      cls._ExpectWrite(usb, b'OKAY', LOCAL_ID, REMOTE_ID, b'')

  @classmethod
  def _ConvertCommand(cls, command):
    return sum(c << (i * 8) for i, c in enumerate(bytearray(command)))

  @classmethod
  def _MakeHeader(cls, command, arg0, arg1, data):
    command = cls._ConvertCommand(command)
    magic = command ^ 0xFFFFFFFF
    checksum = adb_protocol.AdbMessage.CalculateChecksum(data)
    return struct.pack(b'<6I', command, arg0, arg1, len(data), checksum, magic)

  @classmethod
  def _ExpectConnection(cls, usb):
    cls._ExpectWrite(usb, b'CNXN', 0x01000000, 4096, b'host::%s\0' % BANNER)
    cls._ExpectRead(usb, b'CNXN', 0, 0, b'device::\0')

  @classmethod
  def _ExpectOpen(cls, usb, service):
    cls._ExpectWrite(usb, b'OPEN', LOCAL_ID, 0, service)
    cls._ExpectRead(usb, b'OKAY', REMOTE_ID, LOCAL_ID)

  @classmethod
  def _ExpectClose(cls, usb):
    cls._ExpectRead(usb, b'CLSE', REMOTE_ID, 0)
    cls._ExpectWrite(usb, b'CLSE', LOCAL_ID, REMOTE_ID, b'')

  @classmethod
  def _Connect(cls, usb):
    return adb_commands.AdbCommands.Connect(usb, BANNER)


class AdbTest(BaseAdbTest):
  @classmethod
  def _ExpectCommand(cls, service, command, *responses):
    usb = common_stub.StubUsb(device=None, setting=None)
    cls._ExpectConnection(usb)
    cls._ExpectOpen(usb, b'%s:%s\0' % (service, command))

    for response in responses:
      cls._ExpectRead(usb, b'WRTE', REMOTE_ID, 0, response)
    cls._ExpectClose(usb)
    return usb

  def testConnect(self):
    usb = common_stub.StubUsb(device=None, setting=None)
    self._ExpectConnection(usb)

    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)

  def testConnectSerialString(self):
    dev = adb_commands.AdbCommands()

    with mock.patch.object(common.UsbHandle, 'FindAndOpen', return_value=None):
      with mock.patch.object(adb_commands.AdbCommands, '_Connect', return_value=None):
        dev.ConnectDevice(serial='/dev/invalidHandle')

  def testSmallResponseShell(self):
    command = b'keepin it real'
    response = 'word.'
    usb = self._ExpectCommand(b'shell', command, response)

    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    self.assertEqual(response, dev.Shell(command))

  def testBigResponseShell(self):
    command = b'keepin it real big'
    # The data doesn't have to be big, the point is that it just concatenates
    # the data from different WRTEs together.
    responses = [b'other stuff, ', b'and some words.']

    usb = self._ExpectCommand(b'shell', command, *responses)

    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    self.assertEqual(b''.join(responses).decode('utf8'),
                     dev.Shell(command))

  def testUninstall(self):
    package_name = "com.test.package"
    response = 'Success'

    usb = self._ExpectCommand(b'shell', ('pm uninstall "%s"' % package_name).encode('utf8'), response)

    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    self.assertEqual(response, dev.Uninstall(package_name))

  def testStreamingResponseShell(self):
    command = b'keepin it real big'
    # expect multiple lines

    responses = ['other stuff, ', 'and some words.']

    usb = self._ExpectCommand(b'shell', command, *responses)

    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    response_count = 0
    for (expected,actual) in zip(responses, dev.StreamingShell(command)):
      self.assertEqual(expected, actual)
      response_count = response_count + 1
    self.assertEqual(len(responses), response_count)

  def testReboot(self):
    usb = self._ExpectCommand(b'reboot', b'', b'')
    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    dev.Reboot()

  def testRebootBootloader(self):
    usb = self._ExpectCommand(b'reboot', b'bootloader', b'')
    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    dev.RebootBootloader()

  def testRemount(self):
    usb = self._ExpectCommand(b'remount', b'', b'')
    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    dev.Remount()

  def testRoot(self):
    usb = self._ExpectCommand(b'root', b'', b'')
    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    dev.Root()

  def testEnableVerity(self):
    usb = self._ExpectCommand(b'enable-verity', b'', b'')
    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    dev.EnableVerity()

  def testDisableVerity(self):
    usb = self._ExpectCommand(b'disable-verity', b'', b'')
    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    dev.DisableVerity()

class FilesyncAdbTest(BaseAdbTest):

  @classmethod
  def _MakeSyncHeader(cls, command, *int_parts):
    command = cls._ConvertCommand(command)
    return struct.pack(b'<%dI' % (len(int_parts) + 1), command, *int_parts)

  @classmethod
  def _MakeWriteSyncPacket(cls, command, data=b'', size=None):
    if not isinstance(data, bytes):
      data = data.encode('utf8')
    return cls._MakeSyncHeader(command, size or len(data)) + data

  @classmethod
  def _ExpectSyncCommand(cls, write_commands, read_commands):
    usb = common_stub.StubUsb(device=None, setting=None)
    cls._ExpectConnection(usb)
    cls._ExpectOpen(usb, b'sync:\0')

    while write_commands or read_commands:
      if write_commands:
        command = write_commands.pop(0)
        cls._ExpectWrite(usb, b'WRTE', LOCAL_ID, REMOTE_ID, command)

      if read_commands:
        command = read_commands.pop(0)
        cls._ExpectRead(usb, b'WRTE', REMOTE_ID, LOCAL_ID, command)

    cls._ExpectClose(usb)
    return usb

  def testPush(self):
    filedata = b'alo there, govnah'
    mtime = 100

    send = [
        self._MakeWriteSyncPacket(b'SEND', b'/data,33272'),
        self._MakeWriteSyncPacket(b'DATA', filedata),
        self._MakeWriteSyncPacket(b'DONE', size=mtime),
    ]
    data = b'OKAY\0\0\0\0'
    usb = self._ExpectSyncCommand([b''.join(send)], [data])

    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    dev.Push(BytesIO(filedata), '/data', mtime=mtime)

  def testPull(self):
    filedata = b"g'ddayta, govnah"

    recv = self._MakeWriteSyncPacket(b'RECV', b'/data')
    data = [
        self._MakeWriteSyncPacket(b'DATA', filedata),
        self._MakeWriteSyncPacket(b'DONE'),
    ]
    usb = self._ExpectSyncCommand([recv], [b''.join(data)])
    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=usb, banner=BANNER)
    self.assertEqual(filedata, dev.Pull('/data'))


class TcpTimeoutAdbTest(BaseAdbTest):
        
  @classmethod
  def _ExpectCommand(cls, service, command, *responses):
    tcp = common_stub.StubTcp('10.0.0.123')
    cls._ExpectConnection(tcp)
    cls._ExpectOpen(tcp, b'%s:%s\0' % (service, command))

    for response in responses:
      cls._ExpectRead(tcp, b'WRTE', REMOTE_ID, 0, response)
    cls._ExpectClose(tcp)
    return tcp
  
  def _run_shell(self, cmd, timeout_ms=None):
    tcp = self._ExpectCommand(b'shell', cmd)
    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=tcp, banner=BANNER)
    dev.Shell(cmd, timeout_ms=timeout_ms)

  def testConnect(self):
    tcp = common_stub.StubTcp('10.0.0.123')
    self._ExpectConnection(tcp)
    dev = adb_commands.AdbCommands()
    dev.ConnectDevice(handle=tcp, banner=BANNER)

  def testTcpTimeout(self):
    timeout_ms = 1  
    command = b'i_need_a_timeout'
    self.assertRaises(
            TcpTimeoutException, 
            self._run_shell, 
            command, 
            timeout_ms=timeout_ms)


class TcpHandleTest(unittest.TestCase):
  def testInitWithHost(self):
    tcp = common_stub.StubTcp('10.11.12.13')

    self.assertEqual('10.11.12.13:5555', tcp._serial_number)
    self.assertEqual(None, tcp._timeout_ms)

  def testInitWithHostAndPort(self):
    tcp = common_stub.StubTcp('10.11.12.13:5678')

    self.assertEqual('10.11.12.13:5678', tcp._serial_number)
    self.assertEqual(None, tcp._timeout_ms)

  def testInitWithTimeout(self):
    tcp = common_stub.StubTcp('10.0.0.2', timeout_ms=234.5)

    self.assertEqual('10.0.0.2:5555', tcp._serial_number)
    self.assertEqual(234.5, tcp._timeout_ms)

  def testInitWithTimeoutInt(self):
    tcp = common_stub.StubTcp('10.0.0.2', timeout_ms=234)

    self.assertEqual('10.0.0.2:5555', tcp._serial_number)
    self.assertEqual(234.0, tcp._timeout_ms)

if __name__ == '__main__':
  unittest.main()
