import tweepy
from dotenv import load_dotenv
import os
import random
import time
import schedule
from datetime import datetime, timedelta
import pytz
from flask import Flask, jsonify
import logging
import threading

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask App
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Current user and time information
CURRENT_USER = 'oye-bobs'
CURRENT_TIME = '2024-12-24 11:18:11'

# Twitter API rate limits
TWEET_LIMIT = 50  # Tweets per 24 hours
tweet_count = 0
last_reset = datetime.now(pytz.UTC)

# Verify environment variables
required_env_vars = [
    'TWITTER_API_KEY',
    'TWITTER_API_SECRET_KEY',
    'TWITTER_ACCESS_TOKEN',
    'TWITTER_ACCESS_TOKEN_SECRET'
]

for var in required_env_vars:
    if not os.getenv(var):
        logger.error(f"Missing required environment variable: {var}")
        raise RuntimeError(f"Missing required environment variable: {var}")

# Set up Twitter API v2 credentials
try:
    client = tweepy.Client(
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    logger.info("Twitter client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Twitter client: {e}")
    raise

# Track used facts
used_facts = set()
# Facts list
# Your facts list
facts = ["The movement emerged in the early 17th century through three manifestos: the Fama Fraternitatis, Confessio Fraternitatis, and the Chymical Wedding of Christian Rosenkreutz.",
    "The Rose Cross symbolizes both spiritual unfolding (the rose) and the sacrifice of physical existence (the cross).",
    "The rose represents divine love and the unfolding of consciousness, while the cross embodies earthly trials.",
    "The founder of the order, Christian Rosenkreutz, is said to have lived to 106, embodying the virtues of spiritual longevity.",
    "The Chymical Wedding is an allegorical text describing the mystical union of opposites, an essential theme in alchemy.",
    "In mystical thought, the number 7 holds deep significance, representing creation, completion, and spiritual evolution.",
    "The movement believed in the harmony between science, spirituality, and nature, paving the way for the Enlightenment.",
    "Alchemy symbolizes the transformation of the base human self into spiritual gold.",
    "The ideal of 'The Invisible College' represents a fraternity of wisdom seekers dedicated to truth and enlightenment.",
    "The Golden Dawn and Freemasonry drew heavily upon principles of esoteric knowledge.",
    "The Hermetic maxim 'As above, so below' signifies the connection between the microcosm and macrocosm.",
    "The sacred rose symbolizes the heart center, where divine illumination manifests in human consciousness.",
    "Astrology was often studied, believing celestial movements mirrored earthly transformations.",
    "The Seven Alchemical Processes—calcination, dissolution, separation, conjunction, fermentation, distillation, and coagulation—parallel spiritual awakening.",
    "The concept of The Philosopher's Stone signifies achieving spiritual enlightenment and immortality.",
    "Silence was considered a divine tool; inner stillness unlocks cosmic knowledge.",
    "The Temple of the Rosy Cross is said to reside within the heart of every seeker.",
    "The teachings affirm that the universe is a vast living organism, vibrating with divine energy.",
    "The Vault of Christian Rosenkreutz is said to symbolize the hidden wisdom of the ages.",
    "The spiritual Sun represents the divine light of consciousness illuminating the path of the soul.",
    "Meditation on sacred symbols, such as the rose, star, and pentagram, was often practiced.",
    "Philosophy blends Christian mysticism, Hermeticism, and alchemical traditions into a unified spiritual system.",
    "The 'Invisible Brotherhood' was said to work anonymously to uplift humanity.",
    "Alchemy's metaphorical prima materia refers to the raw, unrefined human condition awaiting spiritual transformation.",
    "In art, the rose frequently blooms over the cross to signify spiritual resurrection.",
    "The Mystical Marriage of the soul and spirit represents the ultimate union of opposites in mystical thought.",
    "The seven planets correspond to the chakras and levels of consciousness.",
    "Teachings suggest that the soul undergoes cycles of reincarnation to achieve ultimate unity with the divine.",
    "Every individual carries the seeds of divinity within their heart.",
    "Sacred geometry reflects divine intelligence in the structure of the cosmos.",
    "The rose blooming on the cross represents the triumph of spiritual wisdom over material suffering.",
    "The motto, 'Ex Deo Nascimur, In Jesu Morimur, Per Spiritum Sanctum Reviviscimus' means: 'From God we are born, in Jesus we die, through the Holy Spirit we are reborn.'",
    "The color red signifies life force, passion, and divine fire.",
    "The rose of secrecy was often hung above meetings to signify confidentiality, giving rise to the phrase 'sub rosa' (under the rose).",
    "The heart is seen as the sacred altar where divine illumination occurs.",
    "The number 12 symbolizes cosmic order, reflected in zodiac signs, apostles, and alchemical stages.",
    "Christian Rosenkreutz’s vault was said to contain sacred objects and symbols of universal knowledge.",
    "The Law of Correspondence—what happens within mirrors what happens without—is a key teaching.",
    "Nature is viewed as a divine book, filled with symbols awaiting decipherment by the awakened soul.",
    "The rose garden represents a sanctuary of inner peace and spiritual transformation.",
    "The teachings affirm the importance of cultivating the virtues of wisdom, truth, and universal love.",
    "Alchemy’s spiritual gold signifies the state of perfected, illuminated consciousness.",
    "The 'Great Work' refers to attaining spiritual enlightenment through dedicated inner transformation.",
    "God is referred to as The Master Architect, the divine intelligence behind all creation.",
    "The pentagram is a symbol of the divine human being—spirit ruling over the four elements.",
    "The alchemy of the soul involves transmuting lower emotions into divine love and wisdom.",
    "The unfolding spiritual consciousness is symbolized by the blooming rose.",
    "The mystic light refers to divine illumination awakening the soul’s higher faculties.",
    "The dawn symbolizes enlightenment, the rising of inner light after a dark night of the soul.",
    "Spiritual alchemy teaches the balance of mind, body, and soul for harmonious living.",
    "The secrets of the universe can be uncovered through study, meditation, and inner awakening.",
    "The Rose Cross symbol combines both spiritual aspiration (the rose) and earthly trials (the cross), representing the path of enlightenment.",
    "The power of the word is emphasized, as speech can shape the material world when aligned with spiritual truth.",
    "The chymical wedding symbolizes the alchemical union of the soul with divine wisdom, where opposites are harmonized.",
    "The movement affirms that every person is a microcosm of the universe, containing divine potential.",
    "The path to enlightenment is often a solitary journey, requiring deep inner work and self-purification.",
    "The seventh ray represents the integration of spiritual energy into the material world, embodying divine will.",
    "The number 3 is a symbol of divine harmony, unity, and the manifestation of the trinity in all things.",
    "Rituals and ceremonies often involve the use of sacred symbols to align the practitioner’s energy with universal principles.",
    "The teachings affirm the existence of an immortal, divine spark within every human being, often referred to as the inner Christ.",
    "Spiritual alchemy signifies the transformation of the ego into a divine vessel of pure consciousness.",
    "Hermetic wisdom is valued as a path to understanding the hidden forces of the universe.",
    "The Eye of Horus represents spiritual insight, protection, and the awakening of higher faculties.",
    "Purification is central to the process, as the individual must cleanse the mind, body, and soul to attain spiritual illumination.",
    "The Manifestos reveal the inner workings of a mystical society seeking to uplift humanity through esoteric knowledge and spiritual practices.",
    "The sun is seen as a source of divine light and life force, representing the spiritual illumination of the soul.",
    "Ascension occurs when the soul sheds its material attachments and unites with the divine.",
    "Inner alchemy refines spiritual consciousness through meditation and self-awareness.",
    "The pentagram signifies the harmony between the physical and spiritual realms, balancing the five elements of existence.",
    "The pyramid represents the connection between heaven and earth, the path of spiritual ascent, and the sacred geometry of the universe.",
    "The astral plane is considered a realm of spiritual potential, where the soul can explore higher dimensions of existence.",
    "The Great Work involves the soul’s journey towards its own divinity, refining the self through continual spiritual practice.",
    "The rose symbolizes not only spiritual enlightenment but also the unfolding of consciousness in stages, from bud to bloom.",
    "Initiates often work with sacred texts and symbols, believing they contain hidden knowledge that can guide the soul toward enlightenment.",
    "Alchemy is both a literal and metaphorical process of turning base materials into spiritual gold, signifying the transformation of the self."] # Your existing facts list


def check_rate_limit():
    """Check if we're within rate limits"""
    global tweet_count, last_reset
    
    now = datetime.now(pytz.UTC)
    if (now - last_reset).total_seconds() >= 86400:
        tweet_count = 0
        last_reset = now
        logger.info("Rate limit counter reset")
    
    return tweet_count < TWEET_LIMIT

def get_random_fact():
    """Get a random fact avoiding repetition"""
    global used_facts
    if len(used_facts) >= len(facts):
        used_facts.clear()
    
    available_facts = [f for f in facts if f not in used_facts]
    fact = random.choice(available_facts)
    used_facts.add(fact)
    return fact

def post_fact():
    """Post a random fact to Twitter with rate limit handling"""
    if not check_rate_limit():
        logger.warning("Tweet skipped - Rate limit reached")
        return False, "Rate limit reached"
    
    fact = get_random_fact()
    try:
        response = client.create_tweet(text=fact)
        global tweet_count
        tweet_count += 1
        
        current_time = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
        logger.info(f"Tweet posted successfully at {current_time}")
        logger.info(f"Tweet count: {tweet_count}/{TWEET_LIMIT}")
        return True, "Success"
    except tweepy.TooManyRequests as e:
        logger.error(f"Rate limit exceeded: {e}")
        return False, "Rate limit exceeded"
    except Exception as e:
        logger.error(f"Error posting tweet: {e}")
        return False, str(e)

def verify_credentials():
    """Verify Twitter API credentials without posting"""
    try:
        user = client.get_me()
        logger.info(f"Credentials verified for user: {user.data.username}")
        return True
    except Exception as e:
        logger.error(f"Failed to verify credentials: {e}")
        return False

# Schedule tweets every 6 hours instead of hourly
schedule.every(6).hours.do(lambda: post_fact()[0])

def run_schedule():
    """Run scheduled tasks"""
    logger.info("Schedule thread starting...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"Schedule error: {e}")
            time.sleep(60)

# Flask routes
@app.route('/')
def home():
    next_run = schedule.next_run()
    now = datetime.now(pytz.UTC)
    time_until_reset = 86400 - (now - last_reset).total_seconds()
    
    return jsonify({
        "status": "running",
        "bot_user": CURRENT_USER,
        "current_time": now.strftime('%Y-%m-%d %H:%M:%S UTC'),
        "next_tweet": next_run.strftime('%Y-%m-%d %H:%M:%S UTC') if next_run else "Unknown",
        "rate_limit": {
            "tweets_remaining": TWEET_LIMIT - tweet_count,
            "reset_in_seconds": max(0, time_until_reset),
            "reset_at": (last_reset + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S UTC')
        },
        "facts_used": f"{len(used_facts)}/{len(facts)}"
    })

@app.route('/rate-limit')
def rate_limit_status():
    """Check rate limit status"""
    now = datetime.now(pytz.UTC)
    time_until_reset = 86400 - (now - last_reset).total_seconds()
    
    return jsonify({
        "tweets_used": tweet_count,
        "tweets_remaining": TWEET_LIMIT - tweet_count,
        "reset_in_seconds": max(0, time_until_reset),
        "reset_at": (last_reset + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S UTC')
    })

@app.route('/test-tweet')
def test_tweet():
    """Send a test tweet with rate limit checking"""
    if not check_rate_limit():
        return jsonify({"status": "error", "message": "Rate limit reached"}), 429
    
    try:
        current_time = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
        test_message = f"Test tweet from Rosicrucian Bot - {CURRENT_USER} at {current_time}"
        response = client.create_tweet(text=test_message)
        global tweet_count
        tweet_count += 1
        return jsonify({"status": "success", "message": "Test tweet sent"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/post-now')
def post_now():
    """Post immediate tweet with rate limit checking"""
    success, message = post_fact()
    return jsonify({
        "status": "success" if success else "error",
        "message": message,
        "tweets_remaining": TWEET_LIMIT - tweet_count
    })

def create_app():
    """Create and configure the Flask application"""
    if not verify_credentials():
        logger.error("Failed to verify credentials. Exiting.")
        return None

    # Start the schedule thread
    schedule_thread = threading.Thread(target=run_schedule, name="ScheduleThread")
    schedule_thread.daemon = True
    schedule_thread.start()
    logger.info("Schedule thread started - Tweets every 6 hours")
    
    return app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

