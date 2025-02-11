# sync-folders

A Python tool for automatically synchronizing a replica folder with a source folder at regular intervals. It ensures that new files from the source are copied to the replica, modifies files if they have the same name but different content, and removes files from the replica if they no longer exist in the source. All changes are recorded in a log file with timestamps for tracking actions.

How to Run:

python synchronize.py --source_folder "/path/to/source" --replica_folder "/path/to/replica" --sync_time 5 --log_file "/path/to/sync_log.txt"


Parameters:

--source_folder → Path to the source directory.
--replica_folder → Path to the replica directory.
--sync_time → Synchronization interval (in seconds).
--log_file → Path to the log file where changes are recorded.

Example:

python synchronize.py --source_folder "/home/user/source" --replica_folder "/home/user/replica" --sync_time 10 --log_file "/home/user/sync_log.txt"
