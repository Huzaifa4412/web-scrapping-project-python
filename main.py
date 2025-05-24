import requests
import streamlit as st


# ---------- Scraping / Fetching Layer ----------
def fetch_user_profile(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def fetch_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


# ---------- Streamlit UI Layer ----------
def main():
    st.set_page_config(page_title="GitHub Profile Analyzer", layout="wide")
    st.title("🐙 GitHub Profile Analyzer")

    username = st.text_input("Enter GitHub username:", value="Huzaifa4412")

    if username:
        # Fetch profile data
        profile = fetch_user_profile(username)
        repos = fetch_user_repos(username)

        if profile:
            st.header(f"👤 {profile.get('name', username)}")
            st.image(profile.get("avatar_url"), width=150)
            st.write(f"**Bio:** {profile.get('bio', 'No bio')}")
            st.write(f"**Public Repos:** {profile.get('public_repos')}")
            st.write(
                f"**Followers:** {profile.get('followers')} | **Following:** {profile.get('following')}"
            )

            if repos:
                # Sort repos by stars descending
                sorted_repos = sorted(
                    repos, key=lambda r: r["stargazers_count"], reverse=True
                )

                st.subheader("📦 Repositories (sorted by stars)")
                for repo in sorted_repos:
                    st.markdown(f"### [{repo['name']}]({repo['html_url']})")
                    st.write(
                        f"⭐ Stars: {repo['stargazers_count']} | 🍴 Forks: {repo['forks_count']} | 🛠 Language: {repo['language']}"
                    )
                    st.write(f"📖 {repo['description']}")
                    st.write("---")

                # Top 5 repos table
                st.subheader("⭐ Top 5 Repositories")
                for repo in sorted_repos[:5]:
                    st.write(
                        f"➡ **{repo['name']}** — ⭐ {repo['stargazers_count']} | 🛠 {repo['language']} | [Link]({repo['html_url']})"
                    )

                # Language distribution (manual count)
                lang_counts = {}
                for repo in repos:
                    lang = repo["language"]
                    if lang:
                        lang_counts[lang] = lang_counts.get(lang, 0) + 1

                st.subheader("🌍 Language Distribution")
                st.bar_chart(lang_counts)

                # Download CSV manually
                csv_lines = ["Name,Description,Stars,Forks,Language,URL"]
                for repo in repos:
                    line = f'"{repo["name"]}","{repo["description"]}","{repo["stargazers_count"]}","{repo["forks_count"]}","{repo["language"]}","{repo["html_url"]}"'
                    csv_lines.append(line)
                csv_content = "\n".join(csv_lines).encode("utf-8")

                st.download_button(
                    "Download Repo Data as CSV",
                    data=csv_content,
                    file_name=f"{username}_repos.csv",
                    mime="text/csv",
                )
            else:
                st.warning("No repositories found or failed to fetch repos.")
        else:
            st.error("GitHub user not found!")


if __name__ == "__main__":
    main()
