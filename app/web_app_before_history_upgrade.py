
import streamlit as st
import json
from pathlib import Path

from auth import show_auth
from agent import (
    generate_creative_ideas,
    generate_surprise_idea,
    generate_trend_inspired_ideas,
)

st.set_page_config(
    page_title="AI Content Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    show_auth()
    st.stop()

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

# ---------------------------------------------------------
# PROFESSIONAL CSS
# ---------------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.hero {
    padding: 42px;
    border-radius: 24px;
    background: linear-gradient(135deg, #151515, #252525);
    margin-bottom: 28px;
}

.hero h1 {
    font-size: 46px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    opacity: .7;
}

.card {
    padding: 26px;
    border: 1px solid rgba(128,128,128,.2);
    border-radius: 20px;
    min-height: 180px;
    margin-bottom: 18px;
}

.card h3 {
    margin-top: 5px;
}

.small {
    opacity: .65;
}

.section-title {
    margin-top: 20px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎬 AI Content Studio")
    st.caption("AI-powered creator workspace")

    st.divider()

    pages = {
        "🏠 Dashboard": "Dashboard",
        "💡 Idea Lab": "Idea Lab",
        "🎬 Content Studio": "Content Studio",
        "🖼️ Visual Studio": "Visual Studio",
        "📱 Repurpose": "Repurpose",
        "📚 History": "History",
        "👤 Profile": "Profile",
    }

    for label, page_name in pages.items():
        if st.button(
            label,
            use_container_width=True,
            key="nav_" + page_name.replace(" ", "_")
        ):
            st.session_state["page"] = page_name
            st.rerun()

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state.pop("current_user", None)
        st.session_state["page"] = "Dashboard"
        st.rerun()


page = st.session_state["page"]

# =========================================================
# DASHBOARD
# =========================================================
if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>✨ Create something amazing.</h1>
        <p>Your AI workspace for ideas, scripts, thumbnails and social content.</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # CREATOR OVERVIEW
    # ---------------------------------------------------------
    st.markdown("### 📊 Creator Overview")

    idea_count = 0
    if st.session_state.get("creative_ideas_ready"):
        idea_count += 1
    if st.session_state.get("surprise_idea_ready"):
        idea_count += 1
    if st.session_state.get("trend_ideas_ready"):
        idea_count += 1

    generated_count = 0
    for key in [
        "generated_content",
        "content",
        "strategy",
        "script",
        "storyboard",
    ]:
        if st.session_state.get(key):
            generated_count += 1

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("💡 Ideas Created", idea_count)

    with m2:
        st.metric("🎬 Content Assets", generated_count)

    with m3:
        st.metric("🧠 AI Engine", "Ollama")

    with m4:
        st.metric("⚡ Workspace", "Ready")

    st.markdown("### 🚀 Quick Actions")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
            <h2>💡</h2>
            <h3>Idea Lab</h3>
            <p class="small">Generate fresh, surprising and trend-inspired content ideas.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Idea Lab →", use_container_width=True):
            st.session_state["page"] = "Idea Lab"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="card">
            <h2>🎬</h2>
            <h3>Content Studio</h3>
            <p class="small">Create complete YouTube content from one topic.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Content Studio →", use_container_width=True):
            st.session_state["page"] = "Content Studio"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="card">
            <h2>🖼️</h2>
            <h3>Visual Studio</h3>
            <p class="small">Create thumbnail concepts and visual assets.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Visual Studio →", use_container_width=True):
            st.session_state["page"] = "Visual Studio"
            st.rerun()

    st.markdown("### 🧰 Creator Tools")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
            <h3>📱 Repurpose</h3>
            <p class="small">Turn your long-form content into Shorts and Reels.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Repurpose", use_container_width=True):
            st.session_state["page"] = "Repurpose"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="card">
            <h3>📚 History</h3>
            <p class="small">Review content generated during your current session.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open History", use_container_width=True):
            st.session_state["page"] = "History"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="card">
            <h3>👤 Profile</h3>
            <p class="small">View your creator account information.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Profile", use_container_width=True):
            st.session_state["page"] = "Profile"
            st.rerun()

# =========================================================
# IDEA LAB
# =========================================================
elif page == "Idea Lab":

    st.title("💡 Idea Lab")
    st.caption("Turn a simple concept into creative content opportunities.")

    col1, col2 = st.columns(2)

    with col1:
        audience = st.text_input(
            "🎯 Audience",
            value="College students",
            key="idea_audience"
        )

        platform = st.selectbox(
            "📱 Platform",
            ["YouTube", "Instagram", "YouTube Shorts", "Instagram Reels"],
            key="idea_platform"
        )

    with col2:
        content_type = st.selectbox(
            "🎥 Content Type",
            ["Video", "Short", "Vlog", "Tutorial", "Storytelling", "Review"],
            key="idea_content_type"
        )

        goal = st.selectbox(
            "🎯 Goal",
            ["Growth", "Engagement", "Education", "Entertainment", "Personal Brand"],
            key="idea_goal"
        )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("💡 GENERATE CREATIVE IDEAS", use_container_width=True):
            with st.spinner("🧠 Brainstorming fresh ideas..."):
                st.session_state["creative_ideas"] = generate_creative_ideas(
                    audience,
                    platform,
                    content_type,
                    goal
                )
            st.session_state["creative_ideas_ready"] = True

    with c2:
        if st.button("🎲 SURPRISE ME", use_container_width=True):
            with st.spinner("🎲 Creating a surprise idea..."):
                st.session_state["surprise_idea"] = generate_surprise_idea(
                    audience,
                    platform,
                    content_type
                )
            st.session_state["surprise_idea_ready"] = True

    with c3:
        if st.button("🔥 TREND-INSPIRED", use_container_width=True):
            with st.spinner("🔥 Creating trend-inspired concepts..."):
                st.session_state["trend_ideas"] = generate_trend_inspired_ideas(
                    audience,
                    platform,
                    content_type
                )
            st.session_state["trend_ideas_ready"] = True

    if st.session_state.get("creative_ideas_ready"):
        st.divider()
        st.subheader("💡 Creative Ideas")
        st.write(st.session_state.get("creative_ideas", ""))

    if st.session_state.get("surprise_idea_ready"):
        st.divider()
        st.subheader("🎲 Surprise Idea")
        st.write(st.session_state.get("surprise_idea", ""))

    if st.session_state.get("trend_ideas_ready"):
        st.divider()
        st.subheader("🔥 Trend-Inspired Concepts")
        st.write(st.session_state.get("trend_ideas", ""))

# =========================================================
# CONTENT STUDIO
# =========================================================
elif page == "Content Studio":

    st.title("🎬 Content Studio")
    st.caption("Your complete AI content generation workspace.")

    content_file = Path(__file__).parent / "content_studio.py"

    if content_file.exists():
        code = content_file.read_text()
        exec(compile(code, str(content_file), "exec"), globals())
    else:
        st.error("Content Studio file was not found.")

# =========================================================
# VISUAL STUDIO
# =========================================================
elif page == "Visual Studio":

    st.title("🖼️ Visual Studio")
    st.caption("Create thumbnails and visual assets for your content.")

    st.markdown("""
    <div class="hero">
        <h1>🎨 Make your content stand out.</h1>
        <p>
        Generate thumbnail concepts and use your existing AI thumbnail
        workflow from one workspace.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Thumbnail Workspace")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="card">
            <h2>💡 Thumbnail Ideas</h2>
            <p class="small">
            Generate attention-grabbing thumbnail concepts based on your
            current content.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <h2>🖼️ Thumbnail Generator</h2>
            <p class="small">
            Use the existing Content Studio thumbnail-generation workflow
            to create your visual assets.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    topic = st.session_state.get("topic_input", "")

    if topic:
        st.markdown("### 📌 Current Project")
        st.info(f"Current topic: **{topic}**")
    else:
        st.info(
            "Start a project in Content Studio first. "
            "Your topic and generated thumbnail workflow will then be available here."
        )

    st.markdown("### 🚀 Continue Creating")

    if st.button(
        "🎬 OPEN CONTENT STUDIO & CREATE THUMBNAIL",
        use_container_width=True
    ):
        st.session_state["page"] = "Content Studio"
        st.rerun()

    st.caption(
        "Your existing thumbnail-generation system remains unchanged."
    )

# =========================================================
# REPURPOSE
# =========================================================
elif page == "Repurpose":

    st.title("📱 Repurpose")
    st.caption("Turn one piece of content into multiple social formats.")

    st.markdown("""
    <div class="hero">
        <h1>♻️ Create more from one idea.</h1>
        <p>
        Transform your long-form content into short-form content
        for YouTube Shorts and Instagram Reels.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📦 Repurposing Formats")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="card">
            <h2>▶️ YouTube Shorts</h2>
            <p class="small">
            Extract the strongest moments and turn them into short,
            engaging vertical content.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <h2>📸 Instagram Reels</h2>
            <p class="small">
            Adapt your content into concise, hook-driven Reel concepts.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    generated = []

    for key, label in [
        ("shorts", "▶️ YouTube Shorts"),
        ("reel", "📸 Instagram Reel"),
        ("repurposed", "♻️ Repurposed Content"),
    ]:
        value = st.session_state.get(key)
        if value:
            generated.append((label, value))

    if generated:
        st.markdown("### ✨ Generated Repurposed Content")

        for label, value in generated:
            with st.expander(label, expanded=False):
                st.write(value)
    else:
        st.info(
            "No repurposed content is available yet. "
            "Generate complete content in Content Studio first."
        )

    st.divider()

    if st.button(
        "🎬 OPEN CONTENT STUDIO",
        use_container_width=True
    ):
        st.session_state["page"] = "Content Studio"
        st.rerun()

    st.caption(
        "Your existing Shorts and Reel generation workflow remains unchanged."
    )

# =========================================================
# HISTORY
# =========================================================
elif page == "History":

    st.title("📚 Content History")
    st.caption("Your generated content from this session.")

    found = False

    history_keys = [
        ("creative_ideas", "💡 Creative Ideas"),
        ("surprise_idea", "🎲 Surprise Idea"),
        ("trend_ideas", "🔥 Trend-Inspired Ideas"),
        ("generated_content", "🎬 Generated Content"),
        ("content", "📝 Content"),
        ("topic", "📌 Topic"),
    ]

    for key, title in history_keys:
        if key in st.session_state and st.session_state[key]:
            found = True
            with st.expander(title, expanded=False):
                st.write(st.session_state[key])

    if not found:
        st.info(
            "No generated content is available yet. "
            "Create something in Idea Lab or Content Studio first."
        )

# =========================================================
# PROFILE
# =========================================================
elif page == "Profile":

    st.title("👤 Profile")
    st.caption("Your AI Content Studio account.")

    username = st.session_state.get("current_user", "")

    users_file = Path("data/users.json")
    user = {}

    if users_file.exists() and username:
        try:
            users = json.loads(users_file.read_text())
            user = users.get(username, {})
        except Exception:
            user = {}

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Account")
        st.write("**Username:**", username or "Not available")
        st.write("**Name:**", user.get("name", "Not available"))
        st.write("**Email:**", user.get("email", "Not available"))

    with c2:
        st.markdown("### Workspace")
        st.write("🎬 AI Content Studio")
        st.write("🤖 Local AI Content Generation")
        st.write("🖼️ Thumbnail Generation")
        st.write("📱 Content Repurposing")

    st.divider()

    st.info(
        "Your account is currently stored locally for this prototype. "
        "Cloud database authentication can be added later during deployment."
    )
