"""
Configuration Management for AAPP-MART v1.2.0

Handles:
- Environment variable loading with strict schema validation
- Fail-fast behavior for invalid configurations
- Type coercion and default values
- Security-first approach (no hardcoded secrets)
- Contextual logging of configuration errors
"""

import os
import logging
from typing import Any, Dict, Optional, Type, TypeVar, List, Union
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum
import sys

from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator, ValidationError, root_validator


# ============================================================================
# Environment Setup
# ============================================================================

def load_environment():
    """
    Load environment variables from .env file if it exists.
    Looks for .env in current directory and parent directories up to project root.
    """
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Try parent directories (for nested execution)
        for parent in Path.cwd().parents:
            env_candidate = parent / ".env"
            if env_candidate.exists():
                load_dotenv(env_candidate)
                break


# Load environment on module import
load_environment()


# ============================================================================
# Enums
# ============================================================================

class AppEnvironment(str, Enum):
    """Application deployment environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DBProvider(str, Enum):
    """Supported database providers."""
    COSMOS = "cosmos"
    POSTGRES = "postgres"
    SQLITE = "sqlite"


class ModelProvider(str, Enum):
    """Supported AI model providers."""
    MICROSOFT = "microsoft"
    OPENAI = "openai"
    LOCAL = "local"


# ============================================================================
# Pydantic Configuration Models
# ============================================================================

class AppConfig(BaseModel):
    """Core application configuration."""
    
    app_name: str = Field(default="AAPP-MART", description="Application name")
    app_env: AppEnvironment = Field(
        default=AppEnvironment.DEVELOPMENT,
        description="Deployment environment"
    )
    debug: bool = Field(default=False, description="Debug mode")
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    
    class Config:
        use_enum_values = True


class SecurityConfig(BaseModel):
    """Security and authentication configuration."""
    
    secret_key: Optional[str] = Field(
        default=None,
        description="Secret key for signing (required in production)"
    )
    jwt_secret: Optional[str] = Field(
        default=None,
        description="JWT signing secret (required if JWT enabled)"
    )
    jwt_expiration: int = Field(
        default=3600,
        ge=60,
        le=86400 * 365,
        description="JWT expiration time in seconds (1 min to 1 year)"
    )
    
    @validator("secret_key", always=True)
    def validate_secret_key_for_production(cls, v, values):
        """Ensure SECRET_KEY is set in production."""
        if values.get("app_env") == AppEnvironment.PRODUCTION and not v:
            raise ValueError("SECRET_KEY is required in production environment")
        return v
    
    class Config:
        use_enum_values = False


class DatabaseConfig(BaseModel):
    """Database configuration."""
    
    provider: DBProvider = Field(
        default=DBProvider.SQLITE,
        description="Database provider type"
    )
    connection_string: Optional[str] = Field(
        default=None,
        description="Database connection string (loaded from env, never hardcoded)"
    )
    pool_size: int = Field(default=10, ge=1, le=100, description="Connection pool size")
    
    @validator("connection_string", always=True)
    def validate_connection_string(cls, v, values):
        """Validate connection string for non-SQLite databases."""
        provider = values.get("provider")
        if provider != DBProvider.SQLITE and not v:
            raise ValueError(
                f"connection_string is required for {provider} provider. "
                "Load from environment, never hardcode."
            )
        return v
    
    class Config:
        use_enum_values = True


class RedTeamConfig(BaseModel):
    """Red Team simulation configuration."""
    
    max_agents: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Maximum number of concurrent agents"
    )
    simulation_timeout: int = Field(
        default=300,
        ge=30,
        le=3600,
        description="Simulation timeout in seconds (30s to 1h)"
    )
    simulation_depth: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Attack chain depth limit"
    )
    enable_autonomous_mode: bool = Field(
        default=True,
        description="Enable autonomous agent decision making"
    )
    
    class Config:
        use_enum_values = False


class ModelConfig(BaseModel):
    """AI/ML model configuration."""
    
    provider: ModelProvider = Field(
        default=ModelProvider.LOCAL,
        description="LLM provider"
    )
    model_name: str = Field(
        default="phi-4-reasoning",
        description="Model name or identifier"
    )
    temperature: float = Field(
        default=0.3,
        ge=0.0,
        le=2.0,
        description="Model temperature for creativity (0.0 to 2.0)"
    )
    max_tokens: int = Field(
        default=2048,
        ge=128,
        le=32768,
        description="Maximum tokens in response"
    )
    
    # Provider-specific credentials (loaded from env only)
    azure_openai_api_key: Optional[str] = Field(
        default=None,
        description="Azure OpenAI API key (from env)"
    )
    azure_openai_endpoint: Optional[str] = Field(
        default=None,
        description="Azure OpenAI endpoint (from env)"
    )
    azure_openai_deployment_id: Optional[str] = Field(
        default=None,
        description="Azure OpenAI deployment ID (from env)"
    )
    
    @validator("azure_openai_api_key", always=True)
    def validate_azure_credentials(cls, v, values):
        """Ensure Azure credentials are set when using Azure provider."""
        provider = values.get("provider")
        if provider == ModelProvider.MICROSOFT and not v:
            raise ValueError(
                "azure_openai_api_key is required when provider=microsoft. "
                "Set via AZURE_OPENAI_API_KEY environment variable."
            )
        return v
    
    class Config:
        use_enum_values = True


class ThreatIntelConfig(BaseModel):
    """Threat intelligence configuration."""
    
    enable_threat_feeds: bool = Field(
        default=True,
        description="Enable external threat feeds"
    )
    mitre_attack_version: int = Field(
        default=14,
        ge=1,
        description="MITRE ATT&CK framework version"
    )
    
    class Config:
        use_enum_values = False


class APIConfig(BaseModel):
    """REST API configuration."""
    
    host: str = Field(
        default="0.0.0.0",
        description="API host to bind to"
    )
    port: int = Field(
        default=8000,
        ge=1024,
        le=65535,
        description="API port"
    )
    reload: bool = Field(
        default=False,
        description="Auto-reload on code changes (dev only)"
    )
    
    class Config:
        use_enum_values = False


class CLIConfig(BaseModel):
    """Command-line interface configuration."""
    
    interactive: bool = Field(
        default=True,
        description="Enable interactive mode"
    )
    enable_batch_execution: bool = Field(
        default=True,
        description="Enable batch execution from files"
    )
    
    class Config:
        use_enum_values = False


class ReportConfig(BaseModel):
    """Report generation configuration."""
    
    format: str = Field(
        default="json",
        description="Report output format (json, html, yaml)"
    )
    output_dir: str = Field(
        default="aapp-mart/logs/attack-path",
        description="Directory for output reports"
    )
    include_metadata: bool = Field(
        default=True,
        description="Include contextual metadata in reports"
    )
    
    @validator("format")
    def validate_report_format(cls, v):
        """Validate report format."""
        valid_formats = ["json", "html", "yaml"]
        if v not in valid_formats:
            raise ValueError(f"Report format must be one of {valid_formats}, got {v}")
        return v
    
    class Config:
        use_enum_values = False


class ExperimentalConfig(BaseModel):
    """Experimental features configuration."""
    
    enable_self_learning: bool = Field(
        default=False,
        description="Enable self-learning mode"
    )
    enable_attack_simulation: bool = Field(
        default=True,
        description="Enable attack simulation engine"
    )
    enable_defense_mode: bool = Field(
        default=False,
        description="Enable defense/detection mode"
    )
    
    class Config:
        use_enum_values = False


# ============================================================================
# Main Configuration Class
# ============================================================================

class Config(BaseModel):
    """
    Main configuration class with strict schema validation.
    Combines all configuration sections.
    """
    
    app: AppConfig = Field(default_factory=AppConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    red_team: RedTeamConfig = Field(default_factory=RedTeamConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    threat_intel: ThreatIntelConfig = Field(default_factory=ThreatIntelConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    cli: CLIConfig = Field(default_factory=CLIConfig)
    report: ReportConfig = Field(default_factory=ReportConfig)
    experimental: ExperimentalConfig = Field(default_factory=ExperimentalConfig)
    
    @root_validator(pre=False)
    def validate_environment_consistency(cls, values):
        """Validate consistency across configuration sections."""
        app_config = values.get("app")
        security_config = values.get("security")
        
        # Add app_env to security config for validation context
        if app_config and security_config:
            security_config.app_env = app_config.app_env
        
        return values
    
    class Config:
        use_enum_values = False
    
    def to_dict(self, **kwargs) -> Dict[str, Any]:
        """Convert config to dictionary (for logging/debugging)."""
        return asdict(self)


# ============================================================================
# Configuration Loader with Fail-Fast Behavior
# ============================================================================

class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    pass


class ConfigLoader:
    """
    Loads and validates configuration from environment variables.
    Implements fail-fast behavior for invalid configurations.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize config loader.
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger("aapp_mart.config")
        self.config: Optional[Config] = None
    
    def load(self, fail_fast: bool = True) -> Config:
        """
        Load configuration from environment variables.
        
        Args:
            fail_fast: If True, raise exception on validation error (production mode)
        
        Returns:
            Config instance
        
        Raises:
            ConfigurationError: If configuration is invalid and fail_fast=True
        """
        try:
            self.logger.info("Loading configuration from environment variables")
            
            # Load each configuration section from environment
            app_config = self._load_app_config()
            security_config = self._load_security_config(app_config)
            database_config = self._load_database_config()
            red_team_config = self._load_red_team_config()
            model_config = self._load_model_config()
            threat_intel_config = self._load_threat_intel_config()
            api_config = self._load_api_config()
            cli_config = self._load_cli_config()
            report_config = self._load_report_config()
            experimental_config = self._load_experimental_config()
            
            # Combine into main config
            self.config = Config(
                app=app_config,
                security=security_config,
                database=database_config,
                red_team=red_team_config,
                model=model_config,
                threat_intel=threat_intel_config,
                api=api_config,
                cli=cli_config,
                report=report_config,
                experimental=experimental_config
            )
            
            self.logger.info("Configuration loaded successfully")
            self._log_config_summary()
            return self.config
            
        except ValidationError as e:
            error_msg = self._format_validation_errors(e)
            self.logger.error(f"Configuration validation failed:\n{error_msg}")
            
            if fail_fast:
                raise ConfigurationError(error_msg)
            else:
                self.logger.warning("Continuing with partial configuration")
                raise
        
        except Exception as e:
            error_msg = f"Failed to load configuration: {str(e)}"
            self.logger.error(error_msg)
            
            if fail_fast:
                raise ConfigurationError(error_msg)
            else:
                raise
    
    def _load_app_config(self) -> AppConfig:
        """Load application configuration from environment."""
        return AppConfig(
            app_name=os.getenv("APP_NAME", "AAPP-MART"),
            app_env=os.getenv("APP_ENV", "development"),
            debug=self._parse_bool(os.getenv("DEBUG", "false")),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper()
        )
    
    def _load_security_config(self, app_config: AppConfig) -> SecurityConfig:
        """Load security configuration from environment."""
        return SecurityConfig(
            app_env=app_config.app_env,
            secret_key=os.getenv("SECRET_KEY"),
            jwt_secret=os.getenv("JWT_SECRET"),
            jwt_expiration=self._parse_int(os.getenv("JWT_EXPIRATION", "3600"))
        )
    
    def _load_database_config(self) -> DatabaseConfig:
        """Load database configuration from environment."""
        return DatabaseConfig(
            provider=os.getenv("DB_PROVIDER", "sqlite"),
            connection_string=os.getenv("DB_CONNECTION_STRING"),
            pool_size=self._parse_int(os.getenv("DB_POOL_SIZE", "10"))
        )
    
    def _load_red_team_config(self) -> RedTeamConfig:
        """Load red team configuration from environment."""
        return RedTeamConfig(
            max_agents=self._parse_int(os.getenv("MAX_AGENTS", "5")),
            simulation_timeout=self._parse_int(os.getenv("SIMULATION_TIMEOUT", "300")),
            simulation_depth=self._parse_int(os.getenv("SIMULATION_DEPTH", "10")),
            enable_autonomous_mode=self._parse_bool(os.getenv("ENABLE_AUTONOMOUS_MODE", "true"))
        )
    
    def _load_model_config(self) -> ModelConfig:
        """Load model configuration from environment."""
        return ModelConfig(
            provider=os.getenv("MODEL_PROVIDER", "local"),
            model_name=os.getenv("MODEL_NAME", "phi-4-reasoning"),
            temperature=self._parse_float(os.getenv("MODEL_TEMPERATURE", "0.3")),
            max_tokens=self._parse_int(os.getenv("MODEL_MAX_TOKENS", "2048")),
            azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_openai_deployment_id=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")
        )
    
    def _load_threat_intel_config(self) -> ThreatIntelConfig:
        """Load threat intelligence configuration from environment."""
        return ThreatIntelConfig(
            enable_threat_feeds=self._parse_bool(os.getenv("ENABLE_THREAT_FEEDS", "true")),
            mitre_attack_version=self._parse_int(os.getenv("MITRE_ATTACK_VERSION", "14"))
        )
    
    def _load_api_config(self) -> APIConfig:
        """Load API configuration from environment."""
        return APIConfig(
            host=os.getenv("HOST", "0.0.0.0"),
            port=self._parse_int(os.getenv("PORT", "8000")),
            reload=self._parse_bool(os.getenv("API_RELOAD", "false"))
        )
    
    def _load_cli_config(self) -> CLIConfig:
        """Load CLI configuration from environment."""
        return CLIConfig(
            interactive=self._parse_bool(os.getenv("CLI_INTERACTIVE", "true")),
            enable_batch_execution=self._parse_bool(os.getenv("ENABLE_BATCH_EXECUTION", "true"))
        )
    
    def _load_report_config(self) -> ReportConfig:
        """Load report configuration from environment."""
        return ReportConfig(
            format=os.getenv("REPORT_FORMAT", "json"),
            output_dir=os.getenv("REPORT_OUTPUT_DIR", "aapp-mart/logs/attack-path"),
            include_metadata=self._parse_bool(os.getenv("INCLUDE_METADATA", "true"))
        )
    
    def _load_experimental_config(self) -> ExperimentalConfig:
        """Load experimental features configuration from environment."""
        return ExperimentalConfig(
            enable_self_learning=self._parse_bool(os.getenv("ENABLE_SELF_LEARNING", "false")),
            enable_attack_simulation=self._parse_bool(os.getenv("ENABLE_ATTACK_SIMULATION", "true")),
            enable_defense_mode=self._parse_bool(os.getenv("ENABLE_DEFENSE_MODE", "false"))
        )
    
    @staticmethod
    def _parse_bool(value: str) -> bool:
        """Parse boolean from string."""
        return value.lower() in ("true", "1", "yes", "on")
    
    @staticmethod
    def _parse_int(value: str) -> int:
        """Parse integer from string."""
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Cannot parse '{value}' as integer")
    
    @staticmethod
    def _parse_float(value: str) -> float:
        """Parse float from string."""
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Cannot parse '{value}' as float")
    
    def _format_validation_errors(self, validation_error: ValidationError) -> str:
        """Format Pydantic validation errors for logging."""
        errors = validation_error.errors()
        formatted = []
        for error in errors:
            loc = ".".join(str(l) for l in error["loc"])
            msg = error["msg"]
            formatted.append(f"  - {loc}: {msg}")
        return "\n".join(formatted)
    
    def _log_config_summary(self) -> None:
        """Log configuration summary (without sensitive data)."""
        if not self.config:
            return
        
        summary = {
            "environment": self.config.app.app_env.value,
            "debug_mode": self.config.app.debug,
            "log_level": self.config.app.log_level.value,
            "max_agents": self.config.red_team.max_agents,
            "simulation_timeout": self.config.red_team.simulation_timeout,
            "api_host": self.config.api.host,
            "api_port": self.config.api.port,
            "report_format": self.config.report.format,
            "threat_feeds": self.config.threat_intel.enable_threat_feeds
        }
        
        self.logger.info(f"Configuration summary: {summary}")


