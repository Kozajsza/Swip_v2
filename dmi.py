from dmidecode import DMIDecode
import subprocess

# create parsing instance by passing dmidecode output
dmi = DMIDecode()

# some of the pre-defined queries
print('Manufacturer:\t', dmi.manufacturer())
print('Model:\t\t', dmi.model())
print('Firmware:\t', dmi.firmware())
print('Serial number:\t', dmi.serial_number())
print('Processor type:\t', dmi.cpu_type())
print('Number of CPUs:\t', dmi.cpu_num())
print('Cores count:\t', dmi.total_enabled_cores())
print('Total RAM:\t{} GB'.format(dmi.total_ram()))