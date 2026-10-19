"""Put a job's original files in its real Google Drive FieldNation folder.

The pipeline supplies a validated event and the job's input paths. This file
creates the City-Date-Store folder and its needed subfolders, then uploads
each source once. Stable private labels let a rerun find an upload if an earlier
run stopped after Google saved it but before the local checkpoint was written.
"""

import hashlib
from pathlib import Path

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from file_copying import _slug
from google_auth import get_google_service
from runtime_log import LOCK, read_state, write_state


FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"


class GoogleDriveWriter:
    """Create or find the Drive folders and source files for one job."""

    def __init__(self, credentials_path: Path, token_path: Path):
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        self._service = None

    @property
    def service(self):
        """Sign in only when a valid job reaches the Drive destination."""
        if self._service is None:
            self._service = get_google_service(
                "drive", "v3", self.credentials_path, self.token_path
            )
        return self._service

    def write(self, job, event, parent_folder_id: str) -> dict:
        """Upload a job's originals and return the real folder link from Drive."""
        store = event.store or "Unknown-Store"
        folder_name = f"{_slug(event.city or 'Unknown')}-{event.date}-{_slug(store)}"
        job_folder = self._find_or_create_folder(
            folder_name,
            parent_folder_id,
            f"folder:{parent_folder_id}:{job.key}:{folder_name}",
        )

        key_parts = Path(job.key).parts
        for source, source_name in zip(job.files, job.source_names):
            relative = Path(source_name)
            # Grouped jobs leave their outer work-order folder behind, while
            # loose files and any deeper folders keep their natural path.
            if key_parts and relative.parts[:len(key_parts)] == key_parts:
                relative = Path(*relative.parts[len(key_parts):])
            if not relative.parts or relative == Path("."):
                relative = Path(source).name

            destination_folder = job_folder["id"]
            folder_path = []
            for part in relative.parts[:-1]:
                folder_path.append(part)
                destination_folder = self._find_or_create_folder(
                    part,
                    destination_folder,
                    f"folder:{job_folder['id']}:{job.key}:{'/'.join(folder_path)}",
                )["id"]

            source_key = hashlib.sha256(
                f"{job.key}\0{source_name}".encode("utf-8")
            ).hexdigest()
            if not self._find_source(source_key, destination_folder):
                resource_id = self._resource_id(f"source:{source_key}")
                if self._get_file(resource_id):
                    continue
                body = {
                    "id": resource_id,
                    "name": relative.name,
                    "parents": [destination_folder],
                    "appProperties": {"calendarBotSource": source_key},
                }
                try:
                    self.service.files().create(
                        body=body,
                        media_body=MediaFileUpload(str(source), resumable=True),
                        fields="id,name,webViewLink",
                        supportsAllDrives=True,
                    ).execute()
                except HttpError as error:
                    if error.resp.status != 409:
                        raise
                    self._get_file(resource_id)

        return {
            "id": job_folder["id"],
            "url": job_folder["webViewLink"],
        }

    def _find_or_create_folder(self, name: str, parent_id: str,
                               identity: str | None = None) -> dict:
        """Reuse the folder at this path, or create it when it is missing."""
        query = (
            f"name = '{_quote_query(name)}' and "
            f"mimeType = '{FOLDER_MIME_TYPE}' and "
            f"'{_quote_query(parent_id)}' in parents and trashed = false"
        )
        matches = self.service.files().list(
            q=query,
            pageSize=100,
            fields="files(id,name,webViewLink)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()["files"]
        if matches:
            return matches[0]

        identity = identity or f"folder:{parent_id}:{name}"
        resource_id = self._resource_id(identity)
        existing = self._get_file(resource_id)
        if existing:
            return existing
        try:
            return self.service.files().create(
                body={"id": resource_id, "name": name, "mimeType": FOLDER_MIME_TYPE,
                      "parents": [parent_id]},
                fields="id,name,webViewLink",
                supportsAllDrives=True,
            ).execute()
        except HttpError as error:
            if error.resp.status != 409:
                raise
            return self._get_file(resource_id)

    def _find_source(self, source_key: str, parent_id: str) -> dict | None:
        """Find a previously uploaded source without replacing its contents."""
        query = (
            f"appProperties has {{ key='calendarBotSource' and value='{source_key}' }} and "
            f"'{_quote_query(parent_id)}' in parents and trashed = false"
        )
        matches = self.service.files().list(
            q=query,
            pageSize=100,
            fields="files(id,name,webViewLink)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()["files"]
        return matches[0] if matches else None

    def _resource_id(self, identity: str) -> str:
        """Save a Drive-generated ID before creating its folder or uploaded file."""
        runtime_path = self.credentials_path.parent / "runtime.yaml"
        with LOCK:
            state = read_state(runtime_path)
            ids = state.setdefault("drive_ids", {})
            if identity not in ids:
                generated = self.service.files().generateIds(count=1, space="drive").execute()
                ids[identity] = generated["ids"][0]
                write_state(runtime_path, state)
            return ids[identity]

    def _get_file(self, file_id: str) -> dict | None:
        """Read a saved Drive item, returning nothing only when Google says 404."""
        try:
            return self.service.files().get(
                fileId=file_id,
                fields="id,name,mimeType,webViewLink",
                supportsAllDrives=True,
            ).execute()
        except HttpError as error:
            if error.resp.status == 404:
                return None
            raise


def _quote_query(value: str) -> str:
    """Escape a name or ID before placing it inside Drive's query quotes."""
    return value.replace("\\", "\\\\").replace("'", "\\'")
