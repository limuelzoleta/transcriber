# convert mp3 file to wav                                                       
# sound = AudioSegment.from_wav("Athena.wav")
# sound.export("transcript.wav", format="wav")

filename = "transcription.txt"
storage_uri = 'gs://audio-bucket-limuel/kyhander.wav'
model = 'default' # The transcription model to use, e.g. video, phone_call, default
f = open(filename, "w").close()

def transcribe_gcs(storage_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=storage_uri)
    config = speech.RecognitionConfig(
        language_code="fil-PH",
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=9000)

    f = open(filename, "a")
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        f.write("{} \n".format(result.alternatives[0].transcript))
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
    f.close()

transcribe_gcs(storage_uri)