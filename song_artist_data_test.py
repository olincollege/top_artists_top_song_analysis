"""
Unit tests
"""
import os
from song_artist_data import write_data_to_csv

def test_minimal_data():
    write_data_to_csv({
        "a": {
            "loudness": 1,
        }
    }, "test_minimal.csv", ["loudness"])
    assert os.path.isfile("test_minimal.csv")
    os.remove("test_minimal.csv")

def test_multiple_features():
    write_data_to_csv({
        "a": {
            "loudness": 1,
            "tempo": 120,
            "energy": 0.8
        }
    }, "test_multiple_features.csv", ["loudness", "tempo", "energy"])
    assert os.path.isfile("test_multiple_features.csv")
    os.remove("test_multiple_features.csv")

def test_multiple_artists_and_features():
    write_data_to_csv({
        "a": {
            "loudness": 1,
            "tempo": 110,
            "energy": 0.8
        },
        "b": {
            "loudness": 1,
            "tempo": 120,
            "energy": 0.8
        },
        "c": {
            "loudness": 2,
            "tempo": 130,
            "energy": 0.8
        }
    }, "test_multiple_artists_features.csv", ["loudness", "tempo", "energy"])
    assert os.path.isfile("test_multiple_artists_features.csv")
    os.remove("test_multiple_artists_features.csv")

def test_csv_content():
    test_data = {
        "Rin": {
            "loudness": 0.5,
            "tempo": 120,
            "energy": 0.8
        },
        "Len": {
            "loudness": 0.5,
            "tempo": 120,
            "energy": 0.6
        }
    }
    write_data_to_csv(test_data, "test_content.csv", ["loudness", "tempo", "energy"])

    with open("test_content.csv", 'r', encoding="utf-8") as file:
        lines = file.readlines()
        # Check header
        assert lines[0].strip() == "artist_name,loudness,tempo,energy"
        # Check content
        assert "Rin,0.5,120,0.8\n" in lines
        assert "Len,0.5,120,0.6\n" in lines
    os.remove("test_content.csv")

def test_empty_data():
    write_data_to_csv({}, "test_empty.csv", ["loudness"])
    assert os.path.isfile("test_empty.csv")
    os.remove("test_empty.csv")


