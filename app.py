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
    
    .ultra-compact-summer-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 0.5rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(255, 112, 67, 0.15);
        border: 1px solid rgba(255, 180, 71, 0.2);
        border-left: 3px solid #FFB347;
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
    
    .summer-stat {
        background: linear-gradient(135deg, rgba(255, 248, 220, 0.9) 0%, rgba(255, 235, 205, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255, 165, 0, 0.3);
        box-shadow: 0 3px 10px rgba(255, 140, 0, 0.2);
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
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'discover'

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
            'Beach Read', 'The Seven Husbands of Evelyn Hugo', 'It Ends with Us', 'The Hating Game',
            'Red, White & Royal Blue', 'The Kiss Quotient', 'Where the Crawdads Sing', 'The Guest List',
            'The Invisible Life of Addie LaRue', 'Project Hail Mary', 'The Summer I Turned Pretty', 'Normal People',
            'The Nightingale', 'Educated', 'The Thursday Murder Club', 'Circe'
        ],
        'author': [
            'Emily Henry', 'Taylor Jenkins Reid', 'Colleen Hoover', 'Sally Thorne',
            'Casey McQuiston', 'Helen Hoang', 'Delia Owens', 'Lucy Foley',
            'V.E. Schwab', 'Andy Weir', 'Jenny Han', 'Sally Rooney',
            'Kristin Hannah', 'Tara Westover', 'Richard Osman', 'Madeline Miller'
        ],
        'year': [
            2020, 2017, 2016, 2016, 2019, 2018, 2018, 2020,
            2020, 2021, 2009, 2018, 2015, 2018, 2020, 2018
        ],
        'average_rating': [
            4.05, 4.25, 4.30, 4.15, 4.40, 4.20, 4.41, 4.01,
            4.28, 4.52, 4.20, 4.29, 4.50, 4.47, 4.26, 4.35
        ],
        'genre': [
            'Romance', 'Contemporary', 'Romance', 'Romance',
            'Romance, LGBTQ+', 'Romance', 'Literary Fiction', 'Mystery',
            'Fantasy', 'Science Fiction', 'Young Adult', 'Literary Fiction',
            'Historical Fiction', 'Memoir', 'Mystery', 'Fantasy'
        ],
        'summer_appeal': [
            'Perfect summer romance', 'Engaging contemporary fiction', 'Heartwarming love story', 'Romantic escapism',
            'Popular LGBTQ+ romance', 'Perfect poolside read', 'Beautiful nature writing', 'Gripping page-turner',
            'Magical escapism', 'Thought-provoking sci-fi', 'Perfect YA summer read', 'Award-winning literary fiction',
            'Rich historical detail', 'Inspiring memoir', 'Cozy mystery series', 'Enchanting mythology retelling'
        ]
    }
    return pd.DataFrame(summer_books)

def load_data():
    """Load book data"""
    try:
        # Try to find CSV files in the current directory
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        
        if csv_files:
            st.info(f"📁 Found CSV files: {', '.join(csv_files)}")
            # Try to load the first CSV file
            for csv_file in csv_files:
                try:
                    df = pd.read_csv(csv_file)
                    st.success(f"✅ Successfully loaded {len(df)} books from {csv_file}")
                    
                    # Basic column standardization
                    if 'original_title' in df.columns and 'title' not in df.columns:
                        df['title'] = df['original_title']
                    if 'authors' in df.columns and 'author' not in df.columns:
                        df['author'] = df['authors']
                    if 'avg_rating' in df.columns and 'average_rating' not in df.columns:
                        df['average_rating'] = df['avg_rating']
                        
                    # Ensure required columns exist
                    if 'title' not in df.columns or 'author' not in df.columns:
                        st.warning(f"⚠️ {csv_file} missing required columns (title, author)")
                        continue
                        
                    return df
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not load {csv_file}: {str(e)}")
                    continue
        
        # If no CSV files found or none could be loaded, use sample data
        st.info("📚 No suitable CSV file found. Using sample summer reading data.")
        return load_sample_summer_data()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
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
    try:
        with open(SUMMER_LIST_FILE, 'w') as f:
            json.dump(st.session_state.summer_reading_list, f, indent=2)
    except Exception as e:
        st.error(f"Error saving list: {e}")

