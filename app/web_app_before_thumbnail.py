import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import streamlit as st

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

    st.title("⚙️ Content Settings")

    topic = st.text_input(
        "📌 YouTube Topic",
        value="GRWM college morning routine",
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


# ============================================================
# HEADER
# ============================================================

st.title("🎬 AI Content Studio")

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