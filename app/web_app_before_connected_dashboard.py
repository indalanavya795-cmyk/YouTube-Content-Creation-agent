
import streamlit as st

st.set_page_config(
    page_title="AI Content Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {
    max-width: 1380px;
    padding: 2.5rem 3rem 4rem;
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,.16);
}

.hero {
    padding: 20px 0 35px;
}

.eyebrow {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    opacity: .55;
    text-transform: uppercase;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    letter-spacing: -2px;
    margin: 8px 0;
}

.hero-text {
    font-size: 17px;
    opacity: .62;
    max-width: 720px;
}

.card {
    border: 1px solid rgba(128,128,128,.18);
    border-radius: 18px;
    padding: 25px;
    min-height: 170px;
    background: rgba(128,128,128,.035);
}

.card-icon {
    font-size: 30px;
    margin-bottom: 14px;
}

.card-title {
    font-size: 20px;
    font-weight: 700;
}

.card-text {
    font-size: 14px;
    opacity: .62;
    line-height: 1.5;
    margin-top: 7px;
}

.section {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    opacity: .55;
    margin: 28px 0 14px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:10px 4px 25px;">
        <div style="font-size:23px;font-weight:800;">🎬 AI Content Studio</div>
        <div style="font-size:12px;opacity:.55;margin-top:5px;">
            Creator workspace
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "💡 Idea Lab",
            "🎬 Content Studio",
            "🖼️ Visual Studio",
            "📱 Repurpose",
            "📚 History",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("AI Content Studio")
    st.caption("Creator workspace")

if page == "🎬 Content Studio":
    exec(content.read_text(), globals())
    st.stop()

st.markdown("""
<div class="hero">
    <div class="eyebrow">AI CREATOR WORKSPACE</div>
    <div class="hero-title">Create something amazing.</div>
    <div class="hero-text">
        Plan, script, visualize and optimize your YouTube content
        from one intelligent creative workspace.
    </div>
</div>
""", unsafe_allow_html=True)

if page == "🏠 Dashboard":

    st.markdown('<div class="section">Quick actions</div>',
                unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="card">
            <div class="card-icon">💡</div>
            <div class="card-title">Idea Lab</div>
            <div class="card-text">
                Discover creative video concepts, hooks and content angles.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Idea Lab →", key="idea", use_container_width=True):
            st.info("Idea Lab is ready to be connected to your existing generators.")

    with b:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🎬</div>
            <div class="card-title">Content Studio</div>
            <div class="card-text">
                Turn an idea into titles, scripts, storyboards and SEO content.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Content Studio →", key="content",
                     use_container_width=True):
            st.switch_page("web_app.py")

    with c:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🖼️</div>
            <div class="card-title">Visual Studio</div>
            <div class="card-text">
                Create thumbnail concepts, visual plans and production assets.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section">Creator tools</div>',
                unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="card">
            <div class="card-icon">📱</div>
            <div class="card-title">Repurpose</div>
            <div class="card-text">
                Adapt your YouTube content for Shorts and Instagram Reels.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
            <div class="card-icon">📚</div>
            <div class="card-title">History</div>
            <div class="card-text">
                Revisit saved projects and previously generated content.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="card">
            <div class="card-icon">⚙️</div>
            <div class="card-title">Settings</div>
            <div class="card-text">
                Manage your creator workspace and application preferences.
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "💡 Idea Lab":
    st.header("Idea Lab")
    st.write("Your creative idea workspace.")
    st.info("The existing idea-generation features remain inside Content Studio for now.")

elif page == "🖼️ Visual Studio":
    st.header("Visual Studio")
    st.write("Thumbnail concepts, storyboards and visual planning.")

elif page == "📱 Repurpose":
    st.header("Repurpose")
    st.write("Turn your long-form content into Shorts and Reels.")

elif page == "📚 History":
    st.header("Content History")
    st.write("Your saved projects will appear here.")

