import os
import uuid
from datetime import datetime
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify

@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # Set filename as a random string with UUID
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # Create a path based on the owner ID, apartment ID, current date, and checkin_profile ID
        owner_id = slugify(instance.checkin_profile.owner.id)
        apartment_id = slugify(instance.checkin_profile.apartment.id)
        date_path = datetime.now().strftime('%Y/%m/%d')
        checkin_profile_id = slugify(instance.checkin_profile.id)
        # Return the whole path to the file
        return os.path.join(self.sub_path, str(owner_id), str(apartment_id), date_path, str(checkin_profile_id), filename)

# Usage example
path_and_rename = PathAndRename("document_photos/")