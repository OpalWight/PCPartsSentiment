# PC Parts Brand Sentiment Analyzer

A Python tool that analyzes sentiment towards PC component brands in the r/pcbuilds subreddit using Reddit API and VADER sentiment analysis.

## Features

- 🔍 Scrapes posts and comments from r/pcbuilds
- 🏷️ Identifies mentions of popular PC component brands
- 💭 Analyzes sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner)
- 📊 Provides detailed sentiment scores and summaries
- ⚡ Rate-limited to respect Reddit API guidelines
- 🎛️ Configurable via environment variables

## Quick Start

### 1. Get Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Note your `client_id` (under the app name) and `client_secret`

### 2. Setup

```bash
# Clone the repository
git clone <repository-url>
cd PCPartsSentiment

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your Reddit API credentials
# REDDIT_CLIENT_ID=your_client_id_here
# REDDIT_CLIENT_SECRET=your_client_secret_here
# REDDIT_USER_AGENT=PCPartsSentiment/1.0 by YourUsername
```

### 3. Run Analysis

```bash
# Basic usage
python main.py

# Analyze more posts
python main.py --posts 200

# Verbose output
python main.py --verbose
```

## Configuration

### Environment Variables (.env)

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `REDDIT_CLIENT_ID` | Yes | Reddit API client ID | - |
| `REDDIT_CLIENT_SECRET` | Yes | Reddit API client secret | - |
| `REDDIT_USER_AGENT` | Yes | Unique user agent string | PCPartsSentiment/1.0 |
| `REDDIT_USERNAME` | No | Reddit username (for authenticated requests) | - |
| `REDDIT_PASSWORD` | No | Reddit password (for authenticated requests) | - |
| `MAX_POSTS` | No | Default number of posts to analyze | 100 |
| `RATE_LIMIT_DELAY` | No | Delay between API calls (seconds) | 2 |

### Brand Database (brands.json)

The application uses a JSON file to define PC component brands and their aliases. You can modify this file to add or remove brands:

```json
{
  "cpu": ["amd", "ryzen", "intel", "i5", "i7", "i9"],
  "gpu": ["nvidia", "rtx", "gtx", "amd", "radeon", "rx"],
  "motherboard": ["asus", "msi", "gigabyte", "asrock"],
  ...
}
```

## Output

The tool provides:

- **Brand-specific results**: Mention count, average sentiment score, and classification
- **Summary statistics**: Total brands analyzed, sentiment distribution
- **Overall metrics**: Total mentions and average sentiment

### Sentiment Classification

- **Positive**: Compound score ≥ 0.05
- **Neutral**: Compound score between -0.05 and 0.05  
- **Negative**: Compound score ≤ -0.05

## Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --posts INTEGER     Number of posts to analyze (default: 100)
  --verbose, -v       Enable verbose output
  --help             Show help message
```

## Examples

### Basic Analysis
```bash
python main.py
```

### Analyze 500 Posts with Verbose Output
```bash
python main.py --posts 500 --verbose
```

## Technical Details

### Architecture

- **reddit_scraper.py**: Handles Reddit API interaction using PRAW
- **brand_matcher.py**: Identifies brand mentions using regex patterns
- **sentiment_analyzer.py**: Performs sentiment analysis using NLTK's VADER
- **config.py**: Manages configuration and environment variables
- **main.py**: CLI interface and result formatting

### Rate Limiting

The tool respects Reddit's API rate limit (100 requests per minute) by:
- Adding configurable delays between requests
- Processing a reasonable number of posts per run
- Using PRAW which handles some rate limiting automatically

### Data Processing

1. Scrapes post titles, bodies, and top-level comments
2. Normalizes text and applies regex matching for brands
3. Analyzes sentiment for each text containing brand mentions
4. Aggregates scores by brand and calculates averages

## Troubleshooting

### Common Issues

**"Reddit API credentials are required"**
- Ensure your `.env` file exists and contains valid credentials
- Check that variable names match exactly (case-sensitive)

**"No brand mentions found"**
- Try increasing the number of posts with `--posts`
- Check if the subreddit has recent activity
- Verify your internet connection

**Rate limiting errors**
- Increase `RATE_LIMIT_DELAY` in your `.env` file
- Reduce the number of posts being analyzed

**VADER lexicon download issues**
- The tool will automatically download NLTK data on first run
- Ensure you have internet connectivity
- Check firewall settings if download fails

## Dependencies

- `praw==7.7.1` - Python Reddit API Wrapper
- `nltk==3.8.1` - Natural Language Toolkit (VADER sentiment analysis)
- `python-dotenv==1.0.0` - Environment variable management
- `requests==2.31.0` - HTTP library (backup functionality)

## License

This project is for educational and personal use. Please respect Reddit's Terms of Service and API guidelines.

## Contributing

Feel free to submit issues and enhancement requests!