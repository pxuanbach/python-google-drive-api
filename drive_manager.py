from pprint import pprint

from pydrive2.drive import GoogleDrive, GoogleDriveFile
from auth import drive
from utils import read_file_content, get_local_file_metadata
from constants import QUERY_IS_FOLDER, MIMETYPE_FOLDER


class DriveFileManager:
    def __init__(
        self, 
        drive: GoogleDrive = drive, 
        parent_folder: str = 'DriveFiles', 
        share_owner: str = ''
    ) -> None:
        self.drive = drive
        self.parent_folder = parent_folder
        self.share_owner = share_owner
    
    def get_files(self):
        # Auto-iterate through all files in the root folder.
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            print('File title: %s, id: %s, mimeType: %s' % (file['title'], file['id'], file['mimeType']))
        return file_list
    
    def get_folders(self):
        folder_list = drive.ListFile({'q': QUERY_IS_FOLDER}).GetList()
        for folder in folder_list:
            print('Folder title: %s, id: %s' % (folder['title'], folder['id']))
        return folder_list
    
    def get_folder(self, name: str):
        folder_list = drive.ListFile({'q': f"name = '{name}' and mimeType = '{MIMETYPE_FOLDER}'"}).GetList()
        if len(folder_list) > 0:
            print('Folder title: %s, id: %s' % (folder_list[0]['title'], folder_list[0]['id']))
            return folder_list[0]
        return None
    
    def create_folder(self, folder_name: str):
        metadata = {
            'title': folder_name,
            'mimeType': MIMETYPE_FOLDER,
        }
        folder = self.drive.CreateFile(metadata)
        folder.Upload() 
        print('Folder title: %s, id: %s' % (folder['title'], folder['id']))
        return folder

    def create_file(self, file_path: str):
        # load file
        file_content = read_file_content(file_path)
        file_metadata = get_local_file_metadata(file_path)
        pprint(file_metadata)

        # Create GoogleDriveFile instance
        metadata = {
            'title': file_metadata['name'],
            'mimeType': file_metadata['mimeType'],
            'fileSize': file_metadata['size'],
        }
        file = self.drive.CreateFile(metadata)

        # Set the content of the file
        file.content = file_content

        # Upload the file to google drive
        file.Upload() 
        self.add_share_owner_permission(file)

        print('File title: %s, id: %s' % (file['title'], file['id']))
        return file

    def add_share_owner_permission(self, file: GoogleDriveFile):
        permission = file.InsertPermission(
            {
                'type': 'user',
                'value': self.share_owner,
                'emailAddress': self.share_owner,
                'role': 'writer',
            }
        )
        pprint(permission)
        return file['alternateLink']    # Display the sharable link.
    
    def get_permissions(self, file: GoogleDriveFile):
        permissions = file.GetPermissions()
        return permissions
    
    def download(self, file: GoogleDriveFile, file_name: str):
        # Initialize GoogleDriveFile instance with file id.
        # downloaded_file = drive.CreateFile({'id': file['id']})
        # downloaded_file.GetContentFile(file_name) # Download file
        pass

    def delete(self, file: GoogleDriveFile):
        print("Delete File title: %s, id: %s, mimeType: %s" % (file['title'], file['id'], file['mimeType']))
        file.Delete()
        return