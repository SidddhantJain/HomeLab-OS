import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.hardware.tariff_compiler import tariff_compiler_hal
from app.hardware.build_farm import build_farm_hal
from app.hardware.ai_self_fix import ai_self_fix_hal
from app.hardware.shamir_backup import shamir_backup_hal

client = TestClient(app)

def test_tariff_compiler_and_build_farm_hal():
    t_status = tariff_compiler_hal.get_compiler_status()
    assert "Tariff-Aware Remote Compiler" in t_status["engine"]
    assert t_status["cache_stats"]["hit_ratio_pct"] > 80.0

    tariffs = tariff_compiler_hal.get_energy_tariffs()
    assert len(tariffs) > 0

    scheduled = tariff_compiler_hal.schedule_deferred_build(name="Test-Rust-Build", language="Rust")
    assert scheduled["name"] == "Test-Rust-Build"

    b_status = build_farm_hal.get_build_farm_status()
    assert b_status["total_workers"] >= 1
    assert b_status["total_compilation_cores"] >= 8

def test_ai_self_fix_and_shamir_hal():
    analysis = ai_self_fix_hal.analyze_compiler_error(log_snippet="error: expected `;`", file_path="src/lib.rs")
    assert analysis["file_path"] == "src/lib.rs"
    assert "diff_patch" in analysis

    split = shamir_backup_hal.split_secret(secret_name="master-vault-pass", threshold=3, total_shares=5)
    assert len(split["shares"]) == 5

    recovered = shamir_backup_hal.reconstruct_secret(shares=["s1", "s2", "s3"])
    assert recovered["status"] == "RECONSTRUCTED"

def test_v3_5_api_endpoints():
    # Tariff status
    r = client.get("/api/v1/v3_5/compiler/tariff/status")
    assert r.status_code == 200

    # Build farm status
    r = client.get("/api/v1/v3_5/compiler/build-farm/status")
    assert r.status_code == 200

    # AI Self-Fix analyze
    r = client.post("/api/v1/v3_5/compiler/ai-self-fix/analyze", json={"log_snippet": "error[E0308]: mismatched types", "file_path": "src/main.rs"})
    assert r.status_code == 200
    assert "diff_patch" in r.json()

    # Spotlight Search
    r = client.get("/api/v1/v3_5/spotlight/search?q=main")
    assert r.status_code == 200
    assert r.json()["total_results"] > 0

    # Mobile IDE Layout
    r = client.get("/api/v1/v3_5/mobile-ide/keyboard-layout")
    assert r.status_code == 200
    assert "Ctrl" in r.json()["floating_row_keys"]

    # Mobile Remote Compile
    r = client.post("/api/v1/v3_5/mobile-ide/compile", json={"project_path": "d:/Siddhant/projects/App", "target_arch": "arm64-v8a"})
    assert r.status_code == 200
    assert r.json()["status"] == "BUILD_STARTED"