def parse_genres(genre_data):
    """Parse genre data into a list"""
    if pd.isna(genre_data) or genre_data == '':
        return ['Contemporary']
    
    genres = str(genre_data).split(',')
    return [g.strip() for g in genres if g.strip()]

def get_summer_appeal_score(book):
    """Calculate summer appeal score"""
    rating = book.get('average_rating', 3.5)
    genre = book.get('genre', 'Contemporary')
    
    # Summer-friendly genres get bonus
    summer_genres = ['Romance', 'Contemporary', 'Mystery', 'Young Adult', 'Adventure']
    bonus = 0.5 if any(sg in str(genre) for sg in summer_genres) else 0
    
    try:
        base_score = float(rating) if pd.notna(rating) else 3.5
        return min(5.0, base_score + bonus)
    except:
        return 3.5

def display_book_card(book, show_add_button=True, compact=False):
    """Display a book card"""
    card_class = "ultra-compact-summer-card" if compact else "summer-book-card"
    
    with st.container():
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        
        if show_add_button:
            col_info, col_action = st.columns([5, 1])
        else:
            col_info = st.container()
            col_action = None
        
        with col_info:
            title = str(book.get('title', 'Unknown Title'))
            author = str(book.get('author', 'Unknown Author'))
            
            st.markdown(f'**{title}**')
            st.markdown(f'*by {author}*')
            
            # Rating and year
            rating = book.get('average_rating', 0)
            year = book.get('year', 'Unknown')
            genre = book.get('genre', 'Contemporary')
            
            if pd.notna(rating) and rating > 0:
                rating_display = f"⭐ {float(rating):.1f}"
            else:
                rating_display = "⭐ N/A"
            
            st.markdown(f'{rating_display} • {year} • {genre}')
            
            # Summer appeal
            summer_appeal = book.get('summer_appeal', 'Great for summer reading')
            if not compact:
                st.markdown(f'☀️ *{summer_appeal}*')
        
        if col_action and show_add_button:
            with col_action:
                book_id = f"{title}_{author}"
                book_exists = any(b['title'] == title and b['author'] == author 
                                for b in st.session_state.summer_reading_list)
                
                if not book_exists:
                    if st.button("➕", key=f"add_{book_id}", help="Add to Summer List"):
                        new_book = {
                            'id': len(st.session_state.summer_reading_list) + 1,
                            'title': title,
                            'author': author,
                            'genre': book.get('genre', 'Contemporary'),
                            'rating': book.get('average_rating', 4.0),
                            'year': book.get('year', 'Unknown'),
                            'summer_appeal': summer_appeal,
                            'date_added': datetime.now().strftime("%Y-%m-%d")
                        }
                        st.session_state.summer_reading_list.append(new_book)
                        save_summer_list()
                        st.success(f"Added '{title}' to your summer reading list! ☀️")
                        st.rerun()
                else:
                    st.markdown("✅")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-brand">☀️ Summer Reading</div>
        <div class="sidebar-subtitle">Build Your Perfect List</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.radio(
        "Navigate",
        ["🔍 Discover Books", "📚 My Summer List", "📊 Statistics"],
        key="navigation"
    )
    
    # Load data if not already loaded
    if not st.session_state.loaded_data:
        with st.spinner("Loading books..."):
            st.session_state.books_df = load_data()
            st.session_state.summer_reading_list = load_summer_list()
            st.session_state.loaded_data = True
    
    # Display some stats
    if not st.session_state.books_df.empty:
        st.markdown("---")
        st.markdown("📊 **Quick Stats**")
        total_books = len(st.session_state.books_df)
        list_books = len(st.session_state.summer_reading_list)
        st.metric("Available Books", f"{total_books:,}")
        st.metric("In Summer List", list_books)

