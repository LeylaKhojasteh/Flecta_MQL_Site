"""Upload local MEDIA_ROOT files to the configured storage backend.

Used once after switching media to Supabase Storage (S3), so existing
bundled images keep working at their new URLs::

    SUPABASE_STORAGE_BUCKET=... SUPABASE_URL=... \
    SUPABASE_STORAGE_ACCESS_KEY=... SUPABASE_STORAGE_SECRET_KEY=... \
    python manage.py upload_media --settings=flectasite.setting.vercel
"""

from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Upload files from MEDIA_ROOT to the configured media storage."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List files that would be uploaded without uploading.",
        )

    def handle(self, *args, **options):
        backend = default_storage.__class__.__module__
        if "storages.backends" not in backend:
            self.stderr.write(
                "Default storage is %s, not a remote backend. Set the "
                "SUPABASE_STORAGE_* env vars first." % backend
            )
            return

        root = Path(settings.MEDIA_ROOT)
        if not root.is_dir():
            self.stderr.write("MEDIA_ROOT does not exist: %s" % root)
            return

        dry_run = options["dry_run"]
        uploaded = 0
        skipped = 0

        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            name = path.relative_to(root).as_posix()
            if default_storage.exists(name):
                skipped += 1
                continue
            if dry_run:
                self.stdout.write("would upload %s" % name)
                continue
            with path.open("rb") as handle:
                default_storage.save(name, handle)
            uploaded += 1
            self.stdout.write("uploaded %s" % name)

        self.stdout.write(
            "done: %s uploaded, %s already present%s"
            % (uploaded, skipped, " (dry run)" if dry_run else "")
        )
