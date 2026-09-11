from app.core.wasm_sandbox import wasm_engine


def test_wasm_sandbox_list_installed_plugins():
    plugins = wasm_engine.list_installed_wasm_plugins()
    assert isinstance(plugins, list)
    assert len(plugins) >= 1
    assert plugins[0].get("sandbox_isolation") == "STRICT_WASI"


def test_wasm_sandbox_plugin_execution():
    res = wasm_engine.execute_wasm_plugin("wasm-media-indexer", {"file": "sample.mp4", "mode": "fast"})
    assert res is not None
    assert res.get("status") == "SUCCESS"
    assert "execution_time_ms" in res.get("output", {})
