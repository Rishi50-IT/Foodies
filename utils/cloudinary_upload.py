"""Cloudinary upload wrapper — falls back gracefully if not configured."""
import os
import cloudinary
import cloudinary.uploader

_configured = False


def _configure():
    global _configured
    if _configured:
        return bool(os.getenv("CLOUDINARY_CLOUD_NAME"))
    name = os.getenv("CLOUDINARY_CLOUD_NAME")
    key = os.getenv("CLOUDINARY_API_KEY")
    secret = os.getenv("CLOUDINARY_API_SECRET")
    if not (name and key and secret):
        return False
    cloudinary.config(cloud_name=name, api_key=key, api_secret=secret, secure=True)
    _configured = True
    return True


def upload_image(file_obj, folder="foodrush"):
    """Returns a secure URL, or None if upload is unavailable."""
    if not _configure():
        return None
    try:
        res = cloudinary.uploader.upload(file_obj, folder=folder)
        return res.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None
