"""
Terminal Tool.
A narrow wrapper around subprocess for running shell commands safely
within a specific working directory. Used by the Git Agent now; future
agents (e.g. an enhanced Debugger) can reuse this to run generated code.

This tool has no knowledge of agents or LLMs — it only executes and
reports back stdout/stderr/exit code.
"""
import subprocess


class TerminalToolError(Exception):
    """Raised when a command fails to execute at all (not just non-zero exit)."""


def run_command(command: list[str], cwd: str, timeout: int = 30) -> dict:
    """
    Runs a command as a list of args (never a raw shell string, to avoid
    shell injection) inside `cwd`. Returns exit code, stdout, and stderr.
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except FileNotFoundError as e:
        raise TerminalToolError(f"Command not found: {command[0]}") from e
    except subprocess.TimeoutExpired as e:
        raise TerminalToolError(f"Command timed out after {timeout}s: {command}") from e