import tweepy
from dotenv import load_dotenv
import os
import time
import random
import schedule
from datetime import datetime, timedelta
import pytz

# Load environment variables from .env file
load_dotenv()

# Set up Twitter API v2 credentials
client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

# Predefined facts
facts = [
"Rosicrucianism emerged in the early 17th century through three manifestos: the Fama Fraternitatis, Confessio Fraternitatis, and the Chymical Wedding of Christian Rosenkreutz."
"The Rosy Cross symbolizes both spiritual unfolding (the rose) and the sacrifice of physical existence (the cross)."
"The rose in Rosicrucianism represents divine love and the unfolding of consciousness, while the cross embodies earthly trials."
"The founder of the Rosicrucian order, Christian Rosenkreutz, is said to have lived to 106, embodying the virtues of spiritual longevity."
"The Chymical Wedding is an allegorical text describing the mystical union of opposites, an essential theme in alchemy."
"In Rosicrucian thought, the number 7 holds deep significance, representing creation, completion, and spiritual evolution."
"The Rosicrucians believed in the harmony between science, spirituality, and nature, paving the way for the Enlightenment."
"Alchemy, central to Rosicrucian philosophy, symbolizes the transformation of the base human self into spiritual gold."
"The Rosicrucian ideal of 'The Invisible College' represents a fraternity of wisdom seekers dedicated to truth and enlightenment."
"The Golden Dawn and Freemasonry drew heavily upon Rosicrucian principles of esoteric knowledge."
"The Hermetic maxim 'As above, so below' resonates deeply within Rosicrucian philosophy, signifying the connection between the microcosm and macrocosm."
"The sacred rose symbolizes the heart center, where divine illumination manifests in human consciousness."
"Rosicrucian initiates often studied astrology, believing celestial movements mirrored earthly transformations."
"The Seven Alchemical Processes—calcination, dissolution, separation, conjunction, fermentation, distillation, and coagulation—parallel spiritual awakening."
"The concept of The Philosopher's Stone signifies achieving spiritual enlightenment and immortality."
"Rosicrucians consider silence a divine tool; inner stillness unlocks cosmic knowledge."
"The Temple of the Rosy Cross is said to reside within the heart of every seeker."
"Rosicrucian teachings affirm that the universe is a vast living organism, vibrating with divine energy."
"The Rosicrucian Vault of Christian Rosenkreutz is said to symbolize the hidden wisdom of the ages."
"The spiritual Sun in Rosicrucianism represents the divine light of consciousness illuminating the path of the soul."
"Rosicrucians often practiced meditation on sacred symbols, such as the rose, star, and pentagram."
"Rosicrucian philosophy blends Christian mysticism, Hermeticism, and alchemical traditions into a unified spiritual system."
"The 'Invisible Rosicrucian Brotherhood' was said to work anonymously to uplift humanity."
"Alchemy's metaphorical prima materia refers to the raw, unrefined human condition awaiting spiritual transformation."
"In Rosicrucian art, the rose frequently blooms over the cross to signify spiritual resurrection."
"The Mystical Marriage of the soul and spirit represents the ultimate union of opposites in Rosicrucian thought."
"Rosicrucian mystics believed in the seven planets corresponding to the chakras and levels of consciousness."
"The Rosicrucian teachings suggest that the soul undergoes cycles of reincarnation to achieve ultimate unity with the divine."
"According to Rosicrucian thought, every individual carries the seeds of divinity within their heart."
"The Rosicrucian understanding of sacred geometry reflects divine intelligence in the structure of the cosmos."
"The rose blooming on the cross represents the triumph of spiritual wisdom over material suffering."
"The Rosicrucian motto, 'Ex Deo Nascimur, In Jesu Morimur, Per Spiritum Sanctum Reviviscimus' means: 'From God we are born, in Jesus we die, through the Holy Spirit we are reborn.'"
"The color red in Rosicrucian symbolism signifies life force, passion, and divine fire."
"The rose of secrecy was often hung above meetings to signify confidentiality, giving rise to the phrase 'sub rosa' (under the rose)."
"The Rosicrucians viewed the heart as the sacred altar where divine illumination occurs."
"The number 12 in Rosicrucian thought symbolizes cosmic order, reflected in zodiac signs, apostles, and alchemical stages."
"Christian Rosenkreutz’s vault was said to contain sacred objects and symbols of universal knowledge."
"Rosicrucian teachings emphasize the Law of Correspondence—what happens within mirrors what happens without."
"The Rosicrucians viewed nature as a divine book, filled with symbols awaiting decipherment by the awakened soul."
"The rose garden in Rosicrucian lore represents a sanctuary of inner peace and spiritual transformation."
"The Rosicrucians believed in cultivating the virtues of wisdom, truth, and universal love."
"Alchemy's spiritual gold signifies the state of perfected, illuminated consciousness."
"The Rosicrucian concept of 'The Great Work' refers to attaining spiritual enlightenment through dedicated inner transformation."
"The Rosicrucians often referred to God as The Master Architect, the divine intelligence behind all creation."
"Rosicrucians used the pentagram as a symbol of the divine human being—spirit ruling over the four elements."
"The alchemy of the soul involves transmuting lower emotions into divine love and wisdom."
"The Rosicrucian rose symbolizes unfolding spiritual consciousness, akin to the blooming of a flower."
"The mystic light in Rosicrucian thought refers to divine illumination awakening the soul’s higher faculties."
"In Rosicrucianism, the dawn symbolizes enlightenment, the rising of inner light after a dark night of the soul."
"The Rosicrucian alchemy of spirit teaches the balance of mind, body, and soul for harmonious living."
"The Rosicrucians believed that the secrets of the universe could be uncovered through study, meditation, and inner awakening."
"The Rosy Cross symbol combines both spiritual aspiration (the rose) and earthly trials (the cross), representing the path of enlightenment."
"Rosicrucian teachings emphasize the power of the word, believing that speech can shape the material world when aligned with spiritual truth."
"The chymical wedding symbolizes the alchemical union of the soul with divine wisdom, where opposites are harmonized."
"The mystical teachings of Rosicrucianism state that every person is a microcosm of the universe, containing divine potential."
"According to Rosicrucian philosophy, the path to enlightenment is often a solitary journey, requiring deep inner work and self-purification."
"The seventh ray in Rosicrucian thought represents the integration of spiritual energy into the material world, embodying divine will."
"Rosicrucians view the number 3 as a symbol of divine harmony, unity, and the manifestation of the trinity in all things."
"Rituals and ceremonies in Rosicrucianism often involve the use of sacred symbols to align the practitioner’s energy with universal principles."
"The Rosicrucian teachings affirm the existence of an immortal, divine spark within every human being, often referred to as the inner Christ."
"Within Rosicrucian philosophy, spiritual alchemy signifies the transformation of the ego into a divine vessel of pure consciousness."
"Rosicrucians value the practice of hermetic wisdom, seeing it as a path to understanding the hidden forces of the universe."
"The Eye of Horus in Rosicrucian symbolism represents spiritual insight, protection, and the awakening of higher faculties."
"In Rosicrucian thought, the process of purification is central, as the individual must cleanse the mind, body, and soul to attain spiritual illumination."
"The Rosicrucian Manifestos reveal the inner workings of a mystical society seeking to uplift humanity through esoteric knowledge and spiritual practices."
"Rosicrucians often meditated on the sun as a source of divine light and life force, representing the spiritual illumination of the soul."
"According to Rosicrucian belief, the process of ascension occurs when the soul sheds its material attachments and unites with the divine."
"Rosicrucians emphasize the importance of inner alchemy, where the practitioner refines their spiritual consciousness through meditation and self-awareness."
"The use of the pentagram in Rosicrucianism signifies the harmony between the physical and spiritual realms, balancing the five elements of existence."
"The pyramid in Rosicrucian symbolism represents the connection between heaven and earth, the path of spiritual ascent, and the sacred geometry of the universe."
"Rosicrucians consider the astral plane a realm of spiritual potential, where the soul can explore higher dimensions of existence."
"The Rosicrucian concept of the Great Work involves the soul’s journey towards its own divinity, refining the self through continual spiritual practice."
"The rose symbolizes not only spiritual enlightenment but also the unfolding of consciousness in stages, from bud to bloom."
"Rosicrucian initiates often work with sacred texts and symbols, believing they contain hidden knowledge that can guide the soul toward enlightenment."
"Alchemy, in Rosicrucianism, is both a literal and metaphorical process of turning base materials into gold, reflecting the spiritual transformation of the soul."
"The three pillars of Rosicrucian philosophy are knowledge, wisdom, and understanding, which must be balanced to achieve spiritual mastery."
"The Rosicrucian tradition teaches that the true meaning of life can only be understood by aligning with the cosmic order and divine will."
"In Rosicrucianism, the sphere represents wholeness and unity, reflecting the divine harmony that exists in all aspects of creation."
"The tree of life in Rosicrucian symbolism represents the growth and expansion of consciousness as the soul ascends through spiritual realms."
"The seven chakras in Rosicrucian teachings correspond to different aspects of the soul's journey toward higher consciousness and spiritual balance."
"Rosicrucians believe that sacred geometry reveals the underlying patterns of the universe and can be used to unlock divine secrets."
"According to Rosicrucian thought, spiritual enlightenment is a journey of constant self-discovery, where the seeker must peel away layers of illusion."
"The soul’s ascent in Rosicrucianism represents the continuous evolution of consciousness, moving from lower forms of existence to higher states of being."
"Rosicrucians view the circle as a symbol of unity, eternity, and divine perfection, representing the eternal cycle of life and death."
"The secret fire in Rosicrucian philosophy symbolizes the divine spark that ignites the soul's journey toward enlightenment."
"Rosicrucians teach that the path to spiritual awakening requires a commitment to purity, humility, and love for all creation."
"The sun in Rosicrucianism is seen as the source of divine light, guiding the soul towards enlightenment and illuminating the path to higher understanding."
"Rosicrucians believe that by understanding the divine mysteries, humanity can elevate itself to a higher plane of existence and experience true liberation."
"The practice of meditative visualization is used by Rosicrucians to direct spiritual energy and manifest higher states of consciousness."
"Rosicrucians believe that the inner temple is the seat of divine wisdom, and through meditation, one can access its hidden treasures."
"Rosicrucianism emphasizes the importance of harmony with nature, viewing it as a reflection of divine order and spiritual balance."
"The Rosicrucians viewed the cosmic mind as a divine consciousness that permeates the entire universe, and aligning with this mind leads to enlightenment."
"In Rosicrucian teachings, the soul's journey is often depicted as a pilgrimage, filled with trials and tests that lead the individual to greater wisdom."
"The serpent in Rosicrucian symbolism is a representation of transformation, as it sheds its skin to symbolize spiritual rebirth and renewal."
"According to Rosicrucian philosophy, death is not an end but a transition to another phase of spiritual evolution and awakening."
"Rosicrucians believe that through sacred rituals, one can tap into divine energy and align their own will with universal laws."
"The hermetic principle of as above, so below emphasizes the connection between the physical world and spiritual realms, where both reflect each other."
"The Rosicrucians believe that the goal of alchemy is not just to transmute metals but to transmute the soul into a state of divine purity."
"Rosicrucians view sacrifice as an essential part of spiritual evolution, where the seeker must give up attachments to the material world to gain higher wisdom."
"By working with the elements—earth, air, fire, and water—a Rosicrucian practitioner seeks to achieve balance and harmony within themselves and the world."
"Rosicrucians see the spirit of the rose as a divine force, representing the spiritual blossoming of the soul toward its highest potential."
"In Rosicrucian teachings, the book of nature is considered the divine scripture that contains the truths of the cosmos, waiting to be deciphered."
"The Rosicrucian path of initiation is seen as a gradual unfolding of the soul's potential, where each step brings the seeker closer to divine wisdom."
"Rosicrucians teach that the universe is a reflection of divine will, and through spiritual practices, one can align with the cosmic plan."
"The labors of Hercules are interpreted in Rosicrucian teachings as allegories for the trials and challenges faced by the soul on its journey of spiritual awakening."
]

