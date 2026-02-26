import sys
import os
# Ensure project root is importable when running from the repo root or via
# `streamlit run`.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    import streamlit as st
except Exception:
    st = None

# Defer importing project utilities until Streamlit is available so the file
# can be executed in environments where optional dependencies are not yet
# installed. The imports are performed inside `main()` below.


def main():
    if st is None:
        print("Streamlit is not installed in this environment.")
        print("Install dependencies with: pip install -r requirements.txt")
        return

    # Import project utilities now that Streamlit is available.
    try:
        from utils.llm_client import GeminiClient
        from utils.debugging_helper import build_debugging_prompt
    except Exception as e:
        st.error(f"Missing optional project dependency: {e}")
        return
    st.set_page_config(
        page_title= "AI Debugging Assistant",
        page_icon="🔎",
        layout="centered"
    )

    st.title("🔧 AI Debugging Assistant")
    st.write("Paste your **Python Code** or **error log**, and I'll help you debug it.")

    user_input = st.text_area(
        "Enter your code or error log below:",
        height=200,
        placeholder="Example:\nprint(Hello World)"
    )

    if st.button("🔎 Debug Code"):
        if not user_input.strip():
            st.warning("Please enter some code or error message.")
            return
        with st.spinner("Analyzing your code.."):
            try:
                prompt = build_debugging_prompt(user_input)
                client = GeminiClient()
                response = client.ask(prompt)

                st.markdown("---")
                st.subheader("🧠 Debugging Result")
                st.markdown(response)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__=="__main__":
    main()