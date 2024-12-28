import os
import asyncio
from queue import Queue
from typing import Optional
from threading import Thread
from logging import Logger

from config import BaseConfig

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from aiohttp import ClientSession

from dropbox import Dropbox
from dropbox.files import WriteMode


class FileProcessor:
    """
    Processes file system events in separate threads.
    """
    def __init__(self, thread_id: int, event_queue: Queue, logger: Logger, dropbox_token: str):
        self.thread_id = thread_id
        self.event_queue = event_queue
        self.logger = logger
        self.dbx_client = Dropbox(dropbox_token)

    async def _async_upload(self, file_path: str, dropbox_path: str):
        """
        Asynchronous file upload to Dropbox
        """
        async with ClientSession() as session:
            with open(file_path, "rb") as f:
                file_data = f.read()

            result = await asyncio.to_thread(self.dbx_client.files_upload, file_data, dropbox_path,
                                             mode=WriteMode("overwrite"))

            self.logger.info(f"File uploaded to Dropbox: {result.path_display}")

    def run(self):
        while True:
            event: FileSystemEvent = self.event_queue.get()

            if event is None:
                self.logger.info(f"Thread {self.thread_id} exiting.")
                break

            self.logger.info(f"Thread {self.thread_id} processing: {event.src_path} - Event: {event.event_type}")

            if event.event_type in ['created', 'modified']:
                asyncio.run(self._async_upload(event.src_path, f"/{os.path.basename(event.src_path)}"))

            self.event_queue.task_done()


class FileEventHandler(FileSystemEventHandler):
    """
    Handles file system events.
    """
    def __init__(self, event_queue: Queue, allowed_extensions: Optional[list[str]] = None):
        self.event_queue = event_queue
        self.allowed_extensions = allowed_extensions

    def _is_valid_file_type(self, file_path: str) -> bool:
        ret = False

        if self.allowed_extensions:
            ret = any(file_path.endswith(ext) for ext in self.allowed_extensions)

        return ret

    def _handle_event(self, event: FileSystemEvent):
        if not event.is_directory and self._is_valid_file_type(event.src_path):
            self.event_queue.put(event)

    def on_modified(self, event: FileSystemEvent):
        self._handle_event(event)

    def on_created(self, event: FileSystemEvent):
        self._handle_event(event)

    def on_deleted(self, event: FileSystemEvent):
        self._handle_event(event)


class FolderWatcher:
    """
    Watches a folder for changes and delegates tasks to threads.
    """
    def __init__(self, config: BaseConfig, logger: Logger):
        if not os.path.exists(config.source_folder):
            raise ValueError(f"Folder path does not exist: {config.source_folder}")

        self.local_folder_path = config.source_folder
        self.destination_folder_path = config.destination_folder
        self.threads_num = config.max_threads
        self.logger = logger
        self.dropbox_token = config.DROPBOX_TOKEN
        self.allowed_extensions = config.file_filter

        self.event_queue: Queue = Queue()
        self.threads: list[Thread] = []
        self.observer: Observer = Observer()

    def _start_threads(self):
        for i in range(self.threads_num):
            processor = FileProcessor(i, self.event_queue, self.logger, self.dropbox_token)

            thread = Thread(target=processor.run, daemon=True)
            thread.start()

            self.threads.append(thread)

    def run(self):
        self.logger.info(f"Starting folder watcher on: {self.local_folder_path}")

        self._start_threads()

        event_handler = FileEventHandler(self.event_queue, self.allowed_extensions)

        self.observer.schedule(event_handler, self.local_folder_path, recursive=True)
        self.observer.start()

        try:
            while True:
                pass  # Keep the script running
        except KeyboardInterrupt:
            self._stop()

    def _stop(self):
        self.logger.info("Stopping folder watcher.")
        self.observer.stop()

        # Send exit signal to threads
        for _ in self.threads:
            self.event_queue.put(None)

        # Wait for threads to finish
        for thread in self.threads:
            thread.join()

        self.observer.join()
