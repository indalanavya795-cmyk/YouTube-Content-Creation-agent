import streamlit as st

from agent import (
    generate_youtube_idea,
    generate_youtube_titles,
    generate_youtube_description,
    generate_youtube_hashtags,
    generate_youtube_keywords,
    generate_youtube_script,
    generate_thumbnail_ideas,
    save_youtube_content
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="YouTube Content Creation Agent",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎬 YouTube Content Creation Agent")

st.write(
    "Generate YouTube ideas, titles, descriptions, keywords, "
    "hashtags, scripts, and thumbnail concepts using AI."
)


# ============================================================
# TOPIC INPUT
# ============================================================

topic = st.text_input(
    "Enter your YouTube topic",
    placeholder="Example: AI tools for students"
)


# ============================================================
# GENERATE VIDEO IDEAS
# ============================================================

if st.button("🚀 Generate Content", type="primary"):

    if not topic.strip():

        st.warning("Please enter a topic first.")

    else:

        with st.spinner("Generating YouTube video ideas..."):

            ideas = generate_youtube_idea(topic)

        st.session_state["ideas"] = ideas

        st.success("Video ideas generated!")


# ============================================================
# DISPLAY VIDEO IDEAS
# ============================================================

if "ideas" in st.session_state:

    st.subheader("💡 YouTube Video Ideas")

    st.text_area(
        "Generated ideas",
        st.session_state["ideas"],
        height=180
    )

    st.write("### Choose one idea")

    selected_idea = st.text_area(
        "Enter your chosen video idea:",
        placeholder="Paste one of the generated ideas here.",
        height=100
    )


    # ========================================================
    # GENERATE COMPLETE CONTENT
    # ========================================================

    if st.button("✨ Generate Complete Content"):

        if not selected_idea.strip():

            st.warning("Please enter a video idea first.")

        else:

            with st.spinner("Generating titles..."):

                titles = generate_youtube_titles(
                    selected_idea
                )


            with st.spinner("Generating description..."):

                description = generate_youtube_description(
                    selected_idea
                )


            with st.spinner("Generating hashtags..."):

                hashtags = generate_youtube_hashtags(
                    selected_idea
                )


            with st.spinner("Generating keywords..."):

                keywords = generate_youtube_keywords(
                    selected_idea
                )


            with st.spinner("Generating video script..."):

                script = generate_youtube_script(
                    selected_idea
                )


            with st.spinner("Generating thumbnail ideas..."):

                thumbnail_ideas = generate_thumbnail_ideas(
                    selected_idea
                )


            # =================================================
            # SAVE CONTENT
            # =================================================

            file_path = save_youtube_content(
                selected_idea,
                titles,
                description,
                hashtags,
                keywords,
                script,
                thumbnail_ideas
            )


            # =================================================
            # STORE RESULTS
            # =================================================

            st.session_state["selected_idea"] = selected_idea
            st.session_state["titles"] = titles
            st.session_state["description"] = description
            st.session_state["hashtags"] = hashtags
            st.session_state["keywords"] = keywords
            st.session_state["script"] = script
            st.session_state["thumbnail_ideas"] = thumbnail_ideas
            st.session_state["file_path"] = file_path

            st.success(
                "🎉 Complete YouTube content generated successfully!"
            )


# ============================================================
# DISPLAY GENERATED CONTENT
# ============================================================

if "selected_idea" in st.session_state:

    st.divider()

    st.header("📦 Your YouTube Content")


    # ========================================================
    # VIDEO IDEA
    # ========================================================

    st.subheader("💡 Selected Video Idea")

    st.text_area(
        "Video idea",
        st.session_state["selected_idea"],
        height=100
    )


    # ========================================================
    # TITLES
    # ========================================================

    st.subheader("🎬 YouTube Titles")

    st.text_area(
        "Titles",
        st.session_state["titles"],
        height=180
    )


    # ========================================================
    # DESCRIPTION
    # ========================================================

    st.subheader("📝 YouTube Description")

    st.text_area(
        "Description",
        st.session_state["description"],
        height=250
    )


    # ========================================================
    # KEYWORDS
    # ========================================================

    st.subheader("🔑 YouTube Keywords")

    st.text_area(
        "Keywords",
        st.session_state["keywords"],
        height=150
    )


    # ========================================================
    # HASHTAGS
    # ========================================================

    st.subheader("#️⃣ YouTube Hashtags")

    st.text_area(
        "Hashtags",
        st.session_state["hashtags"],
        height=120
    )


    # ========================================================
    # SCRIPT
    # ========================================================

    st.subheader("🎥 YouTube Video Script")

    st.text_area(
        "Video script",
        st.session_state["script"],
        height=400
    )


    # ========================================================
    # THUMBNAIL IDEAS
    # ========================================================

    st.subheader("🖼️ Thumbnail Ideas")

    st.text_area(
        "Thumbnail ideas",
        st.session_state["thumbnail_ideas"],
        height=180
    )


    # ========================================================
    # SAVED FILE
    # ========================================================

    st.divider()

    st.success(
        f"Content saved successfully to: "
        f"{st.session_state['file_path']}"
    )


    # ========================================================
    # DOWNLOAD CONTENT
    # ========================================================

    st.subheader("⬇️ Download Your Content")


    download_content = f"""
YOUTUBE CONTENT CREATION AGENT

VIDEO IDEA
{st.session_state["selected_idea"]}


TITLES
{st.session_state["titles"]}


DESCRIPTION
{st.session_state["description"]}


KEYWORDS
{st.session_state["keywords"]}


HASHTAGS
{st.session_state["hashtags"]}


VIDEO SCRIPT
{st.session_state["script"]}


THUMBNAIL IDEAS
{st.session_state["thumbnail_ideas"]}
"""


    st.download_button(
        label="📥 Download Complete Content",
        data=download_content,
        file_name="youtube_content.txt",
        mime="text/plain"
    )