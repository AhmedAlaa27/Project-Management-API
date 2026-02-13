from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage, storages
from django.core.files import File
from Users.models import User
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Migrate local avatar files to Backblaze B2'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually doing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.WARNING('\n' + '='*60))
        self.stdout.write(self.style.WARNING('📤 Avatar Migration to Backblaze B2'))
        self.stdout.write(self.style.WARNING('='*60 + '\n'))

        if dry_run:
            self.stdout.write(self.style.NOTICE('🔍 DRY RUN MODE - No files will be uploaded\n'))

        # Get B2 storage
        b2_storage = storages['default']
        
        # Check if using B2
        if 'S3' not in str(type(b2_storage)):
            self.stdout.write(self.style.ERROR('❌ B2 Storage is not configured!'))
            self.stdout.write(self.style.ERROR('   Set USE_B2_STORAGE=True in your .env file\n'))
            return

        self.stdout.write(self.style.SUCCESS(f'✅ B2 Storage Active: {type(b2_storage).__name__}\n'))

        # Get all users with avatars
        users_with_avatars = User.objects.exclude(avatar='').exclude(avatar=None)
        total_users = users_with_avatars.count()

        if total_users == 0:
            self.stdout.write(self.style.WARNING('⚠️  No users with avatars found\n'))
            return

        self.stdout.write(f'📊 Found {total_users} users with avatars\n')

        migrated = 0
        skipped = 0
        errors = 0

        for user in users_with_avatars:
            avatar_path = user.avatar.name
            
            self.stdout.write(f'\n👤 User: {user.username}')
            self.stdout.write(f'   Avatar: {avatar_path}')

            try:
                # Check if file exists locally
                local_path = user.avatar.path
                if not os.path.exists(local_path):
                    self.stdout.write(self.style.WARNING(f'   ⚠️  Local file not found: {local_path}'))
                    skipped += 1
                    continue

                # Check if already in B2
                if b2_storage.exists(avatar_path):
                    self.stdout.write(self.style.NOTICE(f'   ℹ️  Already in B2, skipping'))
                    skipped += 1
                    continue

                if dry_run:
                    self.stdout.write(self.style.NOTICE(f'   ➡️  Would upload to B2: {avatar_path}'))
                    migrated += 1
                else:
                    # Upload to B2
                    with open(local_path, 'rb') as f:
                        file_obj = File(f)
                        b2_storage.save(avatar_path, file_obj)
                    
                    self.stdout.write(self.style.SUCCESS(f'   ✅ Uploaded to B2'))
                    migrated += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Error: {str(e)}'))
                errors += 1

        # Summary
        self.stdout.write(self.style.WARNING('\n' + '='*60))
        self.stdout.write(self.style.WARNING('📋 Migration Summary'))
        self.stdout.write(self.style.WARNING('='*60))
        self.stdout.write(f'\n✅ Migrated: {migrated}')
        self.stdout.write(f'⏭️  Skipped: {skipped}')
        self.stdout.write(f'❌ Errors: {errors}')
        self.stdout.write(f'📊 Total: {total_users}\n')

        if dry_run:
            self.stdout.write(self.style.NOTICE('\n💡 Run without --dry-run to actually migrate files\n'))
        elif migrated > 0:
            self.stdout.write(self.style.SUCCESS('\n🎉 Migration complete! Check your B2 bucket.\n'))
