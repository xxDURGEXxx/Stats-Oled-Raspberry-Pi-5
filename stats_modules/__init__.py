from .home import init as _home_init , update as _home_update
from .network_monitor import init as _network_init , update as _network_update
from . import hardware_select as _hardware_select

__all__=["init_modules", "stats_modules","moduel_count"]

def init_modules(device_size):
    _home_init(device_size)
    _network_init(device_size)
    _hardware_select.init(device_size)

stats_modules=[
    {
        "name":"home",
        "update":_home_update
        } ,
    {
        "name":"hardware_select",
        "active":_hardware_select.getActive,
        "update":_hardware_select.update,
        "toggleActive":_hardware_select.toggleActive,
        "action_next":_hardware_select.action_next,
        "action_select": _hardware_select.action_select,
        "action_back":_hardware_select.action_back
        } ,
    {
        "name":"network",
        "update":_network_update
        } , 
]

moduel_count=len(stats_modules)