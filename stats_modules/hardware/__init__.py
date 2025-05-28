from .cpu_monitor import init as _cpu_init , update as _cpu_update
from .ram_monitor import init as _ram_init , update as _ram_update
from .nvme_monitor import init as _nvme_init , update as _nvme_update
from .rp1_monitor import init as _rp1_init , update as _rp1_update
from .pmic_monitor import init as _pmic_init , update as _pmic_update

__all__ = ["init_modules","hardware_modules"]

def init_modules(device_size):
    _cpu_init(device_size)
    _ram_init(device_size)
    _nvme_init(device_size)
    _rp1_init(device_size)
    _pmic_init(device_size)

hardware_modules = {
    "cpu": {"update":_cpu_update},
    "ram": {"update":_ram_update},
    "nvme": {"update":_nvme_update},
    "rp1": {"update":_rp1_update},
    "pmic": {"update":_pmic_update},
}
