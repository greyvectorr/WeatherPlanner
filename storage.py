"""
storage.py - local persistence for favourite locations and search history,
using plain JSON files on disk (no database needed for this app).

Every read function is defensive: a missing file, an empty file, or a
corrupted file all result in an empty list being returned rather than a
crash - a broken data file should never stop the app from starting.
"""
