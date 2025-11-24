import os
import subprocess
import shutil

def convert_audio(input_path, output_path):
    """
    Konvertiert Audio mit ffmpeg auf Mono + 22050 Hz.
    """
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        "-i", input_path,
        "-ac", "1",  # Mono
        "-ar", "22050",  # 22.05 kHz
        output_path
    ]
    subprocess.run(cmd, check=True)

def mimic_to_ljspeech(mimic_audio_dir, mimic_meta_path, output_dir):
    """
    Konvertiert Mimic Recording Studio WAV und Meta in LJ Speech Format.
    
    Args:
        mimic_audio_dir: Verzeichnis mit Mimic WAV Dateien
        mimic_meta_path: Pfad zur Mimic Metadaten-Textdatei (Tab-getrennt: dateiname \t text)
        output_dir: Basisordner für LJ Speech Format (wavs + metadata.csv)
    """
    os.makedirs(output_dir, exist_ok=True)
    wavs_out_dir = os.path.join(output_dir, "wavs")
    os.makedirs(wavs_out_dir, exist_ok=True)
    
    metadata_lines = []

    with open(mimic_meta_path, 'r', encoding='utf-8') as meta_file:
        for line in meta_file:
            line = line.strip()
            if not line:
                continue
            # Erwartet: "<dateiname>\t<text>"
            # parts = line.split('\t')
            parts = line.split('|')
            if len(parts) < 2:
                print(f"Überspringe ungültige Zeile: {line}")
                continue
            print (parts[0] +  "    " + parts[1])
            filename, text = parts[0], parts[1]
            #input_wav_path = os.path.join(mimic_audio_dir, filename + ".wav")
            input_wav_path = os.path.join(mimic_audio_dir, filename )
            output_wav_path = os.path.join(wavs_out_dir, filename )
            
            if not os.path.exists(input_wav_path):
                print(f"Audio-Datei nicht gefunden: {input_wav_path}")
                continue
            
            # Audio konvertieren
            convert_audio(input_wav_path, output_wav_path)
            
            # Metadata: filename|text|text_lowercase
            filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
            metadata_lines.append(f"{filename_without_extension}|{text}|{text.lower()}")
    
    # metadata.csv schreiben
    metadata_path = os.path.join(output_dir, "metadata.csv")
    with open(metadata_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(metadata_lines))
    print(f"LJ Speech Daten erstellt in: {output_dir}")

# Beispiel Nutzung
strUuid = "b7b9a365-2f38-17b0-79fa-a1a8214eb02d"
mimic_audio_folder = "./" + strUuid
mimic_metadata_txt = "./" + strUuid + "/" + strUuid + "-metadata.txt"
output_ljspeech_dir = "./ljspeech-1.1"

mimic_to_ljspeech(mimic_audio_folder, mimic_metadata_txt, output_ljspeech_dir)

