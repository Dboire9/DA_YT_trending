# YouTube Top 1000 FR Data Analysis

This project scrapes the top 1000 most popular YouTube videos in France using the YouTube Data API, enriches the data with channel subscriber counts, and provides a suite of visualizations for exploratory data analysis.

## Features

- **Data Collection:**  
  - Fetches the top trending videos in France via the YouTube Data API.
  - Collects video statistics (views, likes, comments, etc.), channel info (subscriber count), content details (duration, definition, etc.), and metadata (publish time, live broadcast status, content rating).

- **Data Storage:**  
  - Saves the collected data as `youtube_top_1000_videos_FR.csv`.

- **Visualization & Analysis:**  
  - Scatter plots: Views vs. Likes, Views vs. Subscriber Count.
  - Time-based analysis: Number of videos and total views by hour and day of publication.
  - Live broadcast analysis: Distribution of live vs. non-live videos.

## Usage

1. **Install dependencies:**
    ```bash
    pip install pandas matplotlib seaborn python-dotenv google-api-python-client isodate
    ```

2. **Set up your API key:**
    - Create a `.env` file in the project directory:
      ```
      GOOGLE_API_KEY=YOUR_YOUTUBE_API_KEY
      ```

3. **Scrape the data:**
    ```bash
    python Scrap_yt.py
    ```

4. **Visualize and analyze:**
    ```bash
    python Visualize.py
    ```

## Files

- `Scrap_yt.py` — Scrapes YouTube data and saves it as a CSV.
- `Visualize.py` — Loads the CSV and generates various plots for analysis.
- `.env` — Stores your YouTube API key (not included in version control).
- `youtube_top_1000_videos_FR.csv` — The resulting dataset.

## Notes

- The YouTube API only allows access to currently trending videos, not all-time most popular.
- Some fields (like content rating) may be empty for many videos.
- Make sure your API key has sufficient quota for the requests.

## Example Visualizations

- View count vs. like count
- View count vs. subscriber count
- Number of videos and total views per hour/day of publication
- Distribution of live vs. non-live videos
- Views per minute of video duration
- Presence of content ratings

---

**Author:**  
Dorian Boiré
