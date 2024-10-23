from swsscommon.swsscommon import SonicV2Connector
from sonic_py_common import device_info
import click


SUPPORT_PLATFORM = [
    'x86_64-accton_as9716_32d-r0'
]

def get_i2c_isolation_list_dict ():
    """
    Get the I2C isolation list from STATE_DB
    """
    sonic_db = SonicV2Connector(host='127.0.0.1')
    sonic_db.connect(sonic_db.STATE_DB)
    i2c_isolation_list_dict = {}

    for table_name in sonic_db.keys(sonic_db.STATE_DB, "I2C_ISOLATION_LIST*"):
        _, region_id, i2c_address = table_name.split("|")
        device_name = sonic_db.get(sonic_db.STATE_DB, table_name, "device_name")
        if region_id not in i2c_isolation_list_dict:
            i2c_isolation_list_dict[region_id] = []
        i2c_isolation_list_dict[region_id].append((device_name, i2c_address))

    return i2c_isolation_list_dict


@click.command("i2c-isolation-list")
def i2c_isolation_list():
    """ Show I2C isolation list """

    i2c_isolation_list_dict = get_i2c_isolation_list_dict()

    if not (i2c_isolation_list_dict):
        # No isolated I2C device record in the STATE_DB
        click.echo ("I2C isolation list is empty.")
        return

    click.echo("I2C Isolation List")
    for region_id, devices_list in i2c_isolation_list_dict.items():
        click.echo ("----------------------------")
        click.echo ("Region: {}".format(region_id))
        click.echo ("Devices:")
        for device_name, device_i2c_address in devices_list:
            click.echo ("  {} (address: {})".format(device_name, device_i2c_address))


def register(cli):
    if device_info.get_platform() in SUPPORT_PLATFORM:
        cli.commands['platform'].add_command(i2c_isolation_list)


if __name__ == '__main__':
    i2c_isolation_list()