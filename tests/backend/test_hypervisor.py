import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.hardware.hypervisor import hypervisor_hal

client = TestClient(app)

def test_hypervisor_hal_status():
    status = hypervisor_hal.get_hypervisor_status()
    assert status["type_1_hypervisor"] is True
    assert status["active_vms"] >= 1
    assert status["san_pools_count"] >= 1

def test_hypervisor_vm_lifecycle():
    # 1. Create VM
    new_vm = hypervisor_hal.create_vm(name="Test-VM-1", vm_type="kvm", vcpus=2, ram_mb=2048)
    assert new_vm["name"] == "Test-VM-1"
    vm_id = new_vm["vm_id"]

    # 2. Control VM state
    controlled = hypervisor_hal.control_vm(vm_id, "stop")
    assert controlled["status"] == "STOPPED"

    controlled = hypervisor_hal.control_vm(vm_id, "start")
    assert controlled["status"] == "RUNNING"

    # 3. Delete VM
    deleted = hypervisor_hal.delete_vm(vm_id)
    assert deleted is True

def test_hypervisor_pcie_and_san():
    devices = hypervisor_hal.list_pcie_devices()
    assert len(devices) > 0
    assert any(d["type"] == "GPU" for d in devices)

    pools = hypervisor_hal.get_san_pools()
    assert len(pools) > 0
    
    new_pool = hypervisor_hal.create_san_pool("Test-SAN-Pool", raid_level="RAID-Z1")
    assert new_pool["name"] == "Test-SAN-Pool"

def test_hypervisor_api_endpoints():
    # GET status
    r = client.get("/api/v1/v4/hypervisor/status")
    assert r.status_code == 200
    assert r.json()["type_1_hypervisor"] is True

    # GET vms
    r = client.get("/api/v1/v4/hypervisor/vms")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # POST vm
    payload = {"name": "API-Test-VM", "vm_type": "lxc", "vcpus": 1, "ram_mb": 512, "disk_gb": 10}
    r = client.post("/api/v1/v4/hypervisor/vms", json=payload)
    assert r.status_code == 200
    created = r.json()
    vm_id = created["vm_id"]

    # POST control
    r = client.post(f"/api/v1/v4/hypervisor/vms/{vm_id}/control", json={"action": "pause"})
    assert r.status_code == 200
    assert r.json()["status"] == "PAUSED"

    # DELETE vm
    r = client.delete(f"/api/v1/v4/hypervisor/vms/{vm_id}")
    assert r.status_code == 200

    # GET pcie-devices
    r = client.get("/api/v1/v4/hypervisor/pcie-devices")
    assert r.status_code == 200

    # GET san-pools
    r = client.get("/api/v1/v4/hypervisor/san-pools")
    assert r.status_code == 200
