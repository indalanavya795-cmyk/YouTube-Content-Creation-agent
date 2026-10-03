import zipfile
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import streamlit as st
from auth import show_auth

# Authentication gate
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    show_auth()
    st.stop()

from thumbnail_maker import create_thumbnail

from agent import (
    generate_content_strategy,
    generate_video_idea,
    generate_titles,
    generate_hooks,
    generate_description,
    generate_hashtags,
    generate_keywords,
    generate_script,
    generate_storyboard,
    generate_visual_plan,
    generate_thumbnail_ideas,
    generate_scene_plan,
    generate_youtube_short,
    generate_instagram_reel,
    generate_repurposed_content,
    generate_seo_analysis,
    generate_content_factory,
    generate_creative_ideas,
    generate_surprise_idea,
    generate_trend_inspired_ideas,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Content Studio",
    page_icon="🎬",
    layout="wide",
)


# ============================================================
# PROFESSIONAL AI SAAS UI
# ============================================================

st.markdown("""
<style>
/* Main application */
.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,.16);
}

[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 600;
    transition: all .15s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
}

/* Inputs */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 9px;
}

/* Cards */
.ac-card {
    border: 1px solid rgba(128,128,128,.18);
    border-radius: 16px;
    padding: 22px;
    min-height: 150px;
    background: rgba(128,128,128,.035);
}

.ac-card:hover {
    border-color: rgba(128,128,128,.35);
}

.ac-icon {
    font-size: 27px;
    margin-bottom: 8px;
}

.ac-title {
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 7px;
}

.ac-text {
    font-size: 13px;
    opacity: .62;
    line-height: 1.5;
}

/* Section headings */
h1, h2, h3 {
    letter-spacing: -.02em;
}

/* Metrics */
[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,.16);
    border-radius: 12px;
    padding: 15px;
}

/* Expanders */
[data-testid="stExpander"] {
    border-radius: 12px;
}

/* Dividers */
hr {
    border-color: rgba(128,128,128,.14);
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# APP HEADER
# ============================================================

st.title("🎬 AI Content Studio")

st.markdown(
    "### AI-powered YouTube content planning, scripting, visuals, thumbnails & SEO"
)

st.caption(
    "Create → Plan → Script → Visualize → Publish"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

HISTORY_FILE = DATA_DIR / "content_history.json"

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "idea": "",
    "strategy": "",
    "titles": "",
    "hooks": "",
    "description": "",
    "hashtags": "",
    "keywords": "",
    "script": "",
    "storyboard": "",
    "visual_plan": "",
    "thumbnail_ideas": "",
    "scene_plan": "",
    "shorts": "",
    "reel": "",
    "repurposed": "",
    "seo": "",
    "factory_completed": False,
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HISTORY
# ============================================================

def load_history():

    if not HISTORY_FILE.exists():
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


def save_history(project):

    history = load_history()

    history.append(project)

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False,
        )


# ============================================================
# CURRENT CONTENT
# ============================================================

def get_current_content():

    return {
        "idea": st.session_state.get(
            "idea",
            "",
        ),
        "strategy": st.session_state.get(
            "strategy",
            "",
        ),
        "titles": st.session_state.get(
            "titles",
            "",
        ),
        "hooks": st.session_state.get(
            "hooks",
            "",
        ),
        "description": st.session_state.get(
            "description",
            "",
        ),
        "hashtags": st.session_state.get(
            "hashtags",
            "",
        ),
        "keywords": st.session_state.get(
            "keywords",
            "",
        ),
        "script": st.session_state.get(
            "script",
            "",
        ),
        "storyboard": st.session_state.get(
            "storyboard",
            "",
        ),
        "visual_plan": st.session_state.get(
            "visual_plan",
            "",
        ),
        "thumbnail_ideas": st.session_state.get(
            "thumbnail_ideas",
            "",
        ),
        "scene_plan": st.session_state.get(
            "scene_plan",
            "",
        ),
        "shorts": st.session_state.get(
            "shorts",
            "",
        ),
        "reel": st.session_state.get(
            "reel",
            "",
        ),
        "repurposed": st.session_state.get(
            "repurposed",
            "",
        ),
        "seo": st.session_state.get(
            "seo",
            "",
        ),
    }


# ============================================================
# SAVE PROJECT
# ============================================================

def save_current_project(
    topic,
    audience,
    tone,
    video_length,
    language,
):

    project = {
        "topic": topic,
        "audience": audience,
        "tone": tone,
        "video_length": video_length,
        "language": language,
        "content": get_current_content(),
    }

    save_history(project)


# ============================================================
# SIMPLE TEXT EXPORT
# ============================================================

def build_text_export():

    content = get_current_content()

    sections = [
        ("CONTENT IDEA", content["idea"]),
        ("CONTENT STRATEGY", content["strategy"]),
        ("TITLES", content["titles"]),
        ("HOOKS", content["hooks"]),
        ("DESCRIPTION", content["description"]),
        ("HASHTAGS", content["hashtags"]),
        ("KEYWORDS", content["keywords"]),
        ("FULL SCRIPT", content["script"]),
        ("STORYBOARD", content["storyboard"]),
        ("VISUAL PLAN", content["visual_plan"]),
        ("THUMBNAIL IDEAS", content["thumbnail_ideas"]),
        ("SCENE PLAN", content["scene_plan"]),
        ("YOUTUBE SHORT", content["shorts"]),
        ("INSTAGRAM REEL", content["reel"]),
        ("REPURPOSED CONTENT", content["repurposed"]),
        ("SEO ANALYSIS", content["seo"]),
    ]

    output = []

    for title, text in sections:

        output.append(
            "\n"
            + "=" * 70
            + "\n"
            + title
            + "\n"
            + "=" * 70
            + "\n"
            + str(text)
            + "\n"
        )

    return "\n".join(output)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    current_user = st.session_state.get("current_user", "Creator")

    st.markdown(
        f"""
        <div style="
            padding:12px;
            margin-bottom:15px;
            border:1px solid rgba(128,128,128,.2);
            border-radius:12px;
        ">
            <div style="font-size:20px;">👤</div>
            <div style="font-weight:600;">{current_user}</div>
            <div style="font-size:12px;opacity:.6;">Creator account</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with st.sidebar:
    st.markdown("""
    <div style="padding:8px 4px 20px 4px;">
        <div style="font-size:22px;font-weight:700;">🎬 AI Content Studio</div>
        <div style="font-size:12px;opacity:.6;margin-top:5px;">
            AI-powered creator workspace
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.title("⚙️ Content Settings")

    topic = st.text_input(
        "📌 YouTube Topic",
        value="GRWM college morning routine",
        key="topic_input",
    )

    audience = st.selectbox(
        "🎯 Target Audience",
        [
            "College Students",
            "Teenagers",
            "Young Adults",
            "Working Professionals",
            "Beginners",
            "General Audience",
            "Content Creators",
        ],
    )

    tone = st.selectbox(
        "🎭 Content Style",
        [
            "Friendly",
            "Professional",
            "Educational",
            "Funny",
            "Energetic",
            "Inspirational",
            "Storytelling",
        ],
    )

    platform = st.selectbox(
        "📱 Main Platform",
        [
            "YouTube",
            "YouTube Shorts",
            "Instagram Reels",
        ],
    )

    video_length = st.selectbox(
        "⏱️ Video Length",
        [
            "Short (1–3 minutes)",
            "Medium (5–8 minutes)",
            "Long (10–15 minutes)",
            "Very Long (20+ minutes)",
        ],
    )

    language = st.selectbox(
        "🌐 Language",
        [
            "English",
            "Telugu",
            "Hindi",
            "Tamil",
            "Kannada",
            "Malayalam",
        ],
    )

    st.divider()

    st.info(
        "💡 Enter a specific topic for more useful "
        "AI-generated content."
    )

    # ========================================================
    # CREATIVE IDEA LAB
    # ========================================================

    st.subheader("💡 Creative Idea Lab")

    idea_content_type = st.selectbox(
        "🎨 Content Type",
        [
            "Lifestyle",
            "Education",
            "Technology",
            "Entertainment",
            "College Life",
            "Storytelling",
            "Self Improvement",
            "Any / Surprise Me",
        ],
        key="idea_content_type",
    )

    idea_goal = st.selectbox(
        "🎯 Content Goal",
        [
            "Get attention",
            "Build engagement",
            "Grow a personal brand",
            "Tell an interesting story",
            "Create something different",
        ],
        key="idea_goal",
    )

    if st.button(
        "💡 GENERATE CREATIVE IDEAS",
        use_container_width=True,
    ):

        with st.spinner(
            "🧠 Brainstorming fresh content ideas..."
        ):

            st.session_state["creative_ideas"] = (
                generate_creative_ideas(
                    audience,
                    platform,
                    idea_content_type,
                    idea_goal,
                )
            )

        st.session_state["creative_ideas_ready"] = True

    st.divider()

    st.caption("Need something more unexpected?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🎲 SURPRISE ME",
            use_container_width=True,
        ):
            with st.spinner("🎲 Creating a surprise idea..."):
                st.session_state["surprise_idea"] = (
                    generate_surprise_idea(
                        audience,
                        platform,
                        idea_content_type,
                    )
                )

            st.session_state["surprise_idea_ready"] = True

    with col2:
        if st.button(
            "🔥 TREND-INSPIRED",
            use_container_width=True,
        ):
            with st.spinner("🔥 Finding trend-inspired concepts..."):
                st.session_state["trend_ideas"] = (
                    generate_trend_inspired_ideas(
                        audience,
                        platform,
                        idea_content_type,
                    )
                )

            st.session_state["trend_ideas_ready"] = True


with st.sidebar:
    st.markdown("---")
    if st.button("＋  Create New Project", use_container_width=True):
        for key in [
            "idea", "strategy", "titles", "hooks", "description",
            "hashtags", "keywords", "script", "storyboard",
            "visual_plan", "scene_plan", "thumbnail_ideas",
            "shorts", "reel", "repurposed"
        ]:
            if key in st.session_state:
                st.session_state[key] = ""
        st.rerun()

# ============================================================
# HEADER
# ============================================================

st.title("🎬 AI Content Studio")

# ============================================================
# SURPRISE ME RESULTS
# ============================================================

if st.session_state.get("surprise_idea_ready"):

    st.divider()
    st.header("🎲 Surprise Idea")

    st.write(
        st.session_state.get(
            "surprise_idea",
            "",
        )
    )

    st.info(
        "💡 Like this idea? Copy its title or use it as your YouTube topic."
    )


# ============================================================
# TREND-INSPIRED RESULTS
# ============================================================

if st.session_state.get("trend_ideas_ready"):

    st.divider()
    st.header("🔥 Trend-Inspired Concepts")

    st.caption(
        "Trend-inspired formats you can adapt to your own content."
    )

    st.write(
        st.session_state.get(
            "trend_ideas",
            "",
        )
    )


# ============================================================
# CREATIVE IDEA LAB RESULTS
# ============================================================

if st.session_state.get("creative_ideas_ready"):

    st.divider()

    st.header("💡 Creative Idea Lab")

    st.caption(
        "Fresh concepts designed to help you decide what to create next."
    )

    st.write(
        st.session_state.get(
            "creative_ideas",
            "",
        )
    )

    st.info(
        "💡 Pick an idea below and use it directly as your YouTube topic."
    )

    idea_titles = re.findall(
        r"(?:\*\*)?TITLE(?:\*\*)?\s*:\s*(.+)",
        st.session_state.get("creative_ideas", ""),
        flags=re.IGNORECASE,
    )

    idea_titles = [
        title.strip().strip("*").strip()
        for title in idea_titles
        if title.strip()
    ]

    if idea_titles:
        selected_idea = st.selectbox(
            "🎯 Choose an idea to use",
            idea_titles,
            key="selected_creative_idea",
        )

        if st.button(
            "🚀 USE THIS IDEA",
            use_container_width=True,
        ):
            st.session_state["topic_input"] = selected_idea
            st.rerun()


st.write(
    "Turn one idea into a complete "
    "multi-platform content production package."
)

st.markdown(
    """
### 🚀 From Idea → Production

**Topic → Strategy → Script → Storyboard → Visual Plan
→ Short/Reel → SEO → Export**

This is more than a text generator.

The AI creates a **production blueprint** for your video,
including scenes, camera directions, voice-over,
on-screen text and visual-generation prompts.
"""
)


# ============================================================
# MAIN ACTION
# ============================================================

st.divider()

st.subheader("🚀 Create Complete Content")

if st.button(
    "🚀 CREATE COMPLETE CONTENT",
    use_container_width=True,
    type="primary",
):

    if not topic.strip():

        st.warning(
            "Please enter a topic first."
        )

    else:

        progress = st.progress(0)

        status = st.empty()

        try:

            status.info(
                "🧠 Creating content strategy..."
            )

            strategy = generate_content_strategy(
                topic,
                audience,
                tone,
                platform,
            )

            st.session_state["strategy"] = strategy

            progress.progress(10)

            status.info(
                "💡 Creating video ideas..."
            )

            idea = generate_video_idea(
                topic,
                audience,
                tone,
            )

            st.session_state["idea"] = idea

            progress.progress(20)

            status.info(
                "🎯 Creating titles and hooks..."
            )

            st.session_state["titles"] = (
                generate_titles(
                    topic,
                    audience,
                    tone,
                )
            )

            st.session_state["hooks"] = (
                generate_hooks(topic)
            )

            progress.progress(30)

            status.info(
                "✍️ Writing the complete script..."
            )

            script = generate_script(
                topic,
                audience,
                tone,
                video_length,
                language,
            )

            st.session_state["script"] = script

            progress.progress(45)

            status.info(
                "🎬 Building storyboard..."
            )

            storyboard = generate_storyboard(
                topic,
                script,
                video_length,
            )

            st.session_state[
                "storyboard"
            ] = storyboard

            progress.progress(60)

            status.info(
                "🖼️ Planning visual assets..."
            )

            st.session_state[
                "visual_plan"
            ] = generate_visual_plan(
                topic,
                storyboard,
            )

            st.session_state[
                "scene_plan"
            ] = generate_scene_plan(
                topic,
                video_length,
            )

            st.session_state[
                "thumbnail_ideas"
            ] = generate_thumbnail_ideas(
                topic
            )

            # Create the actual thumbnail image locally
            thumbnail_path = OUTPUT_DIR / "thumbnail.png"

            create_thumbnail(
                topic=topic,
                headline=f"{topic} — WATCH THIS",
                output_path=str(thumbnail_path),
            )

            st.session_state[
                "thumbnail_path"
            ] = str(thumbnail_path)

            progress.progress(70)

            status.info(
                "📱 Creating short-form content..."
            )

            st.session_state[
                "shorts"
            ] = generate_youtube_short(topic)

            st.session_state[
                "reel"
            ] = generate_instagram_reel(topic)

            st.session_state[
                "repurposed"
            ] = generate_repurposed_content(
                topic
            )

            progress.progress(82)

            status.info(
                "🔍 Running SEO analysis..."
            )

            st.session_state[
                "description"
            ] = generate_description(topic)

            st.session_state[
                "hashtags"
            ] = generate_hashtags(topic)

            st.session_state[
                "keywords"
            ] = generate_keywords(topic)

            st.session_state[
                "seo"
            ] = generate_seo_analysis(
                topic,
                st.session_state["titles"],
                st.session_state["description"],
                st.session_state["keywords"],
            )

            progress.progress(100)

            st.session_state[
                "factory_completed"
            ] = True

            status.success(
                "🎉 Complete production package created!"
            )

        except Exception as error:

            st.session_state[
                "factory_completed"
            ] = False

            progress.empty()

            status.error(
                f"❌ Generation failed: {error}"
            )


# ============================================================
# DOWNLOAD COMPLETE PACKAGE
# ============================================================

if st.session_state.get("factory_completed"):

    package_files = {
        "content_strategy.txt": st.session_state.get("strategy", ""),
        "video_idea.txt": st.session_state.get("idea", ""),
        "titles.txt": st.session_state.get("titles", ""),
        "hooks.txt": st.session_state.get("hooks", ""),
        "script.txt": st.session_state.get("script", ""),
        "storyboard.txt": st.session_state.get("storyboard", ""),
        "visual_plan.txt": st.session_state.get("visual_plan", ""),
        "scene_plan.txt": st.session_state.get("scene_plan", ""),
        "thumbnail_concepts.txt": st.session_state.get("thumbnail_ideas", ""),
        "youtube_short.txt": st.session_state.get("shorts", ""),
        "instagram_reel.txt": st.session_state.get("reel", ""),
        "repurposed_content.txt": st.session_state.get("repurposed", ""),
        "seo_analysis.txt": st.session_state.get("seo", ""),
    }

    zip_path = OUTPUT_DIR / "complete_content_package.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as package:

        for filename, content in package_files.items():
            package.writestr(filename, str(content))

        thumbnail = st.session_state.get("thumbnail_path")

        if thumbnail and Path(thumbnail).exists():
            package.write(thumbnail, "thumbnail.png")

    with open(zip_path, "rb") as package_file:

        st.download_button(
            "📦 DOWNLOAD COMPLETE PACKAGE",
            package_file,
            file_name="AI_Content_Studio_Package.zip",
            mime="application/zip",
            use_container_width=True,
        )


# ============================================================
# RESULTS
# ============================================================

if st.session_state.get(
    "factory_completed"
):

    st.divider()

    st.header(
        "📦 Complete Production Package"
    )

    st.success(
        "Your topic has been transformed into "
        "a complete content-production blueprint."
    )

    # ========================================================
    # PROJECT DASHBOARD
    # ========================================================

    st.subheader("📊 Project Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🧠 Strategy", "✓ Ready")

    with col2:
        st.metric("✍️ Script", "✓ Ready")

    with col3:
        st.metric("🖼️ Thumbnail", "✓ Ready")

    with col4:
        st.metric("🔍 SEO", "✓ Ready")

    st.caption(
        f"🎬 Project Topic: {topic}"
    )

    tabs = st.tabs(
        [
            "🧠 Strategy",
            "✍️ Script",
            "🎬 Storyboard",
            "🖼️ Visuals",
            "📱 Social",
            "🔍 SEO",
        ]
    )

    # ========================================================
    # STRATEGY
    # ========================================================

    with tabs[0]:

        st.subheader(
            "🧠 Content Strategy"
        )

        st.write(
            st.session_state[
                "strategy"
            ]
        )

        st.subheader(
            "💡 Video Ideas"
        )

        st.code(
            st.session_state[
                "idea"
            ],
            language=None,
        )

        st.subheader(
            "🎯 Titles"
        )

        st.code(
            st.session_state[
                "titles"
            ],
            language=None,
        )

        st.subheader(
            "🪝 Hooks"
        )

        st.code(
            st.session_state[
                "hooks"
            ],
            language=None,
        )

    # ========================================================
    # SCRIPT
    # ========================================================

    with tabs[1]:

        st.subheader(
            "📜 Full YouTube Script"
        )

        st.code(
            st.session_state[
                "script"
            ],
            language=None,
        )

    # ========================================================
    # STORYBOARD
    # ========================================================

    with tabs[2]:

        st.subheader(
            "🎬 Production Storyboard"
        )

        st.write(
            st.session_state[
                "storyboard"
            ]
        )

        st.subheader(
            "🎞️ Scene Plan"
        )

        st.code(
            st.session_state[
                "scene_plan"
            ],
            language=None,
        )

    # ========================================================
    # VISUALS
    # ========================================================

    with tabs[3]:

        st.subheader(
            "🖼️ Visual Asset Plan"
        )

        st.write(
            st.session_state[
                "visual_plan"
            ]
        )

        st.subheader(
            "🖼️ Thumbnail Concepts"
        )

        st.code(
            st.session_state[
                "thumbnail_ideas"
            ],
            language=None,
        )

        # ====================================================
        # GENERATED THUMBNAIL
        # ====================================================

        thumbnail_path = st.session_state.get(
            "thumbnail_path"
        )

        if thumbnail_path and Path(
            thumbnail_path
        ).exists():

            st.subheader(
                "🎨 Generated Thumbnail"
            )

            st.image(
                thumbnail_path,
                caption="AI Content Studio Thumbnail",
                use_container_width=True,
            )

            with open(
                thumbnail_path,
                "rb",
            ) as image_file:

                st.download_button(
                    "⬇️ Download Thumbnail",
                    image_file,
                    file_name="youtube_thumbnail.png",
                    mime="image/png",
                    use_container_width=True,
                )

    # ========================================================
    # SOCIAL
    # ========================================================

    with tabs[4]:

        st.subheader(
            "📱 YouTube Short"
        )

        st.code(
            st.session_state[
                "shorts"
            ],
            language=None,
        )

        st.subheader(
            "📸 Instagram Reel"
        )

        st.code(
            st.session_state[
                "reel"
            ],
            language=None,
        )

        st.subheader(
            "🔄 Repurposed Content"
        )

        st.code(
            st.session_state[
                "repurposed"
            ],
            language=None,
        )

    # ========================================================
    # SEO
    # ========================================================

    with tabs[5]:

        st.subheader(
            "📝 Description"
        )

        st.code(
            st.session_state[
                "description"
            ],
            language=None,
        )

        st.subheader(
            "#️⃣ Hashtags"
        )

        st.code(
            st.session_state[
                "hashtags"
            ],
            language=None,
        )

        st.subheader(
            "🔑 Keywords"
        )

        st.code(
            st.session_state[
                "keywords"
            ],
            language=None,
        )

        st.subheader(
            "🔍 SEO Analysis"
        )

        st.write(
            st.session_state[
                "seo"
            ]
        )


# ============================================================
# INDIVIDUAL TOOLS
# ============================================================

st.divider()

st.header(
    "🛠️ Individual Production Tools"
)

st.write(
    "Generate or regenerate one part of the "
    "production pipeline without creating everything."
)


tool_tabs = st.tabs(
    [
        "💡 Ideas",
        "🎯 Titles",
        "🪝 Hooks",
        "📜 Script",
        "🎬 Storyboard",
        "🖼️ Visuals",
        "📱 Short/Reel",
        "🔍 SEO",
    ]
)


# ============================================================
# IDEAS
# ============================================================

with tool_tabs[0]:

    if st.button(
        "💡 Generate Video Ideas",
        key="individual_ideas",
        use_container_width=True,
    ):

        with st.spinner(
            "Creating video ideas..."
        ):

            result = generate_video_idea(
                topic,
                audience,
                tone,
            )

        st.session_state[
            "idea"
        ] = result

        st.code(
            result,
            language=None,
        )


# ============================================================
# TITLES
# ============================================================

with tool_tabs[1]:

    if st.button(
        "🎯 Generate Titles",
        key="individual_titles",
        use_container_width=True,
    ):

        with st.spinner(
            "Creating titles..."
        ):

            result = generate_titles(
                topic,
                audience,
                tone,
            )

        st.session_state[
            "titles"
        ] = result

        st.code(
            result,
            language=None,
        )


# ============================================================
# HOOKS
# ============================================================

with tool_tabs[2]:

    if st.button(
        "🪝 Generate Hooks",
        key="individual_hooks",
        use_container_width=True,
    ):

        with st.spinner(
            "Creating hooks..."
        ):

            result = generate_hooks(topic)

        st.session_state[
            "hooks"
        ] = result

        st.code(
            result,
            language=None,
        )


# ============================================================
# SCRIPT
# ============================================================

with tool_tabs[3]:

    if st.button(
        "📜 Generate Full Script",
        key="individual_script",
        use_container_width=True,
    ):

        with st.spinner(
            "Writing script..."
        ):

            result = generate_script(
                topic,
                audience,
                tone,
                video_length,
                language,
            )

        st.session_state[
            "script"
        ] = result

        st.code(
            result,
            language=None,
        )


# ============================================================
# STORYBOARD
# ============================================================

with tool_tabs[4]:

    if st.button(
        "🎬 Generate Storyboard",
        key="individual_storyboard",
        use_container_width=True,
    ):

        script = st.session_state.get(
            "script",
            "",
        )

        if not script:

            st.warning(
                "Generate a script first."
            )

        else:

            with st.spinner(
                "Building production storyboard..."
            ):

                result = generate_storyboard(
                    topic,
                    script,
                    video_length,
                )

            st.session_state[
                "storyboard"
            ] = result

            st.write(result)


# ============================================================
# VISUALS
# ============================================================

with tool_tabs[5]:

    if st.button(
        "🖼️ Generate Visual Plan",
        key="individual_visuals",
        use_container_width=True,
    ):

        storyboard = st.session_state.get(
            "storyboard",
            "",
        )

        if not storyboard:

            st.warning(
                "Generate a storyboard first."
            )

        else:

            with st.spinner(
                "Planning visual assets..."
            ):

                result = generate_visual_plan(
                    topic,
                    storyboard,
                )

            st.session_state[
                "visual_plan"
            ] = result

            st.write(result)

    st.divider()

    if st.button(
        "🖼️ Generate Thumbnail Concepts",
        key="individual_thumbnail",
        use_container_width=True,
    ):

        with st.spinner(
            "Creating thumbnail concepts..."
        ):

            result = generate_thumbnail_ideas(
                topic
            )

        st.session_state[
            "thumbnail_ideas"
        ] = result

        st.code(
            result,
            language=None,
        )

        # Create an actual thumbnail locally
        thumbnail_path = OUTPUT_DIR / "thumbnail.png"

        try:

            create_thumbnail(
                topic=topic,
                headline=str(st.session_state.get("titles", f"{topic} — WATCH THIS")).splitlines()[0],
                output_path=str(thumbnail_path),
            )

            st.subheader("🖼️ Generated Thumbnail")

            st.image(
                str(thumbnail_path),
                caption="AI Content Studio Thumbnail",
                use_container_width=True,
            )

            with open(
                thumbnail_path,
                "rb",
            ) as image_file:

                st.download_button(
                    "⬇️ Download Thumbnail",
                    image_file,
                    file_name="youtube_thumbnail.png",
                    mime="image/png",
                    use_container_width=True,
                )

        except Exception as error:

            st.error(
                f"Thumbnail creation failed: {error}"
            )


# ============================================================
# SHORT / REEL
# ============================================================

with tool_tabs[6]:

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📱 Generate YouTube Short",
            key="individual_short",
            use_container_width=True,
        ):

            with st.spinner(
                "Creating Short..."
            ):

                result = generate_youtube_short(
                    topic
                )

            st.session_state[
                "shorts"
            ] = result

            st.code(
                result,
                language=None,
            )

    with col2:

        if st.button(
            "📸 Generate Instagram Reel",
            key="individual_reel",
            use_container_width=True,
        ):

            with st.spinner(
                "Creating Reel..."
            ):

                result = generate_instagram_reel(
                    topic
                )

            st.session_state[
                "reel"
            ] = result

            st.code(
                result,
                language=None,
            )

    st.divider()

    if st.button(
        "🔄 Generate Repurposed Content",
        key="individual_repurpose",
        use_container_width=True,
    ):

        with st.spinner(
            "Repurposing content..."
        ):

            result = generate_repurposed_content(
                topic
            )

        st.session_state[
            "repurposed"
        ] = result

        st.code(
            result,
            language=None,
        )


# ============================================================
# SEO
# ============================================================

with tool_tabs[7]:

    if st.button(
        "🔍 Generate SEO Analysis",
        key="individual_seo",
        use_container_width=True,
    ):

        with st.spinner(
            "Analyzing SEO..."
        ):

            result = generate_seo_analysis(
                topic,
                st.session_state.get(
                    "titles",
                    "",
                ),
                st.session_state.get(
                    "description",
                    "",
                ),
                st.session_state.get(
                    "keywords",
                    "",
                ),
            )

        st.session_state[
            "seo"
        ] = result

        st.write(result)


# ============================================================
# EXPORT
# ============================================================

st.divider()

st.header("📦 Export & Save")

if st.session_state.get(
    "factory_completed"
):

    export_text = build_text_export()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Save Project",
            use_container_width=True,
        ):

            save_current_project(
                topic,
                audience,
                tone,
                video_length,
                language,
            )

            st.success(
                "Project saved to Content History."
            )

    with col2:

        st.download_button(
            "📄 Download Content Package",
            data=export_text,
            file_name="ai_content_package.txt",
            mime="text/plain",
            use_container_width=True,
        )

else:

    st.info(
        "Create a complete content package first "
        "to enable the full export."
    )


# ============================================================
# CONTENT HISTORY
# ============================================================

st.divider()

st.header("📚 Content History")

history = load_history()

if not history:

    st.info(
        "No saved projects yet."
    )

else:

    st.write(
        f"Saved projects: **{len(history)}**"
    )

    for index, project in enumerate(
        reversed(history)
    ):

        project_topic = project.get(
            "topic",
            "Untitled",
        )

        with st.expander(
            f"📁 {index + 1}. {project_topic}"
        ):

            st.write(
                f"**Audience:** "
                f"{project.get('audience', '')}"
            )

            st.write(
                f"**Tone:** "
                f"{project.get('tone', '')}"
            )

            st.write(
                f"**Platform:** "
                f"{project.get('platform', '')}"
            )

            saved_content = project.get(
                "content",
                {},
            )

            st.subheader(
                "💡 Idea"
            )

            st.write(
                saved_content.get(
                    "idea",
                    "",
                )
            )

            st.subheader(
                "📜 Script"
            )

            st.code(
                saved_content.get(
                    "script",
                    "",
                ),
                language=None,
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎬 AI Content Studio • "
    "Python + Streamlit + Ollama"
)