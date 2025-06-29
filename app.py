import streamlit as st
import downloader


@st.dialog("KapTube")
def show_video_player() -> None:
    st.markdown(f"##### {yt_vid.title}")

    if yt_vid.content:
        st.video(yt_vid.content, autoplay=True, loop=True)
        st.download_button(
            "Download",
            yt_vid.content,
            file_name=yt_vid.filename,
            mime="video/mp4",
            type="primary",
            icon=":material/vertical_align_bottom:",
            use_container_width=True
        )
    else:
        st.video(yt_vid.url, autoplay=True, loop=True)
        download_btn = st.button(
            "Download", type="primary", icon=":material/vertical_align_bottom:", use_container_width=True
        )

        if download_btn:
            st.markdown(
                f"""
                    <script>
                        window.open("{yt_vid.url}", "_blank");
                    </script>
                """,
                unsafe_allow_html=True
            )



st.set_page_config(
    page_title="KapTube | #dwighthacks",
    page_icon="https://img.icons8.com/?size=120&id=HFMepZno1mLn&format=png"
)

st.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, h1, h2, h3, h4, h5, h6, p, input {
        font-family: 'Inter', sans-serif !important;
    }
    </style>
""")

yt_vid = None
error_message = None
search_triggered = False

_, mid_col, _ = st.columns([1, 4, 1])

with mid_col:
    with st.container(border=True):
        _, title_col, _ = st.columns([1, 0.9, 1])
        with title_col:
            st.markdown("#### KapTube")

        yt_url = st.text_input("Video URL", placeholder="https://www.youtube.com/watch?v=xvFZjo5PgG0")
        search_btn = st.button(
            "Search", type="primary",
            icon=":material/search:",
            use_container_width=True
        )

    _, footer_col, _ = st.columns([1, 0.6, 1])
    with footer_col:
        st.text("#dwighthacks")

    if search_btn:
        search_triggered = True
        with st.spinner("Pulling media from Google servers...", show_time=True):
            try:
                yt_vid = downloader.download(yt_url, max_attempts=10)
                if not yt_vid:
                    error_message = "Unable to download this video due to licensing issues. It might be DRM-protected."
            except Exception as e:
                error_message = f"There was a problem downloading this video. {type(e).__name__}: {e}"

# Outside mid_col: show result
if search_triggered:
    if yt_vid:
        show_video_player()

    if error_message:
        with mid_col:
            st.error(error_message, icon=":material/file_download_off:")
