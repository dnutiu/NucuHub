import subprocess


def test_black():
    result = subprocess.run(
        ["black", "--check", "--diff", "--exclude=venv", "."], timeout=5,
    )

    assert result.returncode == 0, result.stdout


def test_isort():
    result = subprocess.run(
        ["isort", "--check-only", "--diff", "--skip=venv"], timeout=5,
    )

    assert result.returncode == 0, result.stdout
