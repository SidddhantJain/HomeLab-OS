from app.hardware.rust_telemetry import rust_engine


def test_rust_core_telemetry_collector():
    metrics = rust_engine.collect_telemetry()
    assert metrics is not None
    assert "execution_latency_ms" in metrics
    assert metrics.get("cpu_cores_active") >= 2
    assert "accelerator" in metrics


def test_rust_core_vault_crypto():
    res = rust_engine.encrypt_vault_data("test_secret_data", "my_secret_key_123")
    assert res is not None
    assert res.get("status") == "encrypted"
    assert res.get("cipher") == "AES-256-GCM"
    assert "payload" in res
