"""Connector and runner regressions; no adapter or serial dependency required."""

import importlib
import os
import sys
import time
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest

import apprunner
from bteve import registers as reg
from bteve.gameduino import Gameduino
from bteve.gameduino_spidriver import GameduinoSPIDriver
from bteve.registers import REG_CMDB_SPACE, REG_HSIZE, REG_ID, REG_PCLK, REG_VSIZE


def mock_chip(gd, chip_id=0x011708):
    memory = {REG_ID: 0x7c, reg.REG_CPURESET: 0, 0xc0000: chip_id,
              REG_CMDB_SPACE: 4092, REG_HSIZE: 480, REG_VSIZE: 272}

    def read(address, count):
        return memory.get(address, 0).to_bytes(count, 'little')

    def write(address, data):
        memory[address] = int.from_bytes(data, 'little')

    gd.rd = Mock(side_effect=read)
    gd.wr = Mock(side_effect=write)
    return memory


def test_spi_framing_and_error_cleanup():
    driver = Mock()
    gd = GameduinoSPIDriver(driver)
    driver.reset_mock()
    driver.read.return_value = b'\x00\x7c\x00\x00\x00'
    assert gd.rd32(REG_ID) == 0x7c
    assert driver.method_calls == [
        ('sel', (), {}), ('write', (b'\x30\x20\x00',), {}),
        ('read', (5,), {}), ('unsel', (), {})]
    driver.reset_mock()
    gd.wr(0x1234, b'payload')
    driver.write.assert_called_once_with(b'\x80\x12\x34payload')
    driver.read.assert_called_once_with(0)

    for operation in (driver.write, driver.read):
        operation.side_effect = OSError('SPI failed')
        driver.reset_mock()
        with pytest.raises(OSError, match='SPI failed'):
            gd.transfer(b'abc', 4)
        driver.unsel.assert_called_once_with()
        operation.side_effect = None


def test_minimal_startup_skips_display_configuration():
    gd = Gameduino()
    gd.transfer = Mock(return_value=b'')
    mock_chip(gd, chip_id=0x011608)
    gd.standard_startup = Mock()
    gd.init(minimal=True)
    assert (gd.w, gd.h, gd.space) == (480, 272, 4092)
    gd.standard_startup.assert_not_called()
    assert [call.args[0] for call in gd.transfer.call_args_list] == [
        b'\x00\x00\x00', b'\x68\x00\x00']
    gd.init()
    gd.standard_startup.assert_called_once_with()


def test_gameduino_default_loads_flash_startup(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda _: None)
    gd = GameduinoSPIDriver(Mock())
    memory = mock_chip(gd, chip_id=0x011608)
    memory[0xffc] = 0x7c6a0100
    gd.cmd_flashread = Mock(wraps=gd.cmd_flashread)
    gd.cmd_regwrite = Mock(wraps=gd.cmd_regwrite)
    gd.init()
    gd.cmd_flashread.assert_called_once_with(0, 0x1000, 0x1000)
    gd.rd.assert_any_call(0, 512)
    gd.cmd_regwrite.assert_any_call(reg.REG_GPIO, 0x83)


@pytest.fixture
def spi_connector(monkeypatch):
    driver = Mock(product='spidriverq')
    factory = Mock(return_value=driver)
    monkeypatch.setitem(sys.modules, 'spidriver', SimpleNamespace(SPIDriver=factory))
    monkeypatch.setitem(sys.modules, 'connectors.cspidriver', None)
    monkeypatch.delitem(sys.modules, 'connectors.cspidriver')
    return importlib.import_module('connectors.cspidriver'), driver, factory


@pytest.mark.parametrize('product', ['spidriver1', 'spidriver2', 'spidriverq'])
def test_adapter_setup_and_close(spi_connector, product):
    connector, driver, factory = spi_connector
    driver.product = product
    gd = connector.EVE('~/ports/test')
    factory.assert_called_once_with(os.path.expanduser('~/ports/test'))
    assert isinstance(gd, GameduinoSPIDriver)
    driver.seta.assert_called_once_with(1)
    driver.setb.assert_called_once_with(1)
    driver.setmode.assert_called_once_with(0)
    if product == 'spidriverq':
        driver.set_width.assert_called_once_with(1)
    else:
        driver.set_width.assert_not_called()
    gd.close()
    driver.close.assert_called_once_with()

    driver.close.reset_mock()
    driver.setmode.side_effect = OSError('setup failed')
    with pytest.raises(OSError, match='setup failed'):
        connector.EVE('/dev/test')
    driver.close.assert_called_once_with()


