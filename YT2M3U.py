import yt_dlp

# CHANGE ME!!!!
playlist_url = 'https://www.youtube.com/playlist?list=PLCfybMeVmbeEcFpijT8pO0C8WsB--tnpu'

# Create M3U file
with open('Playlist.m3u', 'w') as m3u_file:
    m3u_file.write('#EXTM3U\n')  # M3U header
    
    # Use yt-dlp to extract playlist information
    ydl_opts = {
        'quiet': False,  # Show output to help with debugging
        'extract_flat': False,  # Extract full video info (including streams)
        'format': 'bestaudio/bestvideo',  # Choose the best audio and video formats
        'force_generic_extractor': True  # Force a generic extractor if specific ones fail
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            # Check if the info contains videos (for standard playlists)
            if 'entries' in playlist_info:
                total_videos = len(playlist_info['entries'])
                for i, entry in enumerate(playlist_info['entries'], 1):
                    # Get the best video stream URL
                    video = ydl.extract_info(entry['url'], download=False)
                    best_stream_url = None
                    
                    # Look through the available formats for the best video stream URL
                    if 'formats' in video:
                        for fmt in video['formats']:
                            # Select the best quality video stream (you can modify this to fit your needs)
                            if fmt.get('format_id') == '137':  # '137' is usually 1080p
                                best_stream_url = fmt['url']
                                break
                        # Fallback if specific format is not found
                        if not best_stream_url:
                            best_stream_url = video['formats'][0]['url']
                    
                    if best_stream_url:
                        # Print progress
                        videos_left = total_videos - i
                        print(f"Processing video {i}/{total_videos} - URL: {best_stream_url}")
                        print(f"Videos left: {videos_left}")
                        
                        # Write video URL to M3U file
                        m3u_file.write(f'{best_stream_url}\n')

        print("M3U file creation completed successfully.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        # Optionally, print the traceback if you want more details
        import traceback
        traceback.print_exc()
