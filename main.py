from drive_manager import DriveFileManager


instance = DriveFileManager(share_owner='pxuanbach1412@gmail.com')

# folder = instance.create_folder("HEHE")

folders = instance.get_folder("HEHE")

# for f in folders:
#     instance.delete(f)


