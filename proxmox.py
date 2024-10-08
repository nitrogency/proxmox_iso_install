from proxmoxer import ProxmoxAPI
import argparse
import time

parser = argparse.ArgumentParser(description="Sets up a Proxmox VM using an already uploaded image.")
parser.add_argument("-i", "--addr", type=str, required=True, help="Proxmox instance IP/hostname")
parser.add_argument("-u", "--user", type=str, default="root@pam", help="Proxmox user (Default - root@pam)")
parser.add_argument("-p", "--password", type=str, required=True, help="Proxmox user password")
args = parser.parse_args()

proxmox = ProxmoxAPI(args.addr, user=args.user, password=args.password, verify_ssl=False)


node = input('Node in which you want to create the VM (Default - pve): ') or 'pve'
vmid = int(input('ID you want to assign to the VM (Default - 100): ') or '100')
iso_storage = input('Storage location in which the .iso file is kept (Default - local): ') or 'local'
lvm_storage = input('Storage location in which the VM will be created (Default - local-lvm): ') or 'local-lvm'
iso_file = input('Name of the .iso file: ')
vm_name = input('Name of the VM you want to create: ')
memory = input('Memory to allocate (Default - 2048MB): ') or '2048'
cores = input('Cores to allocate (Default - 2): ') or '2'
disk_size = input('Disk size to allocate in gigabytes (Default - 32): ') or '32'

if not (iso_file.endswith(".iso")):
    iso_file = iso_file + ".iso"

proxmox.nodes(node).qemu().create(
    vmid=vmid,
    name=vm_name,
    memory=memory,
    cores=cores,
    ide2=f"{iso_storage}:iso/{iso_file},media=cdrom",
    scsi0=f"{lvm_storage}:{disk_size},format=raw", 
    ostype='l26',
)
print ("VM created successfully.")

# Pagal dokumentaciją kaip ir atitinka, tačiau kažkodėl nepaleidžia
# https://pve.proxmox.com/pve-docs/api-viewer/#/nodes/{node}/qemu/{vmid}/status/start
proxmox.nodes(node).qemu(vmid).status.start()



