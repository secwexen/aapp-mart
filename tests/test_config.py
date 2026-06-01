"""
Unit tests for configuration management (v1.2.0)
"""

import os
import pytest
from unittest.mock import patch
from src.aapp_mart.common.config import (
    ConfigLoader,
    ConfigurationError,
    get_config,
    reset_config,
    AppEnvironment,
    LogLevel,
)


class TestConfigLoader:
    """Test suite for ConfigLoader."""
    
    def setup_method(self):
        """Reset global config before each test."""
        reset_config()
    
    def teardown_method(self):
        """Clean up after each test."""
        reset_config()
    
    def test_load_default_config(self):
        """Test loading config with default values."""
        loader = ConfigLoader()
        config = loader.load(fail_fast=False)
        
        assert config is not None
        assert config.app.app_name == "AAPP-MART"
        assert config.app.debug is False
        assert config.api.port == 8000
        assert config.red_team.max_agents == 5
    
    def test_load_from_environment(self):
        """Test loading config from environment variables."""
        with patch.dict(os.environ, {
            "APP_NAME": "TEST-APP",
            "APP_ENV": "production",
            "DEBUG": "true",
            "LOG_LEVEL": "DEBUG",
            "MAX_AGENTS": "10",
            "PORT": "9000",
        }):
            loader = ConfigLoader()
            config = loader.load(fail_fast=False)
            
            assert config.app.app_name == "TEST-APP"
            assert config.app.app_env == AppEnvironment.PRODUCTION
            assert config.app.debug is True
            assert config.app.log_level == LogLevel.DEBUG
            assert config.red_team.max_agents == 10
            assert config.api.port == 9000
    
    def test_production_requires_secret_key(self):
        """Test that SECRET_KEY is required in production."""
        with patch.dict(os.environ, {
            "APP_ENV": "production",
            "SECRET_KEY": "",  # Empty
        }, clear=False):
            loader = ConfigLoader()
            
            with pytest.raises(ConfigurationError):
                loader.load(fail_fast=True)
    
    def test_port_validation(self):
        """Test port range validation."""
        with patch.dict(os.environ, {
            "PORT": "99999",  # Invalid
        }, clear=False):
            loader = ConfigLoader()
            
            with pytest.raises(ConfigurationError):
                loader.load(fail_fast=True)
    
    def test_max_agents_range(self):
        """Test max_agents range validation."""
        with patch.dict(os.environ, {
            "MAX_AGENTS": "0",  # Too low
        }, clear=False):
            loader = ConfigLoader()
            
            with pytest.raises(ConfigurationError):
                loader.load(fail_fast=True)
    
    def test_simulation_timeout_range(self):
        """Test simulation timeout range validation."""
        with patch.dict(os.environ, {
            "SIMULATION_TIMEOUT": "10",  # Too low (min 30)
        }, clear=False):
            loader = ConfigLoader()
            
            with pytest.raises(ConfigurationError):
                loader.load(fail_fast=True)
    
    def test_temperature_range(self):
        """Test model temperature range validation."""
        with patch.dict(os.environ, {
            "MODEL_TEMPERATURE": "3.0",  # Too high (max 2.0)
        }, clear=False):
            loader = ConfigLoader()
            
            with pytest.raises(ConfigurationError):
                loader.load(fail_fast=True)
    
    def test_report_format_validation(self):
        """Test report format validation."""
        with patch.dict(os.environ, {
            "REPORT_FORMAT": "invalid",
        }, clear=False):
            loader = ConfigLoader()
            
            with pytest.raises(ConfigurationError):
                loader.load(fail_fast=True)
    
    def test_boolean_parsing(self):
        """Test boolean value parsing."""
        test_cases = [
            ("true", True),
            ("false", False),
            ("1", True),
            ("0", False),
            ("yes", True),
            ("no", False),
            ("on", True),
            ("off", False),
        ]
        
        for value_str, expected in test_cases:
            with patch.dict(os.environ, {
                "DEBUG": value_str,
            }, clear=False):
                loader = ConfigLoader()
                config = loader.load(fail_fast=False)
                assert config.app.debug == expected
    
    def test_get_config_singleton(self):
        """Test that get_config returns singleton instance."""
        config1 = get_config()
        config2 = get_config()
        
        assert config1 is config2
    
    def test_reset_config(self):
        """Test that reset_config clears singleton."""
        config1 = get_config()
        reset_config()
        config2 = get_config()
        
        assert config1 is not config2
    
    def test_comprehensive_config_load(self):
        """Test loading all config sections together."""
        with patch.dict(os.environ, {
            "APP_NAME": "AAPP-MART-TEST",
            "APP_ENV": "staging",
            "DEBUG": "true",
            "LOG_LEVEL": "DEBUG",
            "SECRET_KEY": "test-secret-key",
            "JWT_SECRET": "jwt-secret",
            "JWT_EXPIRATION": "7200",
            "DB_PROVIDER": "postgres",
            "MAX_AGENTS": "20",
            "SIMULATION_TIMEOUT": "600",
            "SIMULATION_DEPTH": "15",
            "MODEL_PROVIDER": "local",
            "MODEL_NAME": "llama-2",
            "MODEL_TEMPERATURE": "0.5",
            "MODEL_MAX_TOKENS": "4096",
            "HOST": "127.0.0.1",
            "PORT": "8080",
            "REPORT_FORMAT": "html",
            "ENABLE_THREAT_FEEDS": "false",
        }, clear=False):
            loader = ConfigLoader()
            config = loader.load(fail_fast=False)
            
            # Verify all sections
            assert config.app.app_name == "AAPP-MART-TEST"
            assert config.app.app_env == AppEnvironment.STAGING
            assert config.app.debug is True
            assert config.security.secret_key == "test-secret-key"
            assert config.security.jwt_expiration == 7200
            assert config.red_team.max_agents == 20
            assert config.red_team.simulation_timeout == 600
            assert config.model.model_name == "llama-2"
            assert config.model.temperature == 0.5
            assert config.api.host == "127.0.0.1"
            assert config.api.port == 8080
            assert config.report.format == "html"
            assert config.threat_intel.enable_threat_feeds is False


class TestConfigIntegration:
    """Integration tests for configuration."""
    
    def setup_method(self):
        """Reset config before each test."""
        reset_config()
    
    def teardown_method(self):
        """Clean up after each test."""
        reset_config()
    
    def test_production_security_strict(self):
        """Test strict production security requirements."""
        with patch.dict(os.environ, {
            "APP_ENV": "production",
            "SECRET_KEY": "prod-secret-very-long-and-secure-key-12345",
        }, clear=False):
            config = get_config()
            
            # Production requires SECRET_KEY
            assert config.security.secret_key is not None
            assert len(config.security.secret_key) > 20
    
    def test_development_relaxed_requirements(self):
        """Test development mode has relaxed requirements."""
        with patch.dict(os.environ, {
            "APP_ENV": "development",
        }, clear=False):
            config = get_config()
            
            # Development allows empty SECRET_KEY
            assert config.app.app_env == AppEnvironment.DEVELOPMENT
    
    def test_config_immutability(self):
        """Test that config is properly structured."""
        config = get_config()
        
        # Verify all sections exist
        assert hasattr(config, 'app')
        assert hasattr(config, 'security')
        assert hasattr(config, 'database')
        assert hasattr(config, 'red_team')
        assert hasattr(config, 'model')
        assert hasattr(config, 'threat_intel')
        assert hasattr(config, 'api')
        assert hasattr(config, 'cli')
        assert hasattr(config, 'report')
        assert hasattr(config, 'experimental')


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
