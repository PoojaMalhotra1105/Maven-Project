import streamlit as st
import pandas as pd
import json
import os
import random
from datetime import datetime
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="☀️ Summer Reading List Builder",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for summer reading theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FFB347 0%, #FFD700 50%, #FFA500 100%);
    }
    
    .stSidebar {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #FF7043 0%, #FFB347 100%);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 15px rgba(255, 112, 67, 0.3);
    }
    
    .sidebar-brand {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .sidebar-subtitle {
        font-size: 0.85rem;
        color: #ffffff;
        font-weight: 400;
        opacity: 0.95;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .navigation-section {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(5px);
        padding: 0.6rem;
        border-radius: 10px;
        margin-bottom: 0.4rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .nav-title {
        color: #FF7043;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .summer-book-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(255, 112, 67, 0.2);
        border-left: 4px solid #FFB347;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .summer-book-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 112, 67, 0.3);
    }
    
    .compact-summer-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        box-shadow: 0 3px 12px rgba(255, 112, 67, 0.2);
        border: 1px solid rgba(255, 180, 71, 0.3);
        border-left: 4px solid #FF7043;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .compact-summer-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(255, 112, 67, 0.3);
    }
    
    .ultra-compact-summer-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 0.5rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(255, 112, 67, 0.15);
        border: 1px solid rgba(255, 180, 71, 0.2);
        border-left: 3px solid #FFB347;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
    }
    
    .ultra-compact-summer-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 112, 67, 0.25);
    }
    
    .summer-empty-state {
        text-align: center;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 248, 220, 0.95) 100%);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(255, 140, 0, 0.2);
        border: 2px solid rgba(255, 165, 0, 0.3);
        border-top: 4px solid #FFB347;
    }
    
    .summer-empty-state h3 {
        color: #FF7043;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    
    .summer-empty-state p {
        color: #5D4037;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .summer-stat {
        background: linear-gradient(135deg, rgba(255, 248, 220, 0.9) 0%, rgba(255, 235, 205, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255, 165, 0, 0.3);
        box-shadow: 0 3px 10px rgba(255, 140, 0, 0.2);
    }
    
    .stat-number {
        color: #FF7043;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .stat-label {
        color: #8D6E63;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    .recent-summer-book {
        color: #5D4037;
        font-size: 0.75rem;
        margin-bottom: 0.4rem;
        padding: 0.4rem;
        background: linear-gradient(135deg, rgba(255, 248, 220, 0.8) 0%, rgba(255, 235, 205, 0.8) 100%);
        backdrop-filter: blur(10px);
        border-radius: 6px;
        border-left: 3px solid #FFB347;
        box-shadow: 0 2px 8px rgba(255, 140, 0, 0.15);
    }
    
    .summer-recommendation {
        background: linear-gradient(135deg, rgba(255, 239, 213, 0.9) 0%, rgba(255, 224, 178, 0.9) 100%);
        border: 2px solid rgba(255, 152, 0, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
    }
    
    .summer-genre-tag {
        background: linear-gradient(135deg, #FFB347 0%, #FFA500 100%);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
        margin: 0.1rem;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(255, 165, 0, 0.3);
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

def generate_summer_appeal(title, author, genre, rating):
    """Generate summer appeal description based on book characteristics"""
    appeal_templates = {
        'Romance': ['Perfect summer romance', 'Heartwarming love story', 'Romantic escapism'],
        'Mystery': ['Gripping page-turner', 'Perfect poolside thriller', 'Engaging mystery'],
        'Fantasy': ['Magical escapism', 'Enchanting fantasy adventure', 'Immersive world-building'],
        'Science Fiction': ['Thought-provoking sci-fi', 'Futuristic adventure', 'Mind-bending concepts'],
        'Historical Fiction': ['Rich historical detail', 'Immersive period setting', 'Captivating historical tale'],
        'Contemporary': ['Relatable modern story', 'Engaging contemporary fiction', 'Perfect light read'],
        'Literary Fiction': ['Beautiful prose', 'Thought-provoking narrative', 'Award-worthy writing'],
        'Thriller': ['Heart-pounding suspense', 'Edge-of-your-seat thriller', 'Addictive page-turner'],
        'Young Adult': ['Coming-of-age story', 'Perfect YA adventure', 'Engaging young adult fiction'],
        'Biography': ['Inspiring life story', 'Fascinating biography', 'Compelling personal journey'],
        'Memoir': ['Personal and moving', 'Inspiring memoir', 'Honest and engaging'],
        'Self-Help': ['Life-changing insights', 'Practical guidance', 'Motivational read']
    }
    
    # Try to match genre with templates
    for genre_key, templates in appeal_templates.items():
        if genre_key.lower() in str(genre).lower():
            base_appeal = random.choice(templates)
            break
    else:
        base_appeal = 'Great for summer reading'
    
    # Add rating-based modifiers
    try:
        rating_val = float(rating) if pd.notna(rating) else 3.5
        if rating_val >= 4.5:
            base_appeal = f"Highly acclaimed - {base_appeal.lower()}"
        elif rating_val >= 4.0:
            base_appeal = f"Popular choice - {base_appeal.lower()}"
    except:
        pass
    
    return base_appeal

def load_sample_summer_data():
    """Load expanded sample summer reading data with more variety"""
    # Expanded dataset with more books across different genres
    summer_books = {
        'title': [
            # Romance & Contemporary
            'Beach Read', 'The Seven Husbands of Evelyn Hugo', 'It Ends with Us', 'The Hating Game',
            'Red, White & Royal Blue', 'The Kiss Quotient', 'Beach House Summer', 'Summer Sisters',
            'The Summer House', 'One Last Stop', 'People We Meet on Vacation', 'Book Lovers',
            
            # Mystery & Thriller
            'Where the Crawdads Sing', 'The Guest List', 'The Sanatorium', 'The Thursday Murder Club',
            'Gone Girl', 'The Girl on the Train', 'Big Little Lies', 'The Woman in the Window',
            'In the Woods', 'The Silent Patient', 'The Girl with the Dragon Tattoo', 'Sharp Objects',
            
            # Fantasy & Sci-Fi
            'The Invisible Life of Addie LaRue', 'Project Hail Mary', 'Klara and the Sun', 'The Midnight Library',
            'The Seven Moons of Maali Almeida', 'Station Eleven', 'The Time Traveler\'s Wife', 'Circe',
            'The Night Circus', 'The Priory of the Orange Tree', 'The Fifth Season', 'Dune',
            
            # Young Adult
            'The Summer I Turned Pretty', 'The Cruel Prince', 'Six of Crows', 'The Hate U Give',
            'Eleanor Oliphant Is Completely Fine', 'Me Before You', 'The Fault in Our Stars', 'To All the Boys I\'ve Loved Before',
            
            # Literary Fiction
            'Normal People', 'Educated', 'Becoming', 'The Alchemist', 'A Man Called Ove',
            'The Kite Runner', 'Life of Pi', 'The Book Thief', 'The Help', 'Little Fires Everywhere',
            
            # Historical Fiction
            'The Nightingale', 'All the Light We Cannot See', 'Pachinko', 'The Pillars of the Earth',
            'Outlander', 'The English Patient', 'Cold Mountain', 'The Other Boleyn Girl',
            
            # Non-Fiction
            'Atomic Habits', 'Sapiens', 'Wild', 'Untamed',
            'Maybe You Should Talk to Someone', 'The Body Keeps the Score', 'Thinking, Fast and Slow'
        ],
        'author': [
            # Corresponding authors
            'Emily Henry', 'Taylor Jenkins Reid', 'Colleen Hoover', 'Sally Thorne',
            'Casey McQuiston', 'Helen Hoang', 'Jennifer Probst', 'Judy Blume',
            'Sarah Morgan', 'Casey McQuiston', 'Emily Henry', 'Emily Henry',
            
            'Delia Owens', 'Lucy Foley', 'Sarah Pearse', 'Richard Osman',
            'Gillian Flynn', 'Paula Hawkins', 'Liane Moriarty', 'A.J. Finn',
            'Tana French', 'Alex Michaelides', 'Stieg Larsson', 'Gillian Flynn',
            
            'V.E. Schwab', 'Andy Weir', 'Kazuo Ishiguro', 'Matt Haig',
            'Shehan Karunatilaka', 'Emily St. John Mandel', 'Audrey Niffenegger', 'Madeline Miller',
            'Erin Morgenstern', 'Samantha Shannon', 'N.K. Jemisin', 'Frank Herbert',
            
            'Jenny Han', 'Holly Black', 'Leigh Bardugo', 'Angie Thomas',
            'Gail Honeyman', 'Jojo Moyes', 'John Green', 'Jenny Han',
            
            'Sally Rooney', 'Tara Westover', 'Michelle Obama', 'Paulo Coelho', 'Fredrik Backman',
            'Khaled Hosseini', 'Yann Martel', 'Markus Zusak', 'Kathryn Stockett', 'Celeste Ng',
            
            'Kristin Hannah', 'Anthony Doerr', 'Min Jin Lee', 'Ken Follett',
            'Diana Gabaldon', 'Michael Ondaatje', 'Charles Frazier', 'Philippa Gregory',
            
            'James Clear', 'Yuval Noah Harari', 'Cheryl Strayed', 'Glennon Doyle',
            'Lori Gottlieb', 'Bessel van der Kolk', 'Daniel Kahneman'
        ],
        'year': [
            # Corresponding years (approximated for variety)
            2020, 2017, 2016, 2016, 2019, 2018, 2021, 1998, 2020, 2021, 2021, 2022,
            2018, 2020, 2021, 2020, 2012, 2015, 2014, 2018, 2007, 2019, 2005, 2006,
            2020, 2021, 2021, 2020, 2022, 2014, 2003, 2011, 2011, 2019, 2015, 1965,
            2009, 2018, 2015, 2017, 2017, 2014, 2012, 2014,
            2018, 2018, 2018, 1988, 2012, 2003, 2001, 2005, 2009, 2017,
            2015, 2014, 2017, 1989, 1991, 1992, 1996, 2001,
            2018, 2011, 2012, 2020, 2019, 2014, 2011
        ],
        'average_rating': [
            # Realistic ratings (3.5-4.8 range)
            4.05, 4.25, 4.30, 4.15, 4.40, 4.20, 3.85, 4.10, 3.95, 4.35, 4.25, 4.18,
            4.41, 4.01, 3.91, 4.26, 4.08, 3.88, 4.05, 3.75, 4.32, 4.28, 4.15, 3.92,
            4.28, 4.52, 4.01, 4.15, 3.68, 4.11, 3.99, 4.35, 4.02, 4.28, 4.31, 4.25,
            4.20, 4.42, 4.35, 4.43, 4.31, 4.28, 4.18, 4.32,
            4.29, 4.47, 4.44, 3.88, 4.38, 4.33, 3.89, 4.37, 4.45, 4.09,
            4.50, 4.33, 4.18, 4.32, 4.25, 4.23, 3.92, 4.08,
            4.34, 4.40, 4.26, 4.35, 4.18, 4.15, 4.17
        ]
    }
    
    # Generate genres programmatically
    genre_categories = [
        ['Romance'], ['Contemporary'], ['Romance'], ['Romance'],
        ['Romance', 'LGBTQ+'], ['Romance'], ['Romance'], ['Contemporary'],
        ['Romance'], ['Romance', 'LGBTQ+'], ['Romance'], ['Romance'],
        
        ['Literary Fiction'], ['Mystery'], ['Thriller'], ['Mystery'],
        ['Thriller'], ['Mystery'], ['Contemporary'], ['Thriller'],
        ['Mystery'], ['Thriller'], ['Mystery'], ['Thriller'],
        
        ['Fantasy'], ['Science Fiction'], ['Literary Fiction'], ['Literary Fiction'],
        ['Literary Fiction'], ['Science Fiction'], ['Fantasy'], ['Fantasy'],
        ['Fantasy'], ['Fantasy'], ['Science Fiction'], ['Science Fiction'],
        
        ['Young Adult'], ['Fantasy', 'Young Adult'], ['Fantasy', 'Young Adult'], ['Young Adult'],
        ['Contemporary'], ['Romance'], ['Young Adult'], ['Young Adult', 'Romance'],
        
        ['Literary Fiction'], ['Memoir'], ['Biography'], ['Philosophy'], ['Contemporary'],
        ['Literary Fiction'], ['Adventure'], ['Historical Fiction'], ['Contemporary'], ['Contemporary'],
        
        ['Historical Fiction'], ['Historical Fiction'], ['Literary Fiction'], ['Historical Fiction'],
        ['Historical Fiction'], ['Literary Fiction'], ['Historical Fiction'], ['Historical Fiction'],
        
        ['Self-Help'], ['Non-Fiction'], ['Memoir'], ['Memoir'],
        ['Psychology'], ['Psychology'], ['Psychology']
    ]
    
    # Create summer appeal descriptions
    summer_appeals = []
    for i, (title, author, year, rating) in enumerate(zip(summer_books['title'], summer_books['author'], summer_books['year'], summer_books['average_rating'])):
        genre = ', '.join(genre_categories[i]) if i < len(genre_categories) else 'Contemporary'
        appeal = generate_summer_appeal(title, author, genre, rating)
        summer_appeals.append(appeal)
    
    summer_books['genre'] = [', '.join(genres) for genres in genre_categories]
    summer_books['summer_appeal'] = summer_appeals
    
    return pd.DataFrame(summer_books)

def load_data():
    """Load book data from CSV or create sample summer data"""
    try:
        possible_files = [
            'books.csv', 'book_data.csv', 'library.csv', 'goodbooks.csv',
            'goodreads_works 2.csv', 'maven_books_dataset.csv', 'bookshelf.csv', 'maven_bookshelf.csv',
            'goodreads-books.csv', 'books_1.Best_Books_Ever.csv', 'goodreads_book_graph.csv'
        ]
        
        for filename in possible_files:
            if Path(filename).exists():
                try:
                    # Try to read with different encodings
                    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
                    df = None
                    
                    for encoding in encodings:
                        try:
                            df = pd.read_csv(filename, encoding=encoding, low_memory=False)
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if df is None:
                        continue
                    
                    # Clean column names
                    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '_')
                    
                    # Common column mappings for different datasets
                    column_mapping = {
                        'original_title': 'title',
                        'avg_rating': 'average_rating',
                        'average_rating_': 'average_rating',
                        'original_publication_year': 'year',
                        'publication_year': 'year',
                        'genres': 'genre',
                        'genre_and_votes': 'genre',
                        'authors': 'author',
                        'book_title': 'title',
                        'book_author': 'author',
                        'rating': 'average_rating',
                        'publication_date': 'year'
                    }
                    
                    # Apply column mappings
                    for old_name, new_name in column_mapping.items():
                        if old_name in df.columns:
                            df.rename(columns={old_name: new_name}, inplace=True)
                    
                    # Ensure we have required columns
                    required_columns = ['title', 'author']
                    if not all(col in df.columns for col in required_columns):
                        continue
                    
                    # Clean the data
                    df.dropna(subset=['title'], inplace=True)
                    if 'author' in df.columns:
                        df.dropna(subset=['author'], inplace=True)
                    
                    # Handle year column
                    if 'year' in df.columns:
                        df['year'] = pd.to_numeric(df['year'], errors='coerce')
                    
                    # Handle rating column
                    if 'average_rating' in df.columns:
                        df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')
                    
                    # Generate summer appeal for external datasets
                    if 'summer_appeal' not in df.columns:
                        df['summer_appeal'] = df.apply(lambda row: generate_summer_appeal(
                            row.get('title', ''),
                            row.get('author', ''),
                            row.get('genre', 'Contemporary'),
                            row.get('average_rating', 3.5)
                        ), axis=1)
                    
                    st.success(f"📚 Successfully loaded {len(df):,} books from {filename}")
                    return df
                    
                except Exception as file_error:
                    st.warning(f"⚠️ Could not load {filename}: {str(file_error)}")
                    continue
        
        st.info("📝 No CSV file found. Using expanded curated summer reading recommendations.")
        return load_sample_summer_data()
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("Using expanded sample summer reading data instead.")
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
    """Display a summer-themed book card"""
    genre_data = book.get('genre', 'Contemporary')
    parsed_genres = parse_genres(genre_data)
    
    # Get summer appeal description
    summer_appeal = book.get('summer_appeal', 'Great for summer reading')
    
    if parsed_genres and parsed_genres != ['Contemporary']:
        genre_display = " ".join([summer_genre_icons.get(g, "📚") + " " + g for g in parsed_genres[:2]])
    else:
        genre_display = "📚 Contemporary"
    
    card_class = "ultra-compact-summer-card" if compact else "summer-book-card"
    
    with st.container():
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        
        if show_add_button or show_remove_button:
            col_info, col_action = st.columns([5, 1])
        else:
            col_info = st.container()
            col_action = None
        
        with col_info:
            title = str(book.get('title', 'Unknown Title'))
            author = str(book.get('author', 'Unknown Author'))
            
            display_title = title if len(title) <= 60 else title[:57] + "..."
            st.markdown(f'<div class="book-title" style="font-size: 1rem; margin-bottom: 0.2rem; color: #FF7043;">{display_title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="book-author" style="font-size: 0.8rem; margin-bottom: 0.2rem; color: #8D6E63;">by {author}</div>', unsafe_allow_html=True)
            
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
            
            st.markdown(f'<div class="book-details" style="font-size: 0.75rem; margin-bottom: 0.3rem; color: #5D4037;">{rating_display} • {year_display} • {genre_display}</div>', unsafe_allow_html=True)
            
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
    st.markdown("### ☀️ Discover Summer Books")
    
    if st.session_state.books_df.empty:
        st.warning("📚 No book collection available. Please ensure your dataset file is in the project directory.")
        return
    
    df = st.session_state.books_df.copy()
    df['summer_score'] = df.apply(get_summer_appeal_score, axis=1)
    
    # Main search bar
    search_term = st.text_input("🔍 Search books, authors, or genres", placeholder="Try 'beach read', 'thriller', or author name...")
    
    # Filters in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Author filter
        if 'author' in df.columns:
            authors_list = ['All Authors'] + sorted(df['author'].dropna().unique().tolist())
            selected_author = st.selectbox("👤 Author", authors_list)
        else:
            selected_author = 'All Authors'
    
    with col2:
        # Genre filter
        all_genres = set()
        for genre_data in df['genre'].dropna():
            parsed_genres = parse_genres(genre_data)
            all_genres.update(parsed_genres)
        
        genres_list = ['All Genres'] + sorted(list(all_genres))
        selected_genre = st.selectbox("📚 Genre", genres_list)
    
    with col3:
        # Rating filter
        if 'average_rating' in df.columns:
            min_rating = st.slider("⭐ Min Rating", 1.0, 5.0, 3.5, step=0.1)
        else:
            min_rating = 1.0
    
    with col4:
        # Summer appeal filter
        min_summer_score = st.slider("☀️ Summer Appeal", 1.0, 5.0, 3.5, step=0.1)
    
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
    
    # Genre filter
    if selected_genre != 'All Genres':
        genre_mask = filtered_df['genre'].apply(lambda x: selected_genre in parse_genres(x))
        filtered_df = filtered_df[genre_mask]
    
    # Rating filter
    if 'average_rating' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['average_rating'] >= min_rating]
    
    # Summer appeal filter
    filtered_df = filtered_df[filtered_df['summer_score'] >= min_summer_score]
    
    # Sort by summer score and relevance
    recommended_df = filtered_df.sort_values(['summer_score', 'average_rating'], ascending=[False, False])
    
    # Show curated recommendations if no specific filters applied
    if not search_term and selected_author == 'All Authors' and selected_genre == 'All Genres' and min_rating <= 3.5 and min_summer_score <= 3.5:
        st.markdown("#### ⭐ Staff Picks - Highly Recommended Summer Reads")
        # Show top books by summer score, but don't limit to just 25
        recommended_df = df.nlargest(min(100, len(df)), 'summer_score')
    
    # Display pagination for large datasets
    results_per_page = 50
    total_results = len(recommended_df)
    
    # Pagination
    if total_results > results_per_page:
        # Add pagination controls
        col_pag1, col_pag2, col_pag3 = st.columns([2, 1, 2])
        with col_pag2:
            page_number = st.number_input(
                f"Page (1-{(total_results-1)//results_per_page + 1})", 
                min_value=1, 
                max_value=(total_results-1)//results_per_page + 1, 
                value=1
            )
        
        start_idx = (page_number - 1) * results_per_page
        end_idx = min(start_idx + results_per_page, total_results)
        display_df = recommended_df.iloc[start_idx:end_idx]
        
        st.markdown(f"### 📖 Showing {start_idx + 1}-{end_idx} of {total_results:,} Books")
    else:
        display_df = recommended_df
        st.markdown(f"### 📖 {total_results:,} Books Found")
    
    # Display results
    if total_results == 0:
        st.warning("🔍 No books match your current filters. Try adjusting your search criteria.")
        return
    
    # Show helpful tips for large datasets
    if total_results > 200:
        st.info("💡 **Large dataset detected!** Use the search and filter options above to find books more easily. You can search by title, author, or genre.")
    
    # Display books
    for _, book in display_df.iterrows():
        display_summer_book_card(book, show_add_button=True, compact=True)
