import collectd
from transmissionrpc import Client

USERNAME = None
PASSWORD = None


def configer(conf):
    """Receive configuration block"""
    global USERNAME, PASSWORD
    for node in conf.children:
        if node.key == 'Username':
            USERNAME = node.values[0]
        elif node.key == 'Password':
            PASSWORD = node.values[0]


def dispatch_value(val_type, value):
    """Dispatch a value"""
    val = collectd.Values(plugin='transmission')
    val.type = val_type
    val.values = value if type(value) == list else [value]
    val.dispatch()


def reader():
    """Read data and dispatch"""
    client = Client(user=USERNAME, password=PASSWORD)
    stats = client.session_stats()

    dispatch_value('transmission_speed', [
        stats.cumulative_stats['downloadedBytes'],
        stats.cumulative_stats['uploadedBytes']
    ])

    dispatch_value('transmission_count', [
        stats.activeTorrentCount,
        stats.pausedTorrentCount
    ])

# register callbacks
collectd.register_config(configer)
collectd.register_read(reader)
