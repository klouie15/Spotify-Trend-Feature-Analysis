
# Spotify-Trend-Feature-Analysis
## Introduction
We will be extracting song data from the Spotify API and using data analysis tools such as statistical tests and machine learning models to come to conclusions about the questions we have about the data.

**Contributors:**
- Kevin Louie
- Terence Tang


## Setting up the Web API
- Create a Spotify account and log into the developer website https://developer.spotify.com
- In the developer dashboard, create an "app"
- After creating the app, go into the app's settings
- Copy the client ID and client secret into a .env file in the repository's base directory as follows:
	- ```CLIENT_ID="..."```
	- ```CLIENT_SECRET="..."```
- Now you can access the API!

## Installing Required Libraries
First, install [Python3](https://www.python.org/downloads/)
```
pip3 install pandas numpy spotipy requests python-dotenv scipy scikit-learn matplotlib seaborn
```
Alternatively try ```pip install...``` if pip3 yields an error.

Make sure [Git](https://git-scm.com/) is installed and clone the repository.


## How to Run
Assuming the local environment with .env has been set up with a valid client ID and client secret from the Spotify API:
- Get the track data of 1000 random tracks using the Spotipy library
	- ```python3 get_data.py```
	- Produces "tracks.csv"
- Split the track data into collaborative tracks (two or more artists) and solo tracks
	- ```python3 split_collab_tracks.py tracks.csv collabs.csv solos.csv```
	- Takes in "tracks.csv" as input and outputs "collabs.csv" and "solos.csv"
- Now you can run either analyze-collab-trends.ipynb or feature-popularity-correlation.ipynb
	- Each cell must be executed in chronological order in both notebooks
	- **Note:** there are already outputs for each cell in the notebooks, but you can re-run them