def format_fact(fact):
    """Format the fact with 'Energy Fact:' prefix"""
    return f"Energy Fact: {fact}"

def get_fact():
    """Get a random formatted fact"""
    try:
        return format_fact(random.choice(facts))
    except Exception as e:
        print(f"Error generating fact: {e}")
        return None

def post_tweet():
    """Post a tweet with error handling"""
    tweet_content = get_fact()
    if tweet_content:
        try:
            # Using Twitter API v2 endpoint
            response = client.create_tweet(text=tweet_content)
            if response.data:
                print("\n✅ Tweet posted successfully:")
                print("-" * 50)
                print(tweet_content)
                print("-" * 50)
            else:
                print("❌ No response data received from Twitter")
        except tweepy.TweepyException as e:
            print(f"❌ Twitter API Error: {e}")
    else:
        print("❌ Could not generate tweet content")

def schedule_tweets():
    """Schedule tweets at specified times"""
    # Set timezone to West African Time
    wat = pytz.timezone('Africa/Lagos')

    # Schedule tweets at specified times
    schedule.every().day.at("09:00").do(post_tweet).tag('scheduled-tweet')
    schedule.every().day.at("12:00").do(post_tweet).tag('scheduled-tweet')
    schedule.every().day.at("15:00").do(post_tweet).tag('scheduled-tweet')
    schedule.every().day.at("18:00").do(post_tweet).tag('scheduled-tweet')
    schedule.every().day.at("21:00").do(post_tweet).tag('scheduled-tweet')

    print(f"🤖 Bot Started")
    print(f"⏱️ Scheduled times: 9 AM, 12 PM, 3 PM, 6 PM, 9 PM (WAT)")
    print("-" * 50)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second for pending tasks

if __name__ == "__main__":
    schedule_tweets()