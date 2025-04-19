import os
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd


def _get_exif_data(photo_path):
    # Extract EXIF data from image
    try:
        image = Image.open(photo_path)
        exif_data = image._getexif()
        if exif_data:
            return {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
        return {}
    except Exception:
        return {}


def scan_photos(photo_dir):
    # Extract photo timestamps for matching
    photos = []
    for fn in os.listdir(photo_dir):
        print(f"Processing {fn}")
        if fn.lower().endswith((".jpg", ".jpeg", ".png")):
            full = os.path.join(photo_dir, fn)
            exif = _get_exif_data(full)
            ts_str = exif.get("DateTimeOriginal") or exif.get("DateTime")
            ts = pd.to_datetime(ts_str, format="%Y:%m:%d %H:%M:%S", errors="coerce")
            if pd.notna(ts):
                photos.append({"filename": fn, "path": full, "timestamp": ts})
    return pd.DataFrame(photos)


def match_photos_to_track(track_df, photo_df, max_time_diff_sec=60):
    """
    Match each photo to the nearest GPX point by timestamp.
    If you paused the watch during run, the photo's timestamp
    might be too far from a GPX point. Try to increase the threshold.
    """
    matches = []
    print(f"First and last timestamps in route: {track_df['time'].min(), track_df['time'].max()}")
    print(f"Timestamps for photo: {photo_df['timestamp']}")

    for _, photo in photo_df.iterrows():
        diffs = (track_df["time"] - photo["timestamp"]).abs()
        idx = diffs.idxmin()
        if diffs.loc[idx].total_seconds() <= max_time_diff_sec:
            pt = track_df.loc[idx]
            matches.append(
                {
                    "filename": photo["filename"],
                    "path": photo["path"],
                    "timestamp": photo["timestamp"],
                    "lat": pt["latitude"],
                    "lon": pt["longitude"],
                }
            )
        else:
            print(f"Time stamp for photo {photo['filename']} did not match any point in the route.")
    return pd.DataFrame(matches)
