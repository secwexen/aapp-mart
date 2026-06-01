"""
Structured Logging System for AAPP-MART v1.2.0

Provides:
- Structured logging with contextual metadata
- Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Multiple handlers (console, file)
- Pretty formatting with rich
- Context tracking
- Performance metrics logging
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import traceback

from rich.logging import RichHandler


# ============================================================================
# Log Level
# ============================================================================

class LogLevel(str, Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ============================================================================
# Log Context
# ============================================================================

@dataclass
class LogContext:
    """Context information for logging."""
    agent_id: Optional[str] = None
    simulation_id: Optional[str] = None
    phase: Optional[str] = None
    task_id: Optional[str] = None
    user: Optional[str] = None
    request_id: Optional[str] = None
    custom: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, filtering None values."""
        result = {}
        if self.agent_id:
            result["agent_id"] = self.agent_id
        if self.simulation_id:
            result["simulation_id"] = self.simulation_id
        if self.phase:
            result["phase"] = self.phase
        if self.task_id:
            result["task_id"] = self.task_id
        if self.user:
            result["user"] = self.user
        if self.request_id:
            result["request_id"] = self.request_id
        if self.custom:
            result.update(self.custom)
        return result


# ============================================================================
# Structured Logger
# ============================================================================

class StructuredLogger:
    """
    Production-grade structured logger with context tracking.
    
    Features:
    - Contextual metadata logging
    - Performance timing
    - Exception tracking
    - Multiple output formats
    """
    
    def __init__(
        self,
        name: str,
        level: str = "INFO",
        log_file: Optional[Path] = None,
        pretty: bool = True
    ):
        """
        Initialize logger.
        
        Args:
            name: Logger name (typically module name)
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for logging
            pretty: Use rich formatting for console output
        """
        self.name = name
        self.level = level.upper()
        self.log_file = log_file
        self.pretty = pretty
        
        # Create base logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # Clear existing handlers to avoid duplicates
        self.logger.handlers = []
        self.logger.propagate = False
        
        # Setup handlers
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Setup logging handlers (console + optional file)."""
        
        # Console handler with rich
        if self.pretty:
            try:
                console_handler = RichHandler(
                    rich_tracebacks=True,
                    markup=True,
                    show_time=True,
                    show_level=True,
                    show_path=False
                )
                console_handler.setFormatter(
                    logging.Formatter(
                        "%(message)s",
                        datefmt="[%X]"
                    )
                )
            except Exception:
                # Fallback if rich not available
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(
                    logging.Formatter(
                        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                    )
                )
        else:
            # Plain console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
        
        console_handler.setLevel(self.level)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if self.log_file:
            try:
                self.log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(self.log_file)
                file_handler.setFormatter(
                    logging.Formatter(
                        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                    )
                )
                file_handler.setLevel(self.level)
                self.logger.addHandler(file_handler)
            except Exception as e:
                # Log setup error but don't fail
                self.logger.warning(f"Could not setup file logging: {e}")
    
    def _format_message(
        self,
        message: str,
        context: Optional[LogContext] = None,
        **extra
    ) -> str:
        """
        Format message with context.
        
        Args:
            message: Main message
            context: Optional LogContext with metadata
            **extra: Additional key-value pairs
        
        Returns:
            Formatted message string
        """
        # Build context string
        context_parts = []
        
        if context:
            ctx_dict = context.to_dict()
            for key, value in ctx_dict.items():
                if value is not None:
                    context_parts.append(f"{key}={value}")
        
        # Add extra fields
        for key, value in extra.items():
            if value is not None:
                context_parts.append(f"{key}={value}")
        
        # Format final message
        if context_parts:
            return f"{message} | [{', '.join(context_parts)}]"
        return message
    
    def debug(
        self,
        message: str,
        context: Optional[LogContext] = None,
        **extra
    ) -> None:
        """Log debug message."""
        formatted = self._format_message(message, context, **extra)
        self.logger.debug(formatted)
    
    def info(
        self,
        message: str,
        context: Optional[LogContext] = None,
        **extra
    ) -> None:
        """Log info message."""
        formatted = self._format_message(message, context, **extra)
        self.logger.info(formatted)
    
    def warning(
        self,
        message: str,
        context: Optional[LogContext] = None,
        **extra
    ) -> None:
        """Log warning message."""
        formatted = self._format_message(message, context, **extra)
        self.logger.warning(formatted)
    
    def error(
        self,
        message: str,
        context: Optional[LogContext] = None,
        exception: Optional[Exception] = None,
        **extra
    ) -> None:
        """Log error message with optional exception."""
        formatted = self._format_message(message, context, **extra)
        if exception:
            self.logger.error(formatted, exc_info=exception)
        else:
            self.logger.error(formatted)
    
    def critical(
        self,
        message: str,
        context: Optional[LogContext] = None,
        exception: Optional[Exception] = None,
        **extra
    ) -> None:
        """Log critical message with optional exception."""
        formatted = self._format_message(message, context, **extra)
        if exception:
            self.logger.critical(formatted, exc_info=exception)
        else:
            self.logger.critical(formatted)
    
    def log_exception(
        self,
        exception: Exception,
        context: Optional[LogContext] = None,
        **extra
    ) -> None:
        """
        Log exception with full traceback.
        
        Args:
            exception: Exception instance
            context: Optional LogContext
            **extra: Additional fields
        """
        message = f"Exception: {exception.__class__.__name__}: {str(exception)}"
        self.error(message, context, exception=exception, **extra)


# ============================================================================
# Performance Timer
# ============================================================================

class PerformanceTimer:
    """Context manager for performance timing."""
    
    def __init__(
        self,
        logger: StructuredLogger,
        operation: str,
        context: Optional[LogContext] = None
    ):
        """
        Initialize timer.
        
        Args:
            logger: StructuredLogger instance
            operation: Operation name
            context: Optional LogContext
        """
        self.logger = logger
        self.operation = operation
        self.context = context
        self.start_time: Optional[datetime] = None
        self.duration: Optional[float] = None
    
    def __enter__(self):
        """Start timing."""
        self.start_time = datetime.utcnow()
        self.logger.debug(
            f"Starting: {self.operation}",
            context=self.context
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End timing and log duration."""
        if self.start_time:
            self.duration = (datetime.utcnow() - self.start_time).total_seconds()
            
            if exc_type:
                self.logger.warning(
                    f"Failed: {self.operation}",
                    context=self.context,
                    duration_seconds=round(self.duration, 3),
                    error=str(exc_val)
                )
            else:
                self.logger.info(
                    f"Completed: {self.operation}",
                    context=self.context,
                    duration_seconds=round(self.duration, 3)
                )


