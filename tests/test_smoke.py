def test_validate_toolkit_import():
    """Smoke test: ensure validate_toolkit imports and TOOLKIT_DIR exists."""
    import tests.validate_toolkit as vt
    assert hasattr(vt, "TOOLKIT_DIR")
    assert vt.TOOLKIT_DIR.exists()
