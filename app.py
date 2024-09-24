import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

st.title("AI-Enhanced Life Map Visualization")
st.write("Input your journal entry and visualize your life!")
st.header("Enter Your Journal Entry")
journal_entry = st.text_area("Journal Entry", height=200)

def categorize_journal_entry(entry):
    doc = nlp(entry)
    emotions = []
    interests = []
    projects = []
    traits = []
    events = []
    keywords = []

    for sentence in doc.sents:
        # Enhanced keyword-based categorization
        if any(emotion in sentence.text for emotion in ["happy", "excited", "joyful"]):
            emotions.append("Happy")
        elif any(emotion in sentence.text for emotion in ["sad", "frustrated", "angry"]):
            emotions.append("Sad")
        if "design" in sentence.text or "art" in sentence.text:
            interests.append("Creative Arts")
        if "project" in sentence.text:
            projects.append(sentence.text)
        if "I am" in sentence.text or "I feel" in sentence.text:
            traits.append(sentence.text)
        if any(event in sentence.text for event in ["birthday", "graduation", "anniversary"]):
            events.append(sentence.text)
        keywords.extend([token.text for token in doc if token.is_alpha and not token.is_stop])

    return emotions, interests, projects, traits, events, keywords

if st.button("Generate Life Map"):
    if journal_entry:
        emotions, interests, projects, traits, events, keywords = categorize_journal_entry(journal_entry)

        # Prepare data for radar chart
        categories = ['Emotions', 'Interests', 'Current Projects', 'Personality Traits', 'Significant Events']
        sizes = [len(emotions), len(interests), len(projects), len(traits), len(events)]

        # Create Radar Chart
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=sizes + [sizes[0]],  # Closing the radar chart
            theta=categories + [categories[0]],  # Closing the radar chart
            fill='toself',
            name='Life Map'
        ))

        fig.update_layout(title='Life Map Overview', polar=dict(radialaxis=dict(visible=True, range=[0, max(sizes) + 1])), showlegend=True)
        st.plotly_chart(fig)

        # Generate and display Word Cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(keywords))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # Display summary
        st.write("### Summary of Your Entry:")
        st.write(f"**Emotions:** {', '.join(emotions) if emotions else 'None'}")
        st.write(f"**Interests:** {', '.join(interests) if interests else 'None'}")
        st.write(f"**Current Projects:** {', '.join(projects) if projects else 'None'}")
        st.write(f"**Personality Traits:** {', '.join(traits) if traits else 'None'}")
        st.write(f"**Significant Events:** {', '.join(events) if events else 'None'}")
    else:
        st.error("Please enter a journal entry!")