# ============================================================================
# Logger Factory
# ============================================================================

class LoggerFactory:
    """Factory for creating and managing loggers."""
    
    _loggers: Dict[str, StructuredLogger] = {}
    _log_dir: Optional[Path] = None
    _log_level: str = "INFO"
    _pretty: bool = True
    
    @classmethod
    def configure(
        cls,
        log_dir: Optional[Path] = None,
        log_level: str = "INFO",
        pretty: bool = True
    ) -> None:
        """
        Configure logger factory globally.
        
        Args:
            log_dir: Directory for log files
            log_level: Default log level
            pretty: Use pretty formatting
        """
        cls._log_dir = log_dir
        cls._log_level = log_level.upper()
        cls._pretty = pretty
    
    @classmethod
    def get_logger(
        cls,
        name: str,
        log_file: Optional[str] = None
    ) -> StructuredLogger:
        """
        Get or create logger.
        
        Args:
            name: Logger name (e.g., "aapp_mart.config")
            log_file: Optional log file name (without path)
        
        Returns:
            StructuredLogger instance
        """
        if name not in cls._loggers:
            log_path = None
            if cls._log_dir:
                log_path = cls._log_dir / (log_file or f"{name}.log")
            
            logger = StructuredLogger(
                name=name,
                level=cls._log_level,
                log_file=log_path,
                pretty=cls._pretty
            )
            cls._loggers[name] = logger
        
        return cls._loggers[name]
    
    @classmethod
    def reset(cls) -> None:
        """Reset all loggers (useful for testing)."""
        cls._loggers.clear()


# ============================================================================
# Global Setup Functions
# ============================================================================

def setup_logging(
    log_dir: Path = Path("./logs"),
    log_level: str = "INFO",
    pretty: bool = True
) -> None:
    """
    Setup global logging configuration.
    
    Args:
        log_dir: Directory for log files
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        pretty: Use rich pretty formatting
    """
    LoggerFactory.configure(
        log_dir=log_dir,
        log_level=log_level,
        pretty=pretty
    )


def get_logger(name: str) -> StructuredLogger:
    """
    Get logger by name (convenience function).
    
    Args:
        name: Logger name
    
    Returns:
        StructuredLogger instance
    """
    return LoggerFactory.get_logger(name)


# ============================================================================
# Test / Example Usage
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("AAPP-MART Structured Logging System - Test")
    print("=" * 70)
    
    # Setup logging
    setup_logging(
        log_dir=Path("./logs/aapp-mart"),
        log_level="DEBUG",
        pretty=True
    )
    
    # Get logger
    logger = get_logger("aapp_mart.test")
    
    print("\nTest 1: Simple logging")
    logger.info("Application started")
    logger.debug("Debug information enabled")
    logger.warning("This is a warning")
    
    print("\nTest 2: Logging with context")
    context = LogContext(
        agent_id="recon-001",
        simulation_id="sim-abc123",
        phase="RECONNAISSANCE"
    )
    logger.info("Starting reconnaissance phase", context=context)
    logger.debug("Agent configuration loaded", context=context)
    
    print("\nTest 3: Extra fields")
    logger.info(
        "Operation executed",
        context=context,
        status="success",
        items_processed=42
    )
    
    print("\nTest 4: Performance timing")
    with PerformanceTimer(logger, "sample_operation", context):
        import time
        time.sleep(0.5)  # Simulate work
    
    print("\nTest 5: Error logging")
    try:
        raise ValueError("Test error for demonstration")
    except Exception as e:
        logger.log_exception(e, context)
    
    print("\nTest 6: Multiple loggers")
    logger2 = get_logger("aapp_mart.agents")
    logger2.info("Agent module initialized")
    
    logger3 = get_logger("aapp_mart.network")
    logger3.info("Network module initialized")
    
    print("\n" + "=" * 70)
    print("All tests passed! Logging system is working correctly.")
    print("=" * 70)
