import collectd
import psutil

CPU_COUNT = psutil.NUM_CPUS

def configer(conf):
    pass


def dispatch_value(val_type, value):
    """Dispatch a value"""
    val = collectd.Values(plugin='cpu')
    val.type = 'cpu'
    val.type_instance = val_type
    val.values = [value]
    val.dispatch()


def reader():
    """Read data and dispatch"""
    times = psutil.cpu_times()

    for val in ['user', 'nice', 'system', 'iowait', 'irq', 'softirq']:
        dispatch_value(val, getattr(times, val) * 100 / CPU_COUNT)

# register callbacks
collectd.register_config(configer)
collectd.register_read(reader)
