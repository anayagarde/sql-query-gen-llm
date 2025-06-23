import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "Enter Key here"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
# models = genai.list_models()
# for m in models:
#     print(m.name)

def clear_data():
     st.session_state["text_input"] = ""
     st.session_state["output"] = ""


def main():
    st.set_page_config(page_title="SQL Query Generator", page_icon=":robot:")
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>SQL Query Generator </h1> 
        </div>
        """, unsafe_allow_html=True,
    )

    if "text_input" not in st.session_state:
         st.session_state["text_input"] = ""

    text_input=st.text_area("Enter your query here in plain English", key="text_input")

    col1, col2 = st.columns((0.17, 1))

    with col1:
        submit=st.button("Generate", key="submit")
    
    with col2:
        clear=st.button("Clear", on_click=clear_data)

    if submit:
           with st.spinner("Generating SQL query..."):
                template="""
                    Create a SQL query snippet using the below text:
                    ```
                    {text_input}
                    ```
                    I just want an SQL query

                """
    
                formatted_template=template.format(text_input=text_input)
                response=model.generate_content(formatted_template)
                sql_query=response.text
             
                expected_output="""
                    What would be the expected response of this SQL snippet:
                    ```
                    {sql_query}
                    ```
                    Provide a small sample table and tabular response of the SQL query.
                    After the sample response, also provide a simple explanation of how the query works. 
                """

                expected_output_formatted=expected_output.format(sql_query=sql_query)
                eoutput=model.generate_content(expected_output_formatted).text
                st.session_state["output"] = f"Submitted: {st.session_state.text_input}"
                
                st.write(sql_query)
                st.write(eoutput)

main()