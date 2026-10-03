
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
    st.caption("Review the content you've created in this workspace.")

    topic = st.session_state.get("topic_input", "")
    thumbnail = st.session_state.get("thumbnail_path", "")
    shorts = st.session_state.get("shorts", "")
    reel = st.session_state.get("reel", "")
    repurposed = st.session_state.get("repurposed", "")

    ideas = (
        st.session_state.get("creative_ideas")
        or st.session_state.get("surprise_idea")
        or st.session_state.get("trend_ideas")
        or ""
    )

    content_available = any(
        st.session_state.get(key)
        for key in [
            "generated_content",
            "content",
            "strategy",
            "script",
            "storyboard",
        ]
    )

    # -----------------------------------------------------
    # PROJECT SUMMARY
    # -----------------------------------------------------
    if topic or content_available or thumbnail or shorts or reel:

        st.markdown("### 📌 Current Project")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "📌 Topic",
                "Created" if topic else "Not started"
            )

        with c2:
            st.metric(
                "💡 Ideas",
                "Available" if ideas else "None"
            )

        with c3:
            st.metric(
                "🎬 Content",
                "Ready" if content_available else "Pending"
            )

        with c4:
            st.metric(
                "🖼️ Thumbnail",
                "Ready" if thumbnail else "Pending"
            )

        st.divider()

        if topic:
            st.markdown("### 🎯 Project Topic")
            st.info(topic)

        st.markdown("### 📦 Generated Assets")

        assets = []

        if ideas:
            assets.append(("💡 Ideas", ideas))

        if content_available:
            for key, label in [
                ("generated_content", "🎬 Generated Content"),
                ("content", "📝 Content"),
                ("strategy", "🧠 Content Strategy"),
                ("script", "📜 Script"),
                ("storyboard", "🎞️ Storyboard"),
            ]:
                value = st.session_state.get(key)
                if value:
                    assets.append((label, value))

        if thumbnail:
            assets.append(("🖼️ Thumbnail", thumbnail))

        if shorts:
            assets.append(("▶️ YouTube Short", shorts))

        if reel:
            assets.append(("📸 Instagram Reel", reel))

        if repurposed:
            assets.append(("♻️ Repurposed Content", repurposed))

        if assets:
            for label, value in assets:
                with st.expander(label, expanded=False):

                    if label == "🖼️ Thumbnail" and Path(str(value)).exists():
                        st.image(
                            str(value),
                            caption="Generated Thumbnail",
                            use_container_width=True,
                        )

                        with open(str(value), "rb") as f:
                            st.download_button(
                                "⬇️ Download Thumbnail",
                                f,
                                file_name="thumbnail.png",
                                mime="image/png",
                                key="history_thumbnail_download",
                            )
                    else:
                        st.write(value)

        st.divider()

        if st.button(
            "🎬 Continue Editing This Project",
            use_container_width=True
        ):
            st.session_state["page"] = "Content Studio"
            st.rerun()

    else:

        st.markdown("""
        <div class="hero">
            <h1>📚 Your workspace is empty.</h1>
            <p>
            Create your first idea or generate a content project
            and it will appear here.
            </p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            if st.button(
                "💡 CREATE AN IDEA",
                use_container_width=True
            ):
                st.session_state["page"] = "Idea Lab"
                st.rerun()

        with c2:
            if st.button(
                "🎬 START A PROJECT",
                use_container_width=True
            ):
                st.session_state["page"] = "Content Studio"
                st.rerun()

# =========================================================
# PROFILE
# =========================================================
elif page == "Profile":

    st.title("👤 Profile")
    st.caption("Manage your AI Content Studio workspace.")

    username = st.session_state.get("current_user", "")

    users_file = Path("data/users.json")
    user = {}

    if users_file.exists() and username:
        try:
            users = json.loads(users_file.read_text())
            user = users.get(username, {})
        except Exception:
            user = {}

    # -----------------------------------------------------
    # PROFILE HEADER
    # -----------------------------------------------------
    name = user.get("name", username or "Creator")
    email = user.get("email", "Not available")

    st.markdown(f"""
    <div class="hero">
        <h1>👋 Welcome, {name}</h1>
        <p>Your personal AI Content Studio workspace.</p>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # ACCOUNT DETAILS
    # -----------------------------------------------------
    st.markdown("### 🔐 Account Information")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="card">
            <h3>👤 Creator</h3>
        """, unsafe_allow_html=True)

        st.write("**Name:**", name)
        st.write("**Username:**", username or "Not available")

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <h3>📧 Contact</h3>
        """, unsafe_allow_html=True)

        st.write("**Email:**", email)
        st.write("**Account:**", "Active")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 🧰 Workspace")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("💡 Idea Lab", "Available")

    with c2:
        st.metric("🎬 Content Studio", "Available")

    with c3:
        st.metric("🖼️ Visual Studio", "Available")

    st.divider()

    st.markdown("### 🤖 AI Configuration")

    st.info(
        "Your Content Studio currently uses your local AI setup. "
        "This keeps generation available without requiring a paid cloud API."
    )

    st.markdown("### 🔒 Account")

    if st.button(
        "🚪 LOG OUT",
        use_container_width=True
    ):
        st.session_state["authenticated"] = False
        st.session_state.pop("current_user", None)
        st.session_state["page"] = "Dashboard"
        st.rerun()

    st.caption(
        "AI Content Studio • Creator Workspace"
    )
