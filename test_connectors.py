"""Connector and runner regressions; no adapter or serial dependency required."""

import importlib
import os
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import apprunner
from bteve.gameduino import Gameduino
from bteve.gameduino_spidriver import GameduinoSPIDriver
from bteve.registers import REG_CMDB_SPACE, REG_HSIZE, REG_ID, REG_VSIZE


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
    registers = {REG_ID: 0x7c, REG_CMDB_SPACE: 4092, REG_HSIZE: 480, REG_VSIZE: 272}
    gd.rd32 = Mock(side_effect=registers.__getitem__)
    gd.standard_startup = Mock()
    gd.init(minimal=True)
    assert (gd.w, gd.h, gd.space) == (480, 272, 4092)
    gd.standard_startup.assert_not_called()
    assert [call.args[0] for call in gd.transfer.call_args_list] == [
        b'\x00\x00\x00', b'\x68\x00\x00']
    gd.init()
    gd.standard_startup.assert_called_once_with()


@pytest.mark.parametrize('product', ['spidriver1', 'spidriver2', 'spidriverq'])
def test_adapter_setup_and_close(monkeypatch, product):
    driver = Mock(product=product)
    factory = Mock(return_value=driver)
    monkeypatch.setitem(sys.modules, 'spidriver', SimpleNamespace(SPIDriver=factory))
    monkeypatch.setitem(sys.modules, 'connectors.cspidriver', None)
    monkeypatch.delitem(sys.modules, 'connectors.cspidriver')
    connector = importlib.import_module('connectors.cspidriver')
    gd = connector.EVE('~/ports/test')
    factory.assert_called_once_with(os.path.expanduser('~/ports/test'))
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
