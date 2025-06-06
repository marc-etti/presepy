import pytest
from unittest.mock import Mock, patch
import threading

from app.services.dmx.DMX_logic import (
    init_lights_from_db, 
    main_dmx_function, 
    closing_function,
    dmx,
    pause_event,
    state_manager
)


class TestInitLightsFromDB:
    
    @patch('app.services.dmx.DMX_logic.Device')
    @patch('app.services.dmx.DMX_logic.FaroController')
    def test_init_lights_from_db_with_devices(self, mock_faro_controller, mock_device):
        """Test initialization with light devices in database"""
        # Arrange
        mock_light1 = Mock(name="light1")
        mock_light2 = Mock(name="light2")
        mock_device.query.filter_by.return_value.all.return_value = [mock_light1, mock_light2]
        
        # Act
        result = init_lights_from_db()
        
        # Assert
        mock_device.query.filter_by.assert_called_once_with(type="light")
        assert len(result) == 2
        assert mock_faro_controller.call_count == 2
    
    @patch('app.services.dmx.DMX_logic.Device')
    def test_init_lights_from_db_no_devices(self, mock_device):
        """Test initialization with no light devices in database"""
        # Arrange
        mock_device.query.filter_by.return_value.all.return_value = []
        
        # Act
        result = init_lights_from_db()
        
        # Assert
        assert result == []
        mock_device.query.filter_by.assert_called_once_with(type="light")


class TestMainDMXFunction:
    
    @patch('app.services.dmx.DMX_logic.init_lights_from_db')
    @patch('app.services.dmx.DMX_logic.Phase')
    @patch('app.services.dmx.DMX_logic.time.sleep')
    @patch('app.services.dmx.DMX_logic.state_manager')
    def test_main_dmx_function_single_phase(self, mock_state_mgr, mock_sleep, mock_phase, mock_init_lights):
        """Test main DMX function with single phase"""
        # Arrange
        mock_app = Mock()
        mock_app.app_context.return_value.__enter__ = Mock()
        mock_app.app_context.return_value.__exit__ = Mock()
        
        mock_phase_obj = Mock()
        mock_phase_obj.name = "test_phase"
        mock_phase_obj.duration = 1.0
        mock_phase.get_phases.return_value = [mock_phase_obj]
        
        mock_light = Mock()
        mock_init_lights.return_value = [mock_light]
        
        # Simulate state manager being on for one iteration then off
        mock_state_mgr.is_on.side_effect = [True, True, False]
        
        # Act
        main_dmx_function(mock_app)
        
        # Assert
        mock_app.app_context.assert_called_once()
        mock_phase.get_phases.assert_called_once()
        mock_init_lights.assert_called_once()
        mock_state_mgr.set_phase.assert_called_with("test_phase")
    
    @patch('app.services.dmx.DMX_logic.init_lights_from_db')
    @patch('app.services.dmx.DMX_logic.Phase')
    @patch('app.services.dmx.DMX_logic.time.sleep')
    @patch('app.services.dmx.DMX_logic.state_manager')
    def test_main_dmx_function_system_off(self, mock_state_mgr, mock_sleep, mock_phase, mock_init_lights):
        """Test main DMX function when system is off"""
        # Arrange
        mock_app = Mock()
        mock_app.app_context.return_value.__enter__ = Mock()
        mock_app.app_context.return_value.__exit__ = Mock()
        
        mock_state_mgr.is_on.return_value = False
        
        # Act
        main_dmx_function(mock_app)
        
        # Assert
        mock_phase.get_phases.assert_called_once()
        mock_init_lights.assert_called_once()
    
    @patch('app.services.dmx.DMX_logic.init_lights_from_db')
    @patch('app.services.dmx.DMX_logic.Phase')
    @patch('app.services.dmx.DMX_logic.time.sleep')
    @patch('app.services.dmx.DMX_logic.state_manager')
    @patch('app.services.dmx.DMX_logic.pause_event')
    def test_main_dmx_function_with_pause(self, mock_pause_event, mock_state_mgr, mock_sleep, mock_phase, mock_init_lights):
        """Test main DMX function with pause event"""
        # Arrange
        mock_app = Mock()
        mock_app.app_context.return_value.__enter__ = Mock()
        mock_app.app_context.return_value.__exit__ = Mock()
        
        mock_phase_obj = Mock()
        mock_phase_obj.name = "test_phase"
        mock_phase_obj.duration = 0.1
        mock_phase.get_phases.return_value = [mock_phase_obj]
        
        mock_light = Mock()
        mock_init_lights.return_value = [mock_light]
        
        mock_state_mgr.is_on.side_effect = [True, True, True, False]
        mock_pause_event.is_set.side_effect = [False, True]  # First iteration paused, then resumed
        
        # Act
        main_dmx_function(mock_app)
        
        # Assert
        mock_pause_event.wait.assert_called_once()
    
    @patch('app.services.dmx.DMX_logic.init_lights_from_db')
    @patch('app.services.dmx.DMX_logic.Phase')
    @patch('app.services.dmx.DMX_logic.time.sleep')
    @patch('app.services.dmx.DMX_logic.state_manager')
    @patch('app.services.dmx.DMX_logic.dmx')
    def test_main_dmx_function_dmx_write(self, mock_dmx, mock_state_mgr, mock_sleep, mock_phase, mock_init_lights):
        """Test main DMX function writes to DMX"""
        # Arrange
        mock_app = Mock()
        mock_app.app_context.return_value.__enter__ = Mock()
        mock_app.app_context.return_value.__exit__ = Mock()
        
        mock_phase_obj = Mock()
        mock_phase_obj.name = "test_phase"
        mock_phase_obj.duration = 0.1
        mock_phase.get_phases.return_value = [mock_phase_obj]
        
        mock_light = Mock()
        mock_init_lights.return_value = [mock_light]
        
        mock_state_mgr.is_on.side_effect = [True, True, True, False]
        
        # Act
        main_dmx_function(mock_app)
        
        # Assert
        mock_dmx.write_channels_on_log.assert_called()


class TestClosingFunction:
    
    def test_closing_function(self, capsys):
        """Test closing function prints expected message"""
        # Act
        closing_function()
        
        # Assert
        captured = capsys.readouterr()
        assert "Interfaccia DMX chiusa" in captured.out


class TestModuleGlobals:
    
    def test_dmx_instance_creation(self):
        """Test DMX instance is created"""
        assert dmx is not None
    
    def test_pause_event_creation(self):
        """Test pause event is created as threading.Event"""
        assert isinstance(pause_event, threading.Event)
    
    def test_state_manager_creation(self):
        """Test state manager instance is created"""
        assert state_manager is not None