# ============================================================================
# Global Configuration Instance
# ============================================================================

_global_config: Optional[Config] = None
_config_loader: Optional[ConfigLoader] = None


def get_config(logger: Optional[logging.Logger] = None) -> Config:
    """
    Get global configuration instance.
    Loads configuration on first call, returns cached instance on subsequent calls.
    
    Args:
        logger: Optional logger instance
    
    Returns:
        Config instance
    
    Raises:
        ConfigurationError: If configuration loading fails
    """
    global _global_config, _config_loader
    
    if _global_config is None:
        _config_loader = ConfigLoader(logger)
        _global_config = _config_loader.load(fail_fast=True)
    
    return _global_config


def reset_config() -> None:
    """Reset global configuration (useful for testing)."""
    global _global_config, _config_loader
    _global_config = None
    _config_loader = None


# ============================================================================
# Module Initialization
# ============================================================================

if __name__ == "__main__":
    # Test configuration loading
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    try:
        config = get_config()
        print("\nConfiguration loaded successfully!\n")
        print(f"Environment: {config.app.app_env.value}")
        print(f"Debug: {config.app.debug}")
        print(f"Log Level: {config.app.log_level.value}")
        print(f"API: {config.api.host}:{config.api.port}")
        print(f"Max Agents: {config.red_team.max_agents}")
        print(f"Simulation Timeout: {config.red_team.simulation_timeout}s")
        
    except ConfigurationError as e:
        print(f"\nConfiguration Error:\n{e}")
        sys.exit(1)