# Main content
if page == "🔍 Discover Books":
    st.title("🔍 Discover Summer Books")
    
    if st.session_state.books_df.empty:
        st.warning("No books loaded. Please check your data files.")
    else:
        df = st.session_state.books_df.copy()
        
        # Add summer score
        df['summer_score'] = df.apply(get_summer_appeal_score, axis=1)
        
        # Search and filters
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input("🔍 Search books, authors, or genres", 
                                      placeholder="Try 'romance', 'mystery', or author name...")
        
        with col2:
            min_rating = st.slider("⭐ Min Rating", 1.0, 5.0, 3.0, step=0.1)
        
        # Apply filters
        filtered_df = df.copy()
        
        if search_term:
            search_mask = (
                filtered_df['title'].str.contains(search_term, case=False, na=False) |
                filtered_df['author'].str.contains(search_term, case=False, na=False) |
                filtered_df['genre'].str.contains(search_term, case=False, na=False)
            )
            filtered_df = filtered_df[search_mask]
        
        if 'average_rating' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['average_rating'] >= min_rating]
        
        # Sort by summer score
        filtered_df = filtered_df.sort_values(['summer_score', 'average_rating'], 
                                            ascending=[False, False])
        
        # Display results
        total_results = len(filtered_df)
        st.markdown(f"### 📖 {total_results} Books Found")
        
        if total_results == 0:
            st.info("No books match your search. Try different keywords or lower the rating filter.")
        else:
            # Show books
            for _, book in filtered_df.head(20).iterrows():  # Limit to first 20 for performance
                display_book_card(book, show_add_button=True, compact=True)
            
            if total_results > 20:
                st.info(f"Showing first 20 results. {total_results - 20} more books available - refine your search to see more.")

elif page == "📚 My Summer List":
    st.title("📚 My Summer Reading List")
    
    if not st.session_state.summer_reading_list:
        st.markdown("""
        <div class="summer-empty-state">
            <h3>🏖️ Your Summer List is Empty!</h3>
            <p>Start building your perfect summer reading collection by discovering books and adding them to your list.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"### 🌞 {len(st.session_state.summer_reading_list)} Books in Your Summer List")
        
        # Clear list button
        if st.button("🗑️ Clear All Books", type="secondary"):
            st.session_state.summer_reading_list = []
            save_summer_list()
            st.rerun()
        
        # Display books in list
        for i, book in enumerate(st.session_state.summer_reading_list):
            col_book, col_remove = st.columns([5, 1])
            
            with col_book:
                display_book_card(book, show_add_button=False)
            
            with col_remove:
                if st.button("🗑️", key=f"remove_{i}", help="Remove from list"):
                    st.session_state.summer_reading_list.pop(i)
                    save_summer_list()
                    st.rerun()

elif page == "📊 Statistics":
    st.title("📊 Summer Reading Statistics")
    
    if st.session_state.summer_reading_list:
        list_df = pd.DataFrame(st.session_state.summer_reading_list)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="summer-stat">
                <div class="stat-number">{}</div>
                <div class="stat-label">Total Books</div>
            </div>
            """.format(len(list_df)), unsafe_allow_html=True)
        
        with col2:
            avg_rating = list_df['rating'].mean() if 'rating' in list_df.columns else 0
            st.markdown("""
            <div class="summer-stat">
                <div class="stat-number">{:.1f}⭐</div>
                <div class="stat-label">Avg Rating</div>
            </div>
            """.format(avg_rating), unsafe_allow_html=True)
        
        with col3:
            genres = []
            for genre_list in list_df['genre']:
                genres.extend(parse_genres(genre_list))
            most_common = max(set(genres), key=genres.count) if genres else "None"
            st.markdown("""
            <div class="summer-stat">
                <div class="stat-number">{}</div>
                <div class="stat-label">Top Genre</div>
            </div>
            """.format(most_common), unsafe_allow_html=True)
        
        # Genre distribution
        if genres:
            st.markdown("### 📊 Genre Distribution")
            genre_counts = pd.Series(genres).value_counts()
            st.bar_chart(genre_counts.head(10))
    
    else:
        st.info("Add some books to your summer list to see statistics!")

# Footer
st.markdown("---")
st.markdown("*Built with ☀️ for summer reading enthusiasts*")
