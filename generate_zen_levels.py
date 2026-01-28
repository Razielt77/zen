import json
import random
from collections import Counter
import difflib

# --- CONFIGURATION ---
INPUT_FILE = 'wordlist.txt'
OUTPUT_FILE = 'zen_levels_final.json'
EXTRA_LEVELS_BUFFER = 5 

LEVEL_STRUCTURE = [
    (6, 6, 4),   # Levels 1-4
    (7, 7, 10),   # Levels 5-14
    (8, 8, 12),   # Levels 15-26
    (9, 9, 12),   # Levels 27-38
    (10, 15, 12), # Levels 39-50
]

# --- BLOCKLISTS ---

# 1. Names (The most common ones found in frequency lists)
NAMES = {
    "james", "john", "robert", "michael", "william", "david", "richard",
    "joseph", "thomas", "charles", "christopher", "daniel", "matthew",
    "anthony", "donald", "mark", "paul", "steven", "andrew", "kenneth",
    "joshua", "kevin", "brian", "george", "edward", "ronald", "timothy",
    "jason", "jeffrey", "ryan", "jacob", "gary", "nicholas", "eric",
    "jonathan", "stephen", "larry", "justin", "scott", "brandon", "benjamin",
    "samuel", "frank", "gregory", "raymond", "alexander", "patrick", "jack",
    "dennis", "jerry", "tyler", "aaron", "jose", "adam", "nathan", "henry",
    "douglas", "peter", "kyle", "walter", "ethan", "jeremy", "harold", "keith",
    "christian", "roger", "noah", "gerald", "terry", "sean", "austin", "carl",
    "arthur", "lawrence", "dylan", "jesse", "jordan", "bryan", "billy", "joe",
    "bruce", "gabriel", "logan", "albert", "willie", "alan", "juan", "wayne",
    "elijah", "randy", "roy", "vincent", "ralph", "eugene", "russell", "bobby",
    "mason", "philip", "louis", "mary", "patricia", "jennifer", "linda",
    "elizabeth", "barbara", "susan", "jessica", "sarah", "karen", "nancy",
    "lisa", "margaret", "betty", "sandra", "ashley", "dorothy", "kimberly",
    "emily", "donna", "michelle", "carol", "amanda", "melissa", "deborah",
    "stephanie", "rebecca", "laura", "sharon", "cynthia", "kathleen", "amy",
    "shirley", "angela", "helen", "anna", "brenda", "pamela", "nicole",
    "samantha", "katherine", "emma", "christine", "debra", "rachel",
    "catherine", "carolyn", "janet", "ruth", "maria", "heather", "diane",
    "virginia", "julie", "joyce", "victoria", "olivia", "kelly", "christina",
    "lauren", "joan", "evelyn", "judith", "megan", "cheryl", "andrea",
    "hannah", "martha", "jacqueline", "frances", "gloria", "ann", "teresa",
    "kathryn", "sara", "janice", "jean", "alice", "madison", "julia", "grace",
    "judy", "abigail", "marie", "denise", "beverly", "amber", "theresa",
    "marilyn", "danielle", "diana", "brittany", "natalie", "sophia", "rose",
    "isabella", "alexis", "kayla", "charlotte", "simon", "luke", "phil",
    "harry", "steve", "dave", "mike", "dan", "tom", "chris", "matt"
}

# 2. UK Spellings & Archaic Words
UK_AND_ARCHAIC = {
    "colour", "favour", "honour", "humour", "labour", "neighbour", "rumour",
    "splendour", "behaviour", "harbour", "flavour", "valour", "candour",
    "parlour", "savour", "clamour", "metres", "odour", "rancour", "tumour", "vapour",
    "centre", "fibre", "litre", "metre", "theatre", "lustre", "mitre",
    "spectre", "calibre", "sombre", "meagre", "ochre", "grande", "realty","sceptre",
    "analogue", "catalogue", "dialogue", "monologue", "prologue", "epilogue",
    "travelled", "travelling", "cancelled", "cancelling", "modelling",
    "maiden", "whom", "thy", "thou", "thee", "hath", "shalt", "wilt"
}

# 3. Geography & Bad Vibes (Previous list + additions)
BLOCKLIST = {
    # Places
    "africa", "america", "asia", "europe", "london", "paris", "japan", "china",
    "india", "russia", "spain", "italy", "france", "german", "dutch", "greek",
    "roman", "jewish", "muslim", "christian", "english", "french", "spanish",
    "sweden", "danish", "denmark", "norway", "poland", "polish", "korea",
    "brazil", "mexico", "canada", "sydney", "angeles", "vegas", "miami",
    "dallas", "boston", "chicago", "seattle", "austin", "texas", "jersey",
    "york", "diego", "fran", "cisco", "berlin", "tokyo", "delhi", "cairo",
    "senegal", "ghana", "kenya", "sudan", "congo", "chile", "peru", "cuba",
    "haiti", "fiji", "bali", "guam", "iraq", "iran", "saudi", "arab", "asian",
    "irish", "scottish", "wales", "swiss", "zulu", "thai", "nam", "lanka",
    "naples", "milan", "rome", "venice", "florence", "turin", "genoa",
    "athens", "madrid", "lisbon", "vienn", "prague", "warsaw", "budapest",
    "oslo", "helsinki", "moscow", "kiev", "mumbai", "dubai", "beijing",
    
    # Negative / Adult / Stress
    "murder", "killer", "kill", "death", "dead", "die", "shoot", "gun", "bullet",
    "bomb", "terror", "attack", "fight", "war", "battle", "army", "navy",
    "soldier", "enemy", "victim", "crime", "prison", "jail", "guilty", "felon",
    "thief", "steal", "robber", "drug", "abuse", "slave", "racist", "nazi",
    "rape", "assault", "horror", "panic", "fear", "scare", "fright", "demon",
    "devil", "ghost", "witch", "curse", "blood", "bleed", "wound", "hurt",
    "pain", "injury", "sick", "virus", "cancer", "flu", "plague", "infect",
    "poison", "toxic", "hazard", "danger", "risk", "warn", "threat", "fatal",
    "sex", "sexy", "porn", "nude", "naked", "erotic", "escort", "hooker",
    "strip", "lust", "orgy", "penis", "vagina", "condom", "sperm", "fetish",
    "kinky", "whore", "slut", "bitch", "bastard", "damn", "hell", "crap",
    "money", "tax", "debt", "loan", "owed", "cost", "price", "loss", "broke",
    "poor", "audit", "fraud", "bribe", "sue", "law", "court", "judge", "trial",
    "legal", "policy", "vote", "elect", "party", "gov", "admin", "senate",
    "congress", "mayor", "leader", "chief", "boss", "manager", "work", "job",
    "career", "hiring", "fired", "layoff", "strike", "union", "wages", "salary",
    "office", "desk", "file", "report", "deadline", "urgent", "stress", "tension",
    "anxiety", "worry", "grief", "cry", "tear", "sad", "unhappy", "angry",
    "hate", "rage", "fury", "mad", "crazy", "insane", "stupid", "idiot", "dumb",
    "fool", "fail", "lose", "defeat", "reject", "denial", "refuse", "blame",
    "fault", "mistake", "error", "wrong", "bad", "evil", "sin", "master"
    "terrorism", "terrorist", "bomber", "sniper", "violent", "violence"
}

def get_word_set(filename):
    with open(filename, 'r') as f:
        # Filter: lowercase, alpha only, at least 3 chars
        words = set(line.strip().lower() for line in f if line.strip().isalpha() and len(line.strip()) >= 3)
    return words

def is_simple_plural(word, all_words):
    if word.endswith('s'):
        singular = word[:-1]
        if singular in all_words:
            return True
    return False

def get_subwords(target, all_words):
    target_counter = Counter(target)
    subwords = []
    for candidate in all_words:
        if candidate == target: continue 
        if len(candidate) < 3: continue
        
        # --- THE MASTER FILTER ---
        if candidate in BLOCKLIST: continue
        if candidate in NAMES: continue
        if candidate in UK_AND_ARCHAIC: continue
        
        candidate_counter = Counter(candidate)
        if all(candidate_counter[char] <= target_counter[char] for char in candidate_counter):
            subwords.append(candidate)
    return subwords

def is_too_similar(word1, word2):
    if not word1 or not word2: return False
    if word1[0] == word2[0]: return True
    ratio = difflib.SequenceMatcher(None, word1, word2).ratio()
    return ratio > 0.75

def scramble_word(word):
    # Convert string to list: "CAT" -> ['C', 'A', 'T']
    char_list = list(word)
    
    # Shuffle the list "in place"
    random.shuffle(char_list)
    
    # Join the list back into a string
    return "".join(char_list)

def generate_zen():
    print("🌱 Reading dictionary...")
    try:
        all_words = get_word_set(INPUT_FILE)
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{INPUT_FILE}'.")
        return

    final_levels = []
    used_targets = set()
    
    print("🧘 Generating US-Only Zen Levels (+5 buffer)...")
    
    for min_len, max_len, desired_count in LEVEL_STRUCTURE:
        target_count = desired_count + EXTRA_LEVELS_BUFFER
        print(f"   -> Aiming for {target_count} levels (Tier: {min_len}-{max_len} letters)...")
        
        candidates = [w for w in all_words if min_len <= len(w) <= max_len]
        print(f"      Found {len(candidates)} candidate words of length {min_len}-{max_len}.")
        
        #for candidate in candidates:
        #    print(f"         Candidate: {candidate}")

        random.shuffle(candidates)
        
        levels_added_for_tier = 0
        
        for target in candidates:
            if levels_added_for_tier >= target_count:
                break
            
            # --- AGGRESSIVE FILTERS ---
            if target in used_targets: continue
            if target in BLOCKLIST: continue
            if target in NAMES: continue
            if target in UK_AND_ARCHAIC: continue
            if is_simple_plural(target, all_words): continue
            
            previous_word = final_levels[-1]['target'].lower() if final_levels else None
            if is_too_similar(target, previous_word): continue

            # --- SUBWORD CHECK ---
            valid_subwords = get_subwords(target, all_words)
            
            # Difficulty scaling
            min_subwords = 5
            if min_len >= 9: min_subwords = 8 
            
            if len(valid_subwords) < min_subwords: continue
            
            final_levels.append({
                "id": len(final_levels) + 1,
                "tier": f"{len(target)}-letters",
                "target": target.upper(),
                "letters": scramble_word(target.upper()),
                "answers": [w.upper() for w in valid_subwords]
            })
            
            used_targets.add(target)
            levels_added_for_tier += 1
            print(f"      [{len(final_levels)}] Found: {target.upper()}")

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(final_levels, f, indent=2)
    
    print(f"\n✨ Done! Generated {len(final_levels)} levels in {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_zen()