@pytest.mark.parametrize('board,width,height,hcycle,pclk_freq,pclk_2x,pclk', [
    ('riverdi-ips35', 320, 240, 371, 0x022, 0, 1),
    ('riverdi-ips43', 480, 272, 531, 0x032, 0, 1),
    ('riverdi-ips50', 800, 480, 816, 0xd14, 0, 3),
    ('riverdi-ips70', 1024, 600, 1344, 0xd12, 0, 1),
    ('riverdi-ips101', 1280, 800, 1440, 0x8c1, 1, 1),
])
def test_riverdi_display_startup(spi_connector, monkeypatch, board, width, height,
                                hcycle, pclk_freq, pclk_2x, pclk):
    connector, driver, _ = spi_connector
    events = Mock()
    monkeypatch.setattr(time, 'sleep', events.sleep)
    gd = connector.EVE('/dev/test', board=board)
    memory = mock_chip(gd)
    events.attach_mock(gd.wr, "write")
    gd.cmd_flashread = Mock()
    gd.init()
    assert (gd.w, gd.h, gd.chip_model) == (width, height, 817)
    assert memory[REG_HSIZE] == width
    assert memory[REG_VSIZE] == height
    assert memory[reg.REG_HCYCLE] == hcycle
    assert memory[reg.REG_PCLK_FREQ] == pclk_freq
    assert memory[reg.REG_PCLK_2X] == pclk_2x
    assert memory[REG_PCLK] == pclk
    writes = [(c.args[0], int.from_bytes(c.args[1], 'little'))
              for c in gd.wr.call_args_list]
    assert writes.index((reg.REG_HCYCLE, hcycle)) < writes.index((REG_PCLK, pclk))
    if board == 'riverdi-ips50':
        events.assert_has_calls([
            call.write(REG_PCLK, bytes([pclk])),
            call.sleep(0.12),
            call.write(reg.REG_GPIOX, b'\x00\x90'),
            call.sleep(0.25),
            call.write(reg.REG_PWM_DUTY, bytes([128])),
        ])
    else:
        assert writes.index((REG_PCLK, pclk)) < writes.index((reg.REG_PWM_DUTY, 128))
    gd.cmd_flashread.assert_not_called()
    driver.seta.assert_not_called()
    driver.setb.assert_not_called()


@pytest.mark.parametrize('board', ['riverdi', 'riverdi-ips50'])
def test_riverdi_minimal_skips_panel_and_flash(spi_connector, monkeypatch, board):
    connector, driver, _ = spi_connector
    monkeypatch.setattr(time, 'sleep', lambda _: None)
    gd = connector.EVE('/dev/test', board=board, oscillator='internal')
    memory = mock_chip(gd)
    gd.cmd_flashread = Mock()
    gd.init(minimal=True)
    assert (gd.w, gd.h) == (480, 272)
    assert memory[reg.REG_FREQUENCY] == 72000000
    assert b'\x48\x00\x00' in [call.args[0] for call in driver.write.call_args_list]
    assert {REG_HSIZE, REG_VSIZE, REG_PCLK, reg.REG_PWM_DUTY}.isdisjoint(
        call.args[0] for call in gd.wr.call_args_list)
    gd.cmd_flashread.assert_not_called()


@pytest.mark.parametrize('register,value,error', [
    (REG_ID, 0xff, TimeoutError),
    (reg.REG_CPURESET, 1, TimeoutError),
    (0xc0000, 0x011608, ValueError),
])
def test_riverdi_refuses_to_configure_unready_or_wrong_chip(
        spi_connector, monkeypatch, register, value, error):
    connector, _, _ = spi_connector
    gd = connector.EVE('/dev/test', board='riverdi-ips50')
    memory = mock_chip(gd)
    memory[register] = value
    ticks = iter(range(1000))
    monkeypatch.setattr(time, 'sleep', lambda _: None)
    monkeypatch.setattr(time, 'monotonic', lambda: next(ticks) / 10)
    with pytest.raises(error):
        gd.init()
    assert REG_PCLK not in memory


def test_unknown_board_rejected_before_open(spi_connector):
    connector, _, factory = spi_connector
    with pytest.raises(ValueError, match='unknown|Unknown'):
        connector.EVE('/dev/test', board='no-such-panel')
    factory.assert_not_called()


def test_riverdi_requires_panel_for_full_startup(spi_connector, monkeypatch):
    connector, _, _ = spi_connector
    monkeypatch.setattr(time, 'sleep', lambda _: None)
    gd = connector.EVE('/dev/test', board='riverdi')
    memory = mock_chip(gd)
    with pytest.raises(ValueError, match='part number'):
        gd.init()
    assert REG_PCLK not in memory


@pytest.mark.parametrize('failure', [None, 'init', 'app', 'finish', 'construct'])
def test_runner_lifetime_and_app_arguments(monkeypatch, failure):
    events = []
    original_argv = ['demo.py', '-c', 'test', '--port', '/dev/test',
                     '--minimal', '--application-option', '42']
    monkeypatch.setattr(sys, 'argv', original_argv)

    def step(name):
        events.append(name)
        if name == failure:
            raise RuntimeError(name)

    class Device:
        def __init__(self, port):
            assert port == '/dev/test'
            step('construct')

        def init(self, minimal=False):
            assert minimal
            step('init')

        def finish(self):
            step('finish')

        def close(self):
            step('close')

    def add_arguments(parser):
        parser.add_argument('--port', required=True)

    monkeypatch.setitem(sys.modules, 'connectors.test',
                        SimpleNamespace(EVE=Device, add_arguments=add_arguments))

    def app(gd):
        assert sys.argv == ['demo.py', '--application-option', '42']
        step('app')
        return 123

    if failure:
        with pytest.raises(RuntimeError, match=failure):
            apprunner.run(app)
    else:
        assert apprunner.run(app) == 123
    assert sys.argv is original_argv
    expected = ['construct', 'init', 'app', 'finish']
    if failure:
        expected = expected[:expected.index(failure) + 1]
    if failure != 'construct':
        expected.append('close')
    assert events == expected


def test_missing_connector_and_dependency_are_distinguished(monkeypatch, capsys):
    with pytest.raises(SystemExit):
        apprunner.run(lambda gd: None, argv=['-c', 'does_not_exist'])
    assert 'Unknown connector: does_not_exist' in capsys.readouterr().err

    def missing_dependency(name):
        raise ModuleNotFoundError("No module named 'spidriver'", name='spidriver')

    monkeypatch.setattr(apprunner.importlib, 'import_module', missing_dependency)
    with pytest.raises(SystemExit):
        apprunner.run(lambda gd: None, argv=[])
    assert "requires missing module 'spidriver'" in capsys.readouterr().err


def test_runner_separates_application_and_connector_options(monkeypatch):
    device = Mock()
    factory = Mock(return_value=device)
    def connector_arguments(parser):
        parser.add_argument('--port', required=True)
    def app_arguments(parser):
        parser.add_argument('--output', default='capture.png')
    monkeypatch.setitem(sys.modules, 'connectors.test', SimpleNamespace(
        EVE=factory, add_arguments=connector_arguments))
    app = Mock(return_value=123)
    assert apprunner.run(app, argv=['-c', 'test', '--port', '/dev/test',
                                    '--output', 'custom.png'],
                         add_arguments=app_arguments) == 123
    factory.assert_called_once_with(port='/dev/test')
    assert app.call_args.args[0] is device
    assert app.call_args.args[1].output == 'custom.png'
    device.finish.assert_called_once_with()
    device.close.assert_called_once_with()


@pytest.mark.parametrize('failure', [None, 'destination', 'read', 'timeout'])
def test_screenshot_restores_display_on_success_and_failure(monkeypatch, failure):
    from bteve import eve as eve_module
    gd = Gameduino()
    gd.w, gd.h = 2, 1
    gd.finish = Mock()
    gd.rd32 = Mock(return_value=3)
    gd.wr32 = Mock()
    def read(address, count):
        if address == 0x3020e8:
            return b'\x01' * 8 if failure == 'timeout' else bytes(8)
        assert (address, count) == (0x3c2000, 8)
        if failure == 'read':
            raise OSError('read failed')
        return bytes([1, 2, 3, 255, 4, 5, 6, 255])
    gd.rd = read
    destination = Mock(side_effect=OSError('destination failed')
                       if failure == 'destination' else None)
    monkeypatch.setattr(eve_module.time, 'sleep', lambda _: None)
    ticks = iter([0, 2])
    monkeypatch.setattr(eve_module.time, 'monotonic', lambda: next(ticks))
    if failure:
        with pytest.raises(TimeoutError if failure == 'timeout' else OSError):
            gd.screenshot(destination)
    else:
        gd.screenshot(destination)
        destination.assert_called_once_with(bytes([3, 2, 1, 6, 5, 4]))
    writes = [call.args for call in gd.wr32.call_args_list]
    assert writes[-3:] == [(0x302174, 0), (0x302010, 0), (REG_PCLK, 3)]
