import pytest
from app.services.dmx.DMX_data import DMXData
import os
from datetime import datetime

class TestDMXData:
    @pytest.fixture
    def dmx(self):
        """Fixture che fornisce un'istanza pulita di DMXData per ogni test"""
        dmx = DMXData()
        dmx.reset()
        yield dmx
        # Pulizia dopo il test
        if os.path.exists("test_log.txt"):
            os.remove("test_log.txt")

    def test_singleton_pattern(self):
        """Verifica che la classe sia un singleton"""
        dmx1 = DMXData()
        dmx2 = DMXData()
        assert dmx1 is dmx2

    def test_initial_channels_zeroed(self, dmx):
        """Verifica che tutti i canali siano inizializzati a 0"""
        for i in range(1, 513):
            assert dmx.channels[i] == 0

    def test_set_channel_valid(self, dmx):
        """Verifica l'impostazione corretta di un canale"""
        dmx.set_channel(1, 255)
        assert dmx.channels[1] == 255

        dmx.set_channel(512, 128)
        assert dmx.channels[512] == 128

    def test_set_channel_invalid_channel(self, dmx):
        """Verifica che venga sollevata un'eccezione per canali non validi"""
        with pytest.raises(ValueError):
            dmx.set_channel(0, 255)
        
        with pytest.raises(ValueError):
            dmx.set_channel(513, 255)

    def test_set_channel_invalid_value(self, dmx):
        """Verifica che venga sollevata un'eccezione per valori non validi"""
        with pytest.raises(ValueError):
            dmx.set_channel(1, -1)
        
        with pytest.raises(ValueError):
            dmx.set_channel(1, 256)

    def test_write_channels_on_log(self, dmx):
        """Verifica la scrittura dei canali su file di log"""
        log_file = "test_log.txt"
        dmx.set_channel(1, 255)
        dmx.write_channels_on_log(log_file)
        
        with open(log_file, 'r') as f:
            content = f.read()
            assert "255" in content
            assert datetime.now().strftime("%H:%M:%S") in content

    def test_clear_log_file(self, dmx):
        """Verifica la pulizia del file di log"""
        log_file = "test_log.txt"
        with open(log_file, 'w') as f:
            f.write("test content")
        
        dmx.clear_log_file(log_file)
        
        with open(log_file, 'r') as f:
            assert f.read() == ""

    def test_write_channels_on_console(self, dmx, capsys):
        """Verifica la stampa dei canali sulla console"""
        dmx.set_channel(1, 255)
        dmx.write_channels_on_console()
        captured = capsys.readouterr()
        assert "255" in captured.out

    # Test per i metodi non implementati
    def test_open_not_implemented(self, dmx):
        """Verifica che il metodo open non sia implementato"""
        with pytest.raises(NotImplementedError):
            dmx.open()

    def test_send_not_implemented(self, dmx):
        """Verifica che il metodo send non sia implementato"""
        with pytest.raises(NotImplementedError):
            dmx.send("localhost", 1234)

    def test_close_not_implemented(self, dmx):
        """Verifica che il metodo close non sia implementato"""
        with pytest.raises(NotImplementedError):
            dmx.close()