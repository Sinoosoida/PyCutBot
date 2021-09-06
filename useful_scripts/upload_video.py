from src.processing.yt_upload import upload

upload.upload_video_to_youtube(
    video_path="../test_multimedia/monke_helps.mp4",
    # thumbnail_path='../test_tumbnail.png',
    title="MONKE HELPS",
    description="just helping monkey",
    tags=[],
    app_version=5,
)
