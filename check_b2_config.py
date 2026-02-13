"""
Quick diagnostic script to check B2 configuration on Render
Run this via Render Shell to verify B2 settings
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmtool.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import storages

print("=" * 60)
print("B2 STORAGE CONFIGURATION CHECK")
print("=" * 60)

# Check environment variables
print("\n1. Environment Variables:")
print(f"   USE_B2_STORAGE: {os.getenv('USE_B2_STORAGE')}")
print(f"   B2_APPLICATION_KEY_ID: {'SET' if os.getenv('B2_APPLICATION_KEY_ID') else 'NOT SET'}")
print(f"   B2_APPLICATION_KEY: {'SET' if os.getenv('B2_APPLICATION_KEY') else 'NOT SET'}")
print(f"   B2_BUCKET_NAME: {os.getenv('B2_BUCKET_NAME', 'NOT SET')}")
print(f"   B2_ENDPOINT_URL: {os.getenv('B2_ENDPOINT_URL', 'NOT SET')}")
print(f"   B2_REGION: {os.getenv('B2_REGION', 'NOT SET')}")

# Check Django settings
print("\n2. Django Settings:")
print(f"   USE_B2_STORAGE: {settings.USE_B2_STORAGE}")
if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
    print(f"   AWS_ACCESS_KEY_ID: {'SET' if settings.AWS_ACCESS_KEY_ID else 'NOT SET'}")
    print(f"   AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
    print(f"   AWS_S3_ENDPOINT_URL: {settings.AWS_S3_ENDPOINT_URL}")

# Check storage backend
print("\n3. Storage Backend:")
storage = storages["default"]
print(f"   Type: {type(storage).__name__}")
print(f"   Module: {type(storage).__module__}")

# Try to test connection
if settings.USE_B2_STORAGE:
    print("\n4. Testing B2 Connection:")
    try:
        from django.core.files.base import ContentFile
        test_content = ContentFile(b"Test upload from Render")
        test_path = storage.save("test_render_upload.txt", test_content)
        print(f"   ✅ Upload successful: {test_path}")
        
        # Generate URL
        url = storage.url(test_path)
        print(f"   ✅ URL generated: {url[:80]}...")
        
        # Clean up
        storage.delete(test_path)
        print(f"   ✅ Cleanup successful")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
else:
    print("\n4. B2 Storage is DISABLED (using local filesystem)")

print("\n" + "=" * 60)
