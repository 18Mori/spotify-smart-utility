from pycaw.pycaw import AudioUtilities

def get_audio_sessions():
    return AudioUtilities.GetAllSessions()

def monitor_audio():
    
    print("Monitoring audio sessions...")
    
    while True:
        sessions = get_audio_sessions()
        # Loop through all audio sessions to find Spotify and check for other active audio
        for session in sessions:
            if session.Process:
                process_name = session.Process.name().lower()
                # Check if the session is Spotify or another app playing audio -- it's important to check for other apps first to avoid ducking Spotify when it's the only one playing. It's the key to avoid a feedback loop where Spotify ducks itself.
                if "spotify.exe" in process_name:
                  spot_session = session
                elif session.State == 1: # Active session audio --
                  other_active_audio = True
                  
                  

if __name__ == "__main__":
  monitor_audio()