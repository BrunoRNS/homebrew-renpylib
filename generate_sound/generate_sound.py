
import os
from pathlib import Path
from typing import Any, List
from pyIT import (
    IT2ogg,
    ITfile,
    ITpattern,
    PatternBuilder,
    SchismRenderer,
    WavInstrumentBuilder
)
import shutil
import math


def _generate_partiture_aquarela() -> List[Any]:
    """
    Partiture of aquarela music, more info here: https://www.cifraclub.com.br/toquinho/aquarela/
    """

    partiture: List[Any] = [
        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "C#5", "C#5", None, None,
        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "C#5", "B-4", "A-4", None, None,

        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "C#5", "C#5", None, None,
        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "C#5", "B-4", "A-4", None, None,

        "E-5", "E-5", "A-5", "A-5", None, "G#5", "F#5", None,
        "E-5", "E-5", "A-5", "A-5", None, "G#5", "F#5", None,
        "E-4", "E-4", "F#5", "F#5", None, None,
        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "E-5", "E-5", None, "D#5", "C#5", None,
        "B-4", "B-4", "D#5", "F-5", None, None, None,

        "E-5", "E-5", "F#5", "E-5", None,
        "G#5", "A-5", "G#5", "F#5", None,
        "E-5", "E-5", "F#5", "E-5", None,
        "F#5", "G#5", "F#5", None,

        "G#5", None,
        "A-5", "G#5", "A-5", "G#5", None,
        "A-5", "G#5", "F#5", "E-5", None,
        "F#5", "E-5", None,
        "D#5", "E-5", "G#5", "F#5", None, "E-5", "F#5", None, None,
        "F#5", "G#5", "F#5", "E-5", "E-5", None, None
    ]

    return partiture


def _generate_partiture_tada() -> List[Any]:
    """
    A simple partiture for the TADA sound, which is just a special effect.
    """

    partiture: List[Any] = [
        "C-6", "E-6", "F-6", None
    ]

    return partiture


def _generate_patterns(partitures: List[Any], bpm: int, lpn: int) -> List[ITpattern]:
    """
    Generate a list of patterns from a list of partitures.
    """

    pb = PatternBuilder(bpm=bpm, lines_per_note=lpn)

    max_partiture_size = math.floor(64 / lpn)

    partitures_sliced: List[List[Any]] = []

    i = 0
    k = 0
    while i < len(partitures):
        for j in range(max_partiture_size):
            if i + j >= len(partitures):
                break
            if j == 0:
                partitures_sliced.append(list())
            partitures_sliced[k].append(partitures[i + j])
        i += max_partiture_size
        k += 1

    patterns: List[ITpattern] = []

    for i, partiture in enumerate(partitures_sliced):

        if i == len(partitures_sliced) - 1:
            pattern = pb.build_pattern(partiture, stop_line=pb.last_index(
                partitures_sliced[i]
            ))
            patterns.append(pattern)
            break

        pattern = pb.build_pattern(partiture)
        patterns.append(pattern)

    return patterns


def _generate_tracker_file(
    path: Path,
    name: str,
    patterns: List[ITpattern],
    instrument_path: Path,
    bpm: int,
) -> None:
    """
    Generate the final Impulse Tracker file from a list of patterns.
    """
    music = ITfile()
    music.SongName = name
    music.IT = bpm

    instrument, sample = WavInstrumentBuilder.create_from_wav(
        str(instrument_path.resolve()), instrument_name=instrument_path.name.split(".")[0]
    )

    for note in range(120):
        instrument.SampleTable[note] = [note, 1]

    music.Samples.append(sample)
    music.Instruments.append(instrument)

    for pattern in patterns:
        music.Patterns.append(pattern)

    music.Orders.extend([*list(range(len(music.Patterns))), 255])

    music.write(str(path.resolve()))


def _generate_ogg_from_tracker_files(
    path_in: Path,
    path_out: Path,
) -> None:
    """
    Convert the Impulse Tracker file to an OGG file.
    """
    try:
        if not (Path(os.environ["SCHISM_HOME"]).resolve() / "run.sh").is_file():
            raise OSError(
                "$SCHISM_HOME/run.sh command not found, please set the environment "
                "variable SCHISM_HOME and execute in a linux environment with run.sh")
        if not shutil.which("ffmpeg"):
            raise OSError(
                "ffmpeg command not found")
    except OSError as e:
        print("Exiting with fatal error: ", e)
        raise e

    converter = IT2ogg(path_in, path_out, 32000, 1, renderer=SchismRenderer(
        str(Path(
            os.environ["SCHISM_HOME"]
        ).resolve() / "run.sh")
    )
    )
    converter.convert()


def generate_sound_files() -> None:
    """
    Generate all sound files.
    """

    partiture_sound = _generate_partiture_tada()
    partiture_music = _generate_partiture_aquarela()

    patterns_sound = _generate_patterns(partiture_sound, bpm=200, lpn=3)
    patterns_music = _generate_patterns(partiture_music, bpm=152, lpn=2)

    BASE_DIR = Path(__file__).parent.parent / "tests" / \
        "test_audio" / "game" / "audio"

    instrument: Path = BASE_DIR / "instruments" / "violin.wav"

    _generate_tracker_file(
        BASE_DIR / "tada.it", "TADA", patterns_sound, instrument, bpm=200
    )

    _generate_tracker_file(
        BASE_DIR / "aquarela.it", "AQUARELA", patterns_music, instrument, bpm=152
    )

    _generate_ogg_from_tracker_files(
        BASE_DIR / "tada.it", BASE_DIR / "tada.ogg")
    _generate_ogg_from_tracker_files(
        BASE_DIR / "aquarela.it", BASE_DIR / "aquarela.ogg")

    print("Sound files generated successfully.")
