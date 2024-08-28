import pandas as pd
import sys
import ast

def collab_solo_split(tracks):
    collabs = tracks[tracks['artists'].apply(len) > 1]
    solos = tracks[tracks['artists'].apply(len) == 1]
    return collabs, solos


def main():
    # python3 split_collab_tracks.py tracks.csv collabs.csv solos.csv
    tracks_file = sys.argv[1]
    collabs_file = sys.argv[2]
    solos_file = sys.argv[3]

    tracks = pd.read_csv(tracks_file)
    tracks['artists'] = tracks['artists'].apply(ast.literal_eval)
    collabs, solos = collab_solo_split(tracks)

    collabs.to_csv(collabs_file, index=False)
    solos.to_csv(solos_file, index=False)


if __name__ == '__main__':
    main()