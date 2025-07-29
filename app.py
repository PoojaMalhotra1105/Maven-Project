mport random
from datetime import datetime
from pathlib import Path
import base64

# Set page config
st.set_page_config(
    page_title="✨ Amazing Book Discovery",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for an amazing looking app
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes shimmer {
        0% { background-position: -200px 0; }
        100% { background-position: calc(200px + 100%) 0; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .stSidebar {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        backdrop-filter: blur(20px);
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: shimmer 2s infinite;
    }
    
    .sidebar-brand {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .sidebar-subtitle {
        font-size: 0.9rem;
        color: #ffffff;
        font-weight: 400;
        opacity: 0.95;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
    }
    
    .navigation-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .nav-title {
        color: #667eea;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .amazing-book-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .amazing-book-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 300% 100%;
        animation: gradientShift 3s ease infinite;
    }
    
    .amazing-book-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .compact-amazing-card {
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(15px);
        padding: 1.2rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 6px 30px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.4s ease-out;
    }
    
    .compact-amazing-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #f5576c);
        background-size: 200% 100%;
        animation: gradientShift 4s ease infinite;
    }
    
    .compact-amazing-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }
    
    .ultra-compact-amazing-card {
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(12px);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.5);
        transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .ultra-compact-amazing-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #764ba2, #f093fb);
        background-size: 150% 100%;
        animation: gradientShift 5s ease infinite;
    }
    
    .ultra-compact-amazing-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .amazing-empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        margin: 2rem 0;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .amazing-empty-state::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe);
        background-size: 400% 100%;
        animation: gradientShift 6s ease infinite;
    }
    
    .amazing-empty-state h3 {
        color: #667eea;
        font-weight: 600;
        margin-bottom: 1.5rem;
        font-size: 1.6rem;
    }
    
    .amazing-empty-state p {
        color: #64748b;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .amazing-stat {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        padding: 1.2rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    .amazing-stat:hover {
        transform: translateY(-4px);
        animation: pulse 2s infinite;
    }
    
    .stat-number {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .recent-amazing-book {
        color: #64748b;
        font-size: 0.8rem;
        margin-bottom: 0.6rem;
        padding: 0.6rem;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .recent-amazing-book:hover {
        transform: translateX(4px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    }
    
    .amazing-recommendation {
        background: rgba(255, 255, 255, 0.96);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    .amazing-recommendation:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
    }
    
    .amazing-genre-tag {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 25px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.2rem;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: transform 0.2s ease;
    }
    
    .amazing-genre-tag:hover {
        transform: translateY(-2px);
    }
    
    .amazing-book-cover {
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
        border: 2px solid rgba(255, 255, 255, 0.5);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        overflow: hidden;
    }
    
    .amazing-book-cover:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
    }
    
    .amazing-placeholder {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        text-align: center;
        padding: 8px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .amazing-placeholder::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    .amazing-placeholder:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    .book-title {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.3rem;
        line-height: 1.3;
    }
    
    .book-author {
        color: #64748b;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }
    
    .book-details {
        color: #64748b;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    
    .search-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 25px;
        padding: 0.4rem 1rem;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stProgress .stProgress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 200% 100%;
        animation: gradientShift 2s ease infinite;
    }
    
    /* Enhanced input styles */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
        padding: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
    }
    
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 12px;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Page header styling */
    .page-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .page-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
        animation: fadeInUp 1s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'books_df' not in st.session_state:
    st.session_state.books_df = pd.DataFrame()
if 'summer_reading_list' not in st.session_state:
    st.session_state.summer_reading_list = []
if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = False

# File to store summer reading list
SUMMER_LIST_FILE = 'summer_reading_list.json'

# Summer genre recommendations and emoji mapping
summer_genre_icons = {
    "Romance": "💕", "Adventure": "🏖️", "Mystery": "🕵️", "Fantasy": "🧚", 
    "Science Fiction": "🚀", "Historical Fiction": "🏛️", "Contemporary": "🌻", 
    "Thriller": "⚡", "Young Adult": "🌅", "Comedy": "😎", "Travel": "✈️",
    "Memoir": "📖", "Self-Help": "🌱", "Biography": "👤", "Literary Fiction": "📚",
    "Beach Read": "🏖️", "Light Fiction": "☀️", "Escapist": "🌴", "Feel-Good": "🌈"
}

def load_sample_summer_data():
    """Load sample summer reading data"""
    summer_books = {
        'title': [
            'Beach Read', 'The Seven Husbands of Evelyn Hugo', 'Where the Crawdads Sing', 
            'The Summer I Turned Pretty', 'It Ends with Us', 'The Midnight Library',
            'Project Hail Mary', 'Klara and the Sun', 'The Invisible Life of Addie LaRue',
            'The Guest List', 'Malibu Rising', 'The Sanatoriums', 'The Thursday Murder Club',
            'Educated', 'Atomic Habits', 'Becoming', 'The Alchemist', 'Big Little Lies',
            'Gone Girl', 'The Girl on the Train'
        ],
        'author': [
            'Emily Henry', 'Taylor Jenkins Reid', 'Delia Owens', 'Jenny Han', 
            'Colleen Hoover', 'Matt Haig', 'Andy Weir', 'Kazuo Ishiguro',
            'V.E. Schwab', 'Lucy Foley', 'Taylor Jenkins Reid', 'Sarah Pearse',
            'Richard Osman', 'Tara Westover', 'James Clear', 'Michelle Obama',
            'Paulo Coelho', 'Liane Moriarty', 'Gillian Flynn', 'Paula Hawkins'
        ],
        'year': [
            2020, 2017, 2018, 2009, 2016, 2020, 2021, 2021, 2020, 2020,
            2021, 2021, 2020, 2018, 2018, 2018, 1988, 2014, 2012, 2015
        ],
        'average_rating': [
            4.05, 4.25, 4.41, 4.20, 4.30, 4.15, 4.52, 4.01, 4.28, 4.01,
            3.95, 3.91, 4.26, 4.47, 4.34, 4.44, 3.88, 4.05, 4.08, 3.88
        ],
        'genre': [
            'Romance', 'Contemporary', 'Literary Fiction', 'Young Adult',
            'Romance', 'Literary Fiction', 'Science Fiction', 'Literary Fiction',
            'Fantasy', 'Mystery', 'Contemporary', 'Thriller', 'Mystery',
            'Memoir', 'Self-Help', 'Biography', 'Philosophy', 'Contemporary',
            'Thriller', 'Mystery'
        ],
        'summer_appeal': [
            'Perfect beach read with romance and humor',
            'Glamorous Hollywood story, great for poolside',
            'Beautiful nature writing, atmospheric',
            'Coming-of-age summer romance classic',
            'Emotional contemporary romance',
            'Thought-provoking yet accessible',
            'Fun space adventure with humor',
            'Gentle literary fiction',
            'Magical historical fantasy',
            'Gripping thriller set on an island',
            'Family drama set in Malibu',
            'Atmospheric thriller in the Alps',
            'Cozy British mystery series',
            'Inspiring memoir about education',
            'Practical self-improvement',
            'Inspiring political memoir',
            'Philosophical journey story',
            'Domestic drama with dark secrets',
            'Psychological thriller page-turner',
            'Suspenseful domestic thriller'
        ]
    }
    return pd.DataFrame(summer_books)

def load_data():
    """Load book data from CSV or create sample summer data"""
    try:
        possible_files = [
            'books.csv', 'book_data.csv', 'library.csv', 'goodbooks.csv',
            'goodreads_works 2.csv', 'maven_books_dataset.csv', 'bookshelf.csv', 'maven_bookshelf.csv'
        ]
        
        for filename in possible_files:
            if Path(filename).exists():
                df = pd.read_csv(filename)
                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
                
                column_mapping = {
                    'original_title': 'title',
                    'avg_rating': 'average_rating', 
                    'original_publication_year': 'year',
                    'genres': 'genre'
                }
                
                for old_name, new_name in column_mapping.items():
                    if old_name in df.columns:
                        df.rename(columns={old_name: new_name}, inplace=True)
                
                df.dropna(subset=['title'], inplace=True)
                if 'author' in df.columns:
                    df.dropna(subset=['author'], inplace=True)
                
                return df
        
        st.info("📝 No CSV file found. Using curated summer reading recommendations.")
        return load_sample_summer_data()
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("Using sample summer reading data instead.")
        return load_sample_summer_data()

def load_summer_list():
    """Load summer reading list from JSON file"""
    if os.path.exists(SUMMER_LIST_FILE):
        try:
            with open(SUMMER_LIST_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_summer_list():
    """Save summer reading list to JSON file"""
    with open(SUMMER_LIST_FILE, 'w') as f:
        json.dump(st.session_state.summer_reading_list, f, indent=2)

def parse_genres(genre_data):
    """Parse genre data into a list of individual genres"""
    if pd.isna(genre_data) or genre_data == '' or genre_data is None:
        return ['Contemporary']
    
    genre_str = str(genre_data).strip()
    
    if not genre_str or genre_str.lower() in ['unknown', 'n/a', 'none', 'nan']:
        return ['Contemporary']
    
    # Handle different separators
    separators = [',', ';', '|', '\n', '/', '&', ' and ', ' & ', ' - ']
    current_genres = [genre_str]
    
    for sep in separators:
        new_genres = []
        for item in current_genres:
            if sep in item:
                parts = item.split(sep)
                for part in parts:
                    cleaned_part = part.strip()
                    if cleaned_part:
                        new_genres.append(cleaned_part)
            else:
                new_genres.append(item)
        current_genres = new_genres
    
    # Clean up genres
    clean_genres = []
    for genre in current_genres:
        clean_genre = genre.strip().strip('"').strip("'").strip('[]').strip('()').strip()
        clean_genre = clean_genre.replace('_', ' ').title()
        
        if (clean_genre and 
            len(clean_genre) > 1 and
            clean_genre.lower() not in ['unknown', 'n/a', 'none', 'nan', 'null', '', ' '] and
            not clean_genre.isdigit()):
            clean_genres.append(clean_genre)
    
    return clean_genres if clean_genres else ['Contemporary']

def get_summer_appeal_score(book):
    """Calculate summer appeal score based on genre and rating"""
    genre_data = book.get('genre', 'Contemporary')
    parsed_genres = parse_genres(genre_data)
    rating = book.get('average_rating', 3.5)
    
    # Summer-friendly genres get bonus points
    summer_friendly_genres = [
        'Romance', 'Contemporary', 'Adventure', 'Mystery', 'Young Adult',
        'Comedy', 'Travel', 'Self-Help', 'Biography', 'Light Fiction'
    ]
    
    genre_bonus = 0
    for genre in parsed_genres:
        if any(summer_genre in genre for summer_genre in summer_friendly_genres):
            genre_bonus += 0.5
    
    base_score = float(rating) if pd.notna(rating) else 3.5
    return min(5.0, base_score + genre_bonus)

def display_summer_book_card(book, show_add_button=True, compact=False, show_remove_button=False):
    """Display a summer-themed book card with cover image"""
    genre_data = book.get('genre', 'Contemporary')
    parsed_genres = parse_genres(genre_data)
    
    # Get summer appeal description
    summer_appeal = book.get('summer_appeal', 'Great for summer reading')
    
    if parsed_genres and parsed_genres != ['Contemporary']:
        genre_display = " ".join([summer_genre_icons.get(g, "📚") + " " + g for g in parsed_genres[:2]])
    else:
        genre_display = "📚 Contemporary"
    
    if compact:
        card_class = "ultra-compact-amazing-card"
    else:
        card_class = "amazing-book-card"
    
    with st.container():
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        
        # Create columns for image and content
        if show_add_button or show_remove_button:
            col_image, col_info, col_action = st.columns([1, 4, 1])
        else:
            col_image, col_info = st.columns([1, 5])
            col_action = None
        
        # Book cover image
        with col_image:
            # Try to get book cover image
            title = str(book.get('title', 'Unknown Title'))
            author = str(book.get('author', 'Unknown Author'))
            
            # Check for existing image URL in data (try multiple possible column names)
            image_url = None
            possible_image_columns = ['image_url', 'cover_image', 'thumbnail', 'small_image_url', 'image', 'cover_url', 'book_image']
            
            for col in possible_image_columns:
                if col in book and book.get(col) and str(book.get(col)) not in ['nan', 'None', '', 'null']:
                    image_url = str(book.get(col)).strip()
                    break
            
            # Try to display the image
            image_displayed = False
            if image_url:
                try:
                    # Enhanced image display with better styling
                    st.markdown(f"""
                    <div class="amazing-book-cover" style="width: 80px; height: 120px; margin-bottom: 8px;">
                        <img src="{image_url}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 12px;" 
                             onerror="this.style.display='none'" 
                             alt="Book cover for {title}">
                    </div>
                    """, unsafe_allow_html=True)
                    image_displayed = True
                except Exception as e:
                    # If image fails, we'll show placeholder below
                    image_displayed = False
            
            # Show placeholder if no image or image failed
            if not image_displayed:
                # Create a beautiful placeholder with book info
                clean_title = title[:15] + "..." if len(title) > 15 else title
                clean_author = author[:12] + "..." if len(author) > 12 else author
                
                # Get genre for color theming
                genre_data = book.get('genre', 'Contemporary')
                parsed_genres = parse_genres(genre_data)
                main_genre = parsed_genres[0] if parsed_genres else 'Contemporary'
                
                # Enhanced placeholder with genre-based styling
                st.markdown(f"""
                <div class="amazing-placeholder" style="width: 80px; height: 120px; position: relative;">
                    <div style="font-size: 1.5rem; margin-bottom: 6px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">📚</div>
                    <div style="line-height: 1.1; overflow: hidden; word-wrap: break-word; font-size: 0.6rem; font-weight: 700; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">{clean_title}</div>
                    <div style="font-size: 0.45rem; margin-top: 4px; opacity: 0.9; font-weight: 500;">by {clean_author}</div>
                    <div style="position: absolute; top: 4px; right: 4px; font-size: 0.5rem; opacity: 0.7;">{summer_genre_icons.get(main_genre, "📖")}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_info:
            display_title = title if len(title) <= 60 else title[:57] + "..."
            st.markdown(f'<div class="book-title" style="font-size: 1rem; margin-bottom: 0.2rem; color: #1e293b;">{display_title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="book-author" style="font-size: 0.8rem; margin-bottom: 0.2rem; color: #64748b;">by {author}</div>', unsafe_allow_html=True)
            
            rating = book.get('average_rating', 0)
            year = book.get('year', 'Unknown')
            
            if pd.notna(rating) and rating > 0:
                rating_display = f"⭐ {float(rating):.1f}"
                summer_score = get_summer_appeal_score(book)
                if summer_score >= 4.0:
                    rating_display += " ☀️"
            else:
                rating_display = "⭐ N/A"
            
            if pd.notna(year) and year != 'Unknown':
                try:
                    year_val = int(float(year))
                    year_display = str(year_val)
                except:
                    year_display = "Unknown"
            else:
                year_display = "Unknown"
            
            st.markdown(f'<div class="book-details" style="font-size: 0.75rem; margin-bottom: 0.3rem; color: #64748b;">{rating_display} • {year_display} • {genre_display}</div>', unsafe_allow_html=True)
            
            if summer_appeal and not compact:
                st.markdown(f'<div style="font-size: 0.7rem; color: #FF8C00; font-style: italic; margin-top: 0.3rem;">☀️ {summer_appeal}</div>', unsafe_allow_html=True)
        
        if col_action:
            with col_action:
                if show_add_button:
                    book_id = book.get('work_id', f"{title}_{author}")
                    book_exists = any(book.get('work_id') == book_id or 
                                    (book['title'] == title and book['author'] == author) 
                                    for book in st.session_state.summer_reading_list)
                    
                    if not book_exists:
                        if st.button("➕", key=f"add_{book_id}", type="secondary", help="Add to Summer List"):
                            new_book = {
                                'id': len(st.session_state.summer_reading_list) + 1,
                                'work_id': book_id,
                                'title': title,
                                'author': author,
                                'genre': book.get('genre', 'Contemporary'),
                                'rating': int(float(rating)) if pd.notna(rating) and rating > 0 else 4,
                                'average_rating': float(rating) if pd.notna(rating) else None,
                                'year': year,
                                'summer_appeal': summer_appeal,
                                'image_url': image_url,  # Save image URL to reading list
                                'date_added': datetime.now().strftime("%Y-%m-%d"),
                                'source': 'recommendations'
                            }
                            st.session_state.summer_reading_list.append(new_book)
                            save_summer_list()
                            st.success(f"Added '{title}' to your summer reading list! ☀️")
                            st.rerun()
                    else:
                        st.markdown("✅")
                
                elif show_remove_button:
                    book_id = book.get('work_id', f"{title}_{author}")
                    if st.button("🗑️", key=f"remove_{book_id}", type="secondary", help="Remove from Summer List"):
                        st.session_state.summer_reading_list = [
                            b for b in st.session_state.summer_reading_list
                            if not (b.get('work_id', f"{b['title']}_{b['author']}") == book_id)
                        ]
                        save_summer_list()
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def discover_summer_books():
    """Discover summer reading recommendations"""
    
    # Amazing page header
    st.markdown("""
    <div class="page-header">
        <div class="page-title">✨ Discover Amazing Books</div>
        <div class="page-subtitle">Find your next incredible reading adventure</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.books_df.empty:
        st.warning("📚 No book collection available. Please ensure your dataset file is in the project directory.")
        return
    
    df = st.session_state.books_df.copy()
    df['summer_score'] = df.apply(get_summer_appeal_score, axis=1)
    
    # Apply filters first to get total results for pagination
    filtered_df = df.copy()
    
    # Get filter values (we'll display them after the header)
    search_term = ""
    selected_author = 'All Authors'
    min_rating = 3.5
    min_summer_score = 3.5
    
    # Pre-calculate results for pagination
    recommended_df = filtered_df.sort_values('summer_score', ascending=False)
    total_results = len(recommended_df)
    
    # Header with title and pagination
    header_col1, header_col2 = st.columns([2, 1])
    
    with header_col1:
        st.markdown("### ☀️ Discover Summer Books")
    
    with header_col2:
        # Pagination controls next to title
        books_per_page = 50  # Fixed at 50 books per page
        page_number = 1  # Default page
        
        if total_results > books_per_page:
            # Calculate total pages
            total_pages = (total_results - 1) // books_per_page + 1
            
            # Page selector next to title
            page_number = st.selectbox("📄 Page", 
                                       options=list(range(1, total_pages + 1)), 
                                       index=0,
                                       key="page_selector")
    
    # Search and filter section with amazing styling
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Main search bar
    search_term = st.text_input("🔍 Search books, authors, or genres", placeholder="Try 'romance', 'mystery', or your favorite author...", key="search_input")
    
    # Filters in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Author filter
        if 'author' in df.columns:
            authors_list = ['All Authors'] + sorted(df['author'].dropna().unique().tolist())
            selected_author = st.selectbox("👤 Author", authors_list, key="author_filter")
        else:
            selected_author = 'All Authors'
    
    with col2:
        # Rating filter
        if 'average_rating' in df.columns:
            min_rating = st.slider("⭐ Min Rating", 1.0, 5.0, 3.5, step=0.1, key="rating_filter")
        else:
            min_rating = 1.0
    
    with col3:
        # Summer appeal filter
        min_summer_score = st.slider("✨ Reading Appeal", 1.0, 5.0, 3.5, step=0.1, key="summer_score_filter")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    # Search filter
    if search_term and search_term.strip():
        search_mask = (
            filtered_df['title'].str.contains(search_term, case=False, na=False) |
            filtered_df['author'].str.contains(search_term, case=False, na=False) |
            filtered_df['genre'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[search_mask]
    
    # Author filter
    if selected_author != 'All Authors':
        filtered_df = filtered_df[filtered_df['author'] == selected_author]
    
    # Rating filter
    if 'average_rating' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['average_rating'] >= min_rating]
    
    # Summer appeal filter
    filtered_df = filtered_df[filtered_df['summer_score'] >= min_summer_score]
    
    # Sort by summer score
    recommended_df = filtered_df.sort_values('summer_score', ascending=False)
    
    # Show default recommendations if no filters applied
    if not search_term and selected_author == 'All Authors' and min_rating <= 3.5 and min_summer_score <= 3.5:
        # Show all books sorted by summer score instead of limiting to 25
        recommended_df = df.sort_values('summer_score', ascending=False)
    
    # Update total results after filtering
    total_results = len(recommended_df)
    
    # Display results
    if total_results == 0:
        st.warning("🔍 No books match your current filters. Try adjusting your search criteria.")
        return
    
    # Calculate pagination after filtering
    if total_results > books_per_page:
        # Calculate start and end indices
        start_idx = (page_number - 1) * books_per_page
        end_idx = min(start_idx + books_per_page, total_results)
        
        # Show books for current page
        page_books = recommended_df.iloc[start_idx:end_idx]
        
        # Show pagination info
        st.caption(f"📚 Showing {start_idx + 1}-{end_idx} of {total_results} books")
    else:
        page_books = recommended_df
        st.caption(f"📚 Showing all {total_results} books")
    
    # Display recommendations
    for _, book in page_books.iterrows():
        display_summer_book_card(book, show_add_button=True, compact=True)

def display_summer_reading_list():
    """Display and manage the summer reading list"""
    
    # Amazing page header
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🏖️ My Reading Collection</div>
        <div class="page-subtitle">Your curated library of amazing books</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.summer_reading_list:
        st.markdown("""
        <div class="amazing-empty-state">
            <h3>☀️ Your summer reading adventure awaits!</h3>
            <p>Start building your perfect summer reading list by discovering books that match your mood and interests.</p>
            <p>🌅 Head over to 'Discover Summer Books' to find your next great read!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    summer_books_df = pd.DataFrame(st.session_state.summer_reading_list)

    # Summer reading stats
    total_books = len(summer_books_df)
    avg_rating = summer_books_df['rating'].mean() if not summer_books_df.empty else 0
    unique_authors = summer_books_df['author'].nunique() if 'author' in summer_books_df.columns else 0
    
    # Calculate reading goal progress
    summer_goal = st.sidebar.number_input("📚 Summer Reading Goal", min_value=1, max_value=50, value=10, key="summer_goal_input")
    progress = min(100, (total_books / summer_goal) * 100)
    
    # Display stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="amazing-stat">
            <div class="stat-number">{total_books}</div>
            <div class="stat-label">Books Added</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="amazing-stat">
            <div class="stat-number">{avg_rating:.1f}⭐</div>
            <div class="stat-label">Avg Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="amazing-stat">
            <div class="stat-number">{unique_authors}</div>
            <div class="stat-label">Authors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="amazing-stat">
            <div class="stat-number">{progress:.0f}%</div>
            <div class="stat-label">Goal Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress / 100)
    st.caption(f"🎯 {total_books} of {summer_goal} books added to your summer list")
    
    st.markdown("---")

    # Filters for the list
    col1, col2 = st.columns(2)
    with col1:
        search_summer_books = st.text_input("Search your summer list", placeholder="Title or author...", key="search_list_input")
    with col2:
        min_rating = st.slider("Minimum Rating", 1, 5, 1, key="min_rating_filter")

    # Apply filters to summer list
    filtered_books = summer_books_df.copy()
    if search_summer_books:
        mask = (
            filtered_books['title'].str.contains(search_summer_books, case=False, na=False) |
            filtered_books['author'].str.contains(search_summer_books, case=False, na=False)
        )
        filtered_books = filtered_books[mask]
    
    filtered_books = filtered_books[filtered_books['rating'] >= min_rating]

    # Display summer reading list
    st.markdown("### 📚 Your Curated Summer Collection")
    
    if len(filtered_books) == 0:
        st.info("🔍 No books match your filters. Try adjusting your search.")
        return
    
    # Group by genre for better organization
    genre_groups = {}
    for idx, book in filtered_books.iterrows():
        genre_data = book.get('genre', 'Contemporary')
        parsed_genres = parse_genres(genre_data)
        main_genre = parsed_genres[0] if parsed_genres else 'Contemporary'
        
        if main_genre not in genre_groups:
            genre_groups[main_genre] = []
        genre_groups[main_genre].append(book)
    
    # Display by genre sections
    for genre, books in genre_groups.items():
        genre_icon = summer_genre_icons.get(genre, "📚")
        st.markdown(f"#### {genre_icon} {genre} ({len(books)} book{'s' if len(books) != 1 else ''})")
        
        for book in books:
            display_summer_book_card(book, show_add_button=False, show_remove_button=True, compact=True)

def show_summer_insights():
    """Show summer reading insights and recommendations"""
    
    # Amazing page header
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📊 Reading Analytics</div>
        <div class="page-subtitle">Discover insights about your reading journey</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset analytics for summer reading
    if not st.session_state.books_df.empty:
        st.markdown("#### 🌞 Summer Reading Trends")
        df = st.session_state.books_df.copy()
        
        # Calculate summer appeal scores for all books
        df['summer_score'] = df.apply(get_summer_appeal_score, axis=1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Most summer-friendly genres
            genre_summer_scores = {}
            for _, row in df.iterrows():
                genre_data = row['genre']
                parsed_genres = parse_genres(genre_data)
                summer_score = row['summer_score']
                
                for genre in parsed_genres:
                    if genre not in genre_summer_scores:
                        genre_summer_scores[genre] = []
                    genre_summer_scores[genre].append(summer_score)
            
            # Calculate average summer scores by genre
            avg_genre_scores = {
                genre: sum(scores) / len(scores) 
                for genre, scores in genre_summer_scores.items() 
                if len(scores) >= 3  # Only include genres with at least 3 books
            }
            
            if avg_genre_scores:
                st.markdown("##### 🏖️ Best Summer Genres")
                sorted_genres = sorted(avg_genre_scores.items(), key=lambda x: x[1], reverse=True)[:8]
                genre_chart_data = pd.DataFrame(sorted_genres, columns=['Genre', 'Summer Appeal Score'])
                st.bar_chart(genre_chart_data.set_index('Genre')['Summer Appeal Score'])
        
        with col2:
            # Summer reading recommendations by rating
            st.markdown("##### ⭐ Highly Rated Summer Books")
            top_summer_books = df[df['summer_score'] >= 4.2].nlargest(10, 'average_rating')
            
            if not top_summer_books.empty:
                for _, book in top_summer_books.head(5).iterrows():
                    genre_data = book.get('genre', 'Contemporary')
                    parsed_genres = parse_genres(genre_data)
                    genre_display = parsed_genres[0] if parsed_genres else 'Contemporary'
                    
                    st.markdown(f"""
                    <div class="amazing-recommendation">
                        <strong>{book['title']}</strong><br>
                        <em>by {book['author']}</em><br>
                        <span class="amazing-genre-tag">{genre_display}</span>
                        <span style="color: #667eea;">⭐ {book['average_rating']:.1f}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Personal summer reading analytics
    if st.session_state.summer_reading_list:
        st.markdown("---")
        st.markdown("#### 🏖️ Your Summer Reading Profile")
        summer_books_df = pd.DataFrame(st.session_state.summer_reading_list)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre distribution in summer list
            summer_genres = {}
            for book in st.session_state.summer_reading_list:
                genre_data = book.get('genre', 'Contemporary')
                parsed_genres = parse_genres(genre_data)
                for genre in parsed_genres:
                    summer_genres[genre] = summer_genres.get(genre, 0) + 1
            
            if summer_genres:
                st.markdown("##### 📚 Your Summer Genre Mix")
                summer_genre_df = pd.DataFrame(list(summer_genres.items()), columns=['Genre', 'Count'])
                st.bar_chart(summer_genre_df.set_index('Genre')['Count'])
        
        with col2:
            # Rating distribution
            rating_counts = summer_books_df['rating'].value_counts().sort_index()
            st.markdown("##### ⭐ Your Summer Ratings")
            rating_labels = {1: '1⭐', 2: '2⭐', 3: '3⭐', 4: '4⭐', 5: '5⭐'}
            rating_counts.index = rating_counts.index.map(rating_labels)
            st.bar_chart(rating_counts)
        
        # Summer reading timeline
        summer_books_df['date_added'] = pd.to_datetime(summer_books_df['date_added'])
        books_per_day = summer_books_df.groupby(summer_books_df['date_added'].dt.date).size()
        
        if len(books_per_day) > 1:
            st.markdown("##### 📈 List Building Progress")
            st.line_chart(books_per_day)
        
        # Summer reading recommendations based on preferences
        st.markdown("##### 🌅 Personalized Summer Recommendations")
        
        # Analyze user's genre preferences
        user_favorite_genres = list(summer_genres.keys())[:3] if summer_genres else ['Romance', 'Contemporary']
        
        # Find books that match user preferences but aren't in their list
        if not st.session_state.books_df.empty:
            df = st.session_state.books_df.copy()
            df['summer_score'] = df.apply(get_summer_appeal_score, axis=1)
            
            # Get existing book IDs in summer list
            existing_ids = {book.get('work_id', f"{book['title']}_{book['author']}") for book in st.session_state.summer_reading_list}
            
            # Filter recommendations
            recommendations = []
            for _, book in df.iterrows():
                book_id = book.get('work_id', f"{book['title']}_{book['author']}")
                if book_id not in existing_ids:
                    genre_data = book.get('genre', 'Contemporary')
                    parsed_genres = parse_genres(genre_data)
                    
                    # Check if book matches user's preferred genres
                    genre_match = any(user_genre in genre for user_genre in user_favorite_genres for genre in parsed_genres)
                    
                    if genre_match and book['summer_score'] >= 4.0:
                        recommendations.append(book)
            
            # Sort by summer score and display top 3
            recommendations.sort(key=lambda x: x['summer_score'], reverse=True)
            
            if recommendations:
                st.markdown("Based on your current list, you might enjoy:")
                for book in recommendations[:3]:
                    display_summer_book_card(book, show_add_button=True, compact=True)
            else:
                st.info("🎉 Great selection! You've already found some excellent summer reads.")
        
        # Summer reading tips
        st.markdown("##### 💡 Summer Reading Tips")
        tips = [
            "🏖️ Beach reads should be engaging but not too complex!",
            "📱 Download audiobooks for road trips and walks", 
            "🌙 Keep a shorter book for bedtime reading",
            "☀️ Mix genres to match different summer moods",
            "👥 Join online book clubs for summer discussions"
        ]
        
        for tip in tips:
            st.markdown(f"- {tip}")
    
    else:
        st.markdown("""
        <div class="amazing-empty-state">
            <h3>📊 Start tracking your summer reading!</h3>
            <p>Add books to your summer reading list to see personalized insights and recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application"""
    # Load summer reading list on startup
    if not st.session_state.summer_reading_list:
        st.session_state.summer_reading_list = load_summer_list()
    
    # Auto-load dataset with amazing loading message
    if not st.session_state.loaded_data:
        with st.spinner("✨ Loading your amazing book collection..."):
            st.session_state.books_df = load_data()
            st.session_state.loaded_data = True
    
    # Sidebar with amazing styling
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-brand">✨ Amazing Book Discovery</div>
        <div class="sidebar-subtitle">Curate Your Perfect Reading Collection</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation section
    st.sidebar.markdown("""
    <div class="navigation-section">
        <div class="nav-title">Navigation</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.sidebar.radio("", [
        "Discover Amazing Books", 
        "My Reading Collection", 
        "Reading Analytics"
    ], key="main_nav")
    
    # Show recent additions to summer list
    if st.session_state.summer_reading_list and len(st.session_state.summer_reading_list) > 0:
        st.sidebar.markdown("""
        <div class="navigation-section">
            <div class="nav-title">Recently Added</div>
        </div>
        """, unsafe_allow_html=True)
        recent_books = sorted(st.session_state.summer_reading_list, key=lambda x: x['date_added'], reverse=True)[:3]
        for book in recent_books:
            st.sidebar.markdown(f"""
            <div class="recent-amazing-book">
                ✨ {book['title'][:25]}{'...' if len(book['title']) > 25 else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div class="navigation-section">
            <div class="nav-title">Reading Goals</div>
            <p style='color: #64748b; font-size: 0.75rem; margin: 0.4rem 0; line-height: 1.3;'>
                ✨ Build your perfect reading collection! Discover amazing books that match your mood and interests.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Reading tip of the day
    amazing_tips = [
        "✨ Choose books that spark your curiosity and imagination!",
        "📚 Mix different genres to keep your reading fresh and exciting",
        "⏰ Set achievable reading goals and celebrate your progress",
        "🎧 Audiobooks are perfect for multitasking and commuting",
        "👥 Join online book communities for amazing discussions!",
        "🌟 Keep a reading journal to track your literary journey",
        "📖 Don't be afraid to DNF (Did Not Finish) books that don't click"
    ]
    
    daily_tip = random.choice(amazing_tips)
    st.sidebar.markdown(f"""
    <div class="navigation-section">
        <div class="nav-title">💡 Reading Tip</div>
        <p style='color: #64748b; font-size: 0.75rem; margin: 0.4rem 0; line-height: 1.3; font-style: italic;'>
            {daily_tip}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    if page == "Discover Amazing Books":
        discover_summer_books()
    elif page == "My Reading Collection":
        display_summer_reading_list()
    elif page == "Reading Analytics":
        show_summer_insights()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 0.7rem; background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.9) 100%); backdrop-filter: blur(10px); padding: 12px; border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2); box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1);'>
        <p style='margin: 0; font-weight: 600;'>✨ Amazing Book Discovery</p>
        <p style='margin: 4px 0 0 0; opacity: 0.8;'>Discover your next incredible read!